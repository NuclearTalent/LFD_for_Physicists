/*
 * phrase-search.js
 *
 * Exact quoted-phrase searching plus persistent result-page highlighting
 * for Jupyter Book 1 / Sphinx 7.4.x.
 *
 * Quoted searches are displayed in Jupyter Book TOC/sidebar order.
 * Ordinary unquoted searches retain Sphinx's normal relevance ordering.
 *
 * Examples:
 *
 *   statistical model
 *       -> ordinary Sphinx search/relevance ordering
 *       -> each result page highlights "statistical" and "model"
 *
 *   "statistical model"
 *       -> only pages containing the exact phrase are returned
 *       -> matching pages are listed in book/TOC order
 *       -> each result page highlights the whole phrase as a unit
 *
 *   "statistical model" likelihood
 *       -> pages must contain the exact phrase and satisfy the normal
 *          Sphinx search for likelihood
 *       -> matching pages are listed in book/TOC order
 *       -> the phrase is highlighted as a unit and likelihood separately
 *
 * Curly double quotes (“...”) are treated like straight quotes ("...").
 *
 * Phrase filtering fetches candidate HTML pages in the browser, so quoted
 * searches require HTTP/HTTPS (GitHub Pages or a local web server), not file://.
 */

(function () {
  "use strict";

  const HIGHLIGHT_STORAGE_KEY =
    "jb_search_highlight_payload";

  const HIGHLIGHT_MAX_AGE_MS =
    10 * 60 * 1000;

  function normalizeText(text) {
    return text
      .toLowerCase()
      .replace(/\u00ad/g, "")
      .replace(/[\u200b-\u200d\uFEFF]/g, "")
      .replace(/\s+/g, " ")
      .trim();
  }

  function escapeRegExp(text) {
    return text.replace(
      /[.*+?^${}()|[\]\\]/g,
      "\\$&"
    );
  }

  function parseQuotedPhrases(query) {
    const normalizedQuery =
      query.replace(/[“”]/g, '"');

    const phrases = [];
    const re = /"([^"]+)"/g;
    let match;

    while (
      (match = re.exec(normalizedQuery)) !== null
    ) {
      const phrase =
        normalizeText(match[1]);

      if (phrase) {
        phrases.push(phrase);
      }
    }

    const unquotedQuery =
      normalizedQuery
        .replace(/"[^"]*"/g, " ")
        .replace(/\s+/g, " ")
        .trim();

    return {
      normalizedQuery,
      phrases,
      unquotedQuery,
    };
  }

  function requestUrlForResult(result) {
    const docName = result[0];

    const contentRoot =
      document.documentElement
        .dataset.content_root || "";

    if (
      DOCUMENTATION_OPTIONS.BUILDER ===
      "dirhtml"
    ) {
      let dirname =
        docName + "/";

      if (
        dirname.match(/\/index\/$/)
      ) {
        dirname =
          dirname.substring(
            0,
            dirname.length - 6
          );
      } else if (
        dirname === "index/"
      ) {
        dirname = "";
      }

      return (
        contentRoot +
        dirname
      );
    }

    return (
      contentRoot +
      docName +
      DOCUMENTATION_OPTIONS.FILE_SUFFIX
    );
  }

  function clearSphinxHighlightStorage() {
    try {
      localStorage.removeItem(
        "sphinx_highlight_terms"
      );
    } catch (error) {
      // Safe to ignore.
    }
  }

  /*
   * ------------------------------------------------------------
   * TOC/book ordering for quoted searches
   * ------------------------------------------------------------
   */

  function canonicalPageKey(urlLike) {
    const url =
      new URL(
        urlLike,
        window.location.href
      );

    url.hash = "";
    url.search = "";

    let path =
      url.pathname;

    path =
      path.replace(
        /\/index\.html$/,
        "/"
      );

    return (
      url.origin +
      path
    );
  }

  function buildTocOrderMap() {
    const tocOrder =
      new Map();

    const tocLinks =
      document.querySelectorAll(
        "nav.bd-links a.reference.internal[href], " +
        ".bd-sidenav a.reference.internal[href]"
      );

    let nextRank = 0;

    tocLinks.forEach(
      (link) => {
        const href =
          link.getAttribute(
            "href"
          );

        if (
          !href ||
          href === "#"
        ) {
          return;
        }

        const key =
          canonicalPageKey(
            href
          );

        if (
          !tocOrder.has(key)
        ) {
          tocOrder.set(
            key,
            nextRank
          );

          nextRank += 1;
        }
      }
    );

    return tocOrder;
  }

  function orderPhraseResultsByToc(
    results
  ) {
    const tocOrder =
      buildTocOrderMap();

    if (!tocOrder.size) {
      console.warn(
        "Phrase search could not find the Jupyter Book sidebar TOC; " +
        "keeping Sphinx's original result ordering."
      );

      return results;
    }

    /*
     * Sphinx displays results using results.pop().
     * Reverse first to obtain actual display order.
     */
    const currentDisplayOrder =
      results
        .slice()
        .reverse();

    const inToc = [];
    const notInToc = [];

    currentDisplayOrder.forEach(
      (
        result,
        originalDisplayIndex
      ) => {
        const key =
          canonicalPageKey(
            requestUrlForResult(
              result
            )
          );

        if (
          tocOrder.has(key)
        ) {
          inToc.push({
            result,
            rank:
              tocOrder.get(key),
            originalDisplayIndex,
          });
        } else {
          notInToc.push({
            result,
            originalDisplayIndex,
          });
        }
      }
    );

    inToc.sort(
      (a, b) => {
        if (
          a.rank !== b.rank
        ) {
          return (
            a.rank -
            b.rank
          );
        }

        return (
          a.originalDisplayIndex -
          b.originalDisplayIndex
        );
      }
    );

    const desiredDisplayOrder = [
      ...inToc.map(
        (entry) =>
          entry.result
      ),

      ...notInToc.map(
        (entry) =>
          entry.result
      ),
    ];

    /*
     * Reverse again because Sphinx consumes the array with pop().
     */
    return (
      desiredDisplayOrder
        .reverse()
    );
  }

  /*
   * ------------------------------------------------------------
   * Persistent highlighting WITHOUT changing result URLs
   * ------------------------------------------------------------
   */

  function saveHighlightPayload(
    link,
    phrases,
    words
  ) {
    try {
      const href =
        link.getAttribute(
          "href"
        );

      if (!href) {
        return;
      }

      const targetUrl =
        new URL(
          href,
          window.location.href
        );

      const payload = {
        targetPath:
          targetUrl.pathname,

        phrases:
          [...phrases],

        words:
          [...words],

        createdAt:
          Date.now(),
      };

      localStorage.setItem(
        HIGHLIGHT_STORAGE_KEY,
        JSON.stringify(
          payload
        )
      );

    } catch (error) {
      console.warn(
        "Could not save search highlighting state:",
        error
      );
    }
  }

  function readHighlightPayloadForCurrentPage() {
    try {
      const raw =
        localStorage.getItem(
          HIGHLIGHT_STORAGE_KEY
        );

      if (!raw) {
        return null;
      }

      const payload =
        JSON.parse(raw);

      const tooOld =
        !payload.createdAt ||
        (
          Date.now() -
          payload.createdAt
        ) >
        HIGHLIGHT_MAX_AGE_MS;

      const wrongPage =
        payload.targetPath !==
        window.location.pathname;

      if (
        tooOld ||
        wrongPage
      ) {
        localStorage.removeItem(
          HIGHLIGHT_STORAGE_KEY
        );

        return null;
      }

      /*
       * Consume this payload. Going back to the search page and
       * clicking another result writes a fresh one.
       */
      localStorage.removeItem(
        HIGHLIGHT_STORAGE_KEY
      );

      return payload;

    } catch (error) {
      try {
        localStorage.removeItem(
          HIGHLIGHT_STORAGE_KEY
        );
      } catch (_) {
        // Ignore.
      }

      return null;
    }
  }

  /*
   * ------------------------------------------------------------
   * Destination-page highlighting
   * ------------------------------------------------------------
   */

  function unwrapExistingHighlights(
    root
  ) {
    const parents =
      new Set();

    root
      .querySelectorAll(
        "span.highlighted"
      )
      .forEach(
        (span) => {
          const parent =
            span.parentNode;

          if (!parent) {
            return;
          }

          while (
            span.firstChild
          ) {
            parent.insertBefore(
              span.firstChild,
              span
            );
          }

          span.remove();

          parents.add(
            parent
          );
        }
      );

    parents.forEach(
      (parent) =>
        parent.normalize()
    );
  }

  function highlightTextInNode(
    node,
    text
  ) {
    if (
      node.nodeType ===
      Node.TEXT_NODE
    ) {
      const parent =
        node.parentNode;

      if (
        !parent ||
        !node.nodeValue
      ) {
        return;
      }

      if (
        parent.closest(
          "script, style, button, select, textarea, " +
          ".nohighlight, .highlighted"
        )
      ) {
        return;
      }

      /*
       * Permit arbitrary whitespace between phrase words.
       */
      const pieces =
        text
          .trim()
          .split(/\s+/)
          .map(
            escapeRegExp
          );

      if (
        !pieces.length
      ) {
        return;
      }

      const pattern =
        new RegExp(
          pieces.join(
            "\\s+"
          ),
          "i"
        );

      const match =
        pattern.exec(
          node.nodeValue
        );

      if (!match) {
        return;
      }

      const before =
        node.nodeValue.slice(
          0,
          match.index
        );

      const matched =
        node.nodeValue.slice(
          match.index,
          match.index +
            match[0].length
        );

      const after =
        node.nodeValue.slice(
          match.index +
            match[0].length
        );

      const span =
        document.createElement(
          "span"
        );

      span.classList.add(
        "highlighted"
      );

      span.textContent =
        matched;

      const parentNode =
        node.parentNode;

      const beforeNode =
        document.createTextNode(
          before
        );

      const afterNode =
        document.createTextNode(
          after
        );

      parentNode.insertBefore(
        beforeNode,
        node
      );

      parentNode.insertBefore(
        span,
        node
      );

      parentNode.insertBefore(
        afterNode,
        node
      );

      node.remove();

      /*
       * Highlight further occurrences in the remainder.
       */
      highlightTextInNode(
        afterNode,
        text
      );

      return;
    }

    if (
      node.nodeType ===
        Node.ELEMENT_NODE &&
      !node.matches(
        "script, style, button, select, textarea, " +
        ".nohighlight, .highlighted"
      )
    ) {
      Array.from(
        node.childNodes
      ).forEach(
        (child) => {
          highlightTextInNode(
            child,
            text
          );
        }
      );
    }
  }

  function addHideHighlightsLink(
    root
  ) {
    if (
      document.querySelector(
        "#searchbox .highlight-link"
      )
    ) {
      return;
    }

    const searchBox =
      document.getElementById(
        "searchbox"
      );

    if (!searchBox) {
      return;
    }

    const p =
      document.createElement(
        "p"
      );

    p.classList.add(
      "highlight-link"
    );

    const a =
      document.createElement(
        "a"
      );

    a.href = "#";

    a.textContent =
      typeof _ ===
      "function"
        ? _(
            "Hide Search Matches"
          )
        : "Hide Search Matches";

    a.addEventListener(
      "click",
      (event) => {
        event.preventDefault();

        unwrapExistingHighlights(
          root
        );

        p.remove();
      }
    );

    p.appendChild(a);

    searchBox.appendChild(
      p
    );
  }

  function highlightDestinationTerms(
    phrases,
    words
  ) {
    if (
      !phrases.length &&
      !words.length
    ) {
      return;
    }

    const root =
      document.querySelector(
        '[role="main"]'
      ) ||
      document.querySelector(
        "div.body"
      ) ||
      document.body;

    if (!root) {
      return;
    }

    unwrapExistingHighlights(
      root
    );

    /*
     * Highlight complete quoted phrases first.
     */
    [...phrases]
      .sort(
        (a, b) =>
          b.length -
          a.length
      )
      .forEach(
        (phrase) => {
          highlightTextInNode(
            root,
            phrase
          );
        }
      );

    /*
     * Then highlight unquoted words.
     */
    [
      ...new Set(
        words
      ),
    ].forEach(
      (word) => {
        highlightTextInNode(
          root,
          word
        );
      }
    );

    addHideHighlightsLink(
      root
    );
  }

  const destinationPayload =
    readHighlightPayloadForCurrentPage();

  if (
    destinationPayload
  ) {
    clearSphinxHighlightStorage();

    const applyHighlights =
      () => {
        highlightDestinationTerms(
          destinationPayload
            .phrases || [],

          destinationPayload
            .words || []
        );
      };

    if (
      document.readyState ===
      "loading"
    ) {
      document.addEventListener(
        "DOMContentLoaded",
        applyHighlights
      );
    } else {
      applyHighlights();
    }
  }

  /*
   * ------------------------------------------------------------
   * Search-result highlighting handler
   * ------------------------------------------------------------
   */

  function extractHighlightTerms(
    query
  ) {
    const terms =
      new Set();

    if (!query.trim()) {
      return terms;
    }

    splitQuery(
      query.trim()
    ).forEach(
      (queryTerm) => {
        const lower =
          queryTerm.toLowerCase();

        if (
          stopwords.indexOf(
            lower
          ) !== -1 ||
          queryTerm.match(
            /^\d+$/
          )
        ) {
          return;
        }

        terms.add(
          lower
        );
      }
    );

    return terms;
  }

  function installResultHighlightHandler(
    phrases,
    words
  ) {
    if (!Search.output) {
      return;
    }

    if (
      Search.output
        ._jbHighlightHandlerInstalled
    ) {
      return;
    }

    Search.output
      ._jbHighlightHandlerInstalled =
      true;

    const rememberForEvent =
      (event) => {
        const target =
          event.target instanceof
          Element
            ? event.target
            : event.target.parentElement;

        if (!target) {
          return;
        }

        const link =
          target.closest(
            "a[href]"
          );

        if (
          !link ||
          !Search.output.contains(
            link
          )
        ) {
          return;
        }

        /*
         * IMPORTANT:
         *
         * Do NOT alter link.href here.
         * Sphinx generated the correct destination URL.
         */
        saveHighlightPayload(
          link,
          phrases,
          words
        );
      };

    Search.output.addEventListener(
      "click",
      rememberForEvent,
      true
    );

    Search.output.addEventListener(
      "auxclick",
      rememberForEvent,
      true
    );

    Search.output.addEventListener(
      "contextmenu",
      rememberForEvent,
      true
    );
  }

  /*
   * ------------------------------------------------------------
   * Search implementation
   * ------------------------------------------------------------
   */

  function installPhraseSearch() {
    if (
      typeof Search ===
      "undefined"
    ) {
      return;
    }

    if (
      Search._phraseSearchInstalled
    ) {
      return;
    }

    Search._phraseSearchInstalled =
      true;

    const pageTextCache =
      new Map();

    async function fetchPageText(
      result
    ) {
      const url =
        requestUrlForResult(
          result
        );

      if (
        !pageTextCache.has(
          url
        )
      ) {
        pageTextCache.set(
          url,

          fetch(url)
            .then(
              (response) => {
                if (
                  !response.ok
                ) {
                  throw new Error(
                    `HTTP ${response.status} for ${url}`
                  );
                }

                return (
                  response.text()
                );
              }
            )
            .then(
              (html) =>
                normalizeText(
                  Search.htmlToText(
                    html,
                    ""
                  )
                )
            )
        );
      }

      return (
        pageTextCache.get(
          url
        )
      );
    }

    Search.query =
      async function (
        query
      ) {
        const parsed =
          parseQuotedPhrases(
            query
          );

        /*
         * ------------------------------------------------------
         * Ordinary unquoted search
         * ------------------------------------------------------
         *
         * Keep Sphinx's normal relevance ordering.
         */

        if (
          parsed.phrases
            .length === 0
        ) {
          const [
            searchQuery,
            searchTerms,
            excludedTerms,
            highlightTerms,
            objectTerms,
          ] =
            Search._parseQuery(
              query
            );

          clearSphinxHighlightStorage();

          const results =
            Search._performSearch(
              searchQuery,
              searchTerms,
              excludedTerms,
              highlightTerms,
              objectTerms
            );

          installResultHighlightHandler(
            [],
            [...highlightTerms]
          );

          _displayNextItem(
            results,
            results.length,
            searchTerms,
            highlightTerms
          );

          return;
        }

        /*
         * ------------------------------------------------------
         * Quoted phrase search
         * ------------------------------------------------------
         */

        if (
          window.location.protocol ===
          "file:"
        ) {
          console.warn(
            "Exact phrase search requires the book " +
            "to be served over HTTP/HTTPS."
          );

          if (
            Search.status
          ) {
            Search.status.innerText =
              "Exact phrase search requires HTTP/HTTPS. " +
              "Serve _build/html locally instead of opening " +
              "search.html directly.";
          }

          Search.stopPulse();

          return;
        }

        /*
         * Use Sphinx's index as a fast candidate search.
         */
        const candidateQuery =
          parsed.normalizedQuery
            .replace(
              /"/g,
              " "
            )
            .replace(
              /\s+/g,
              " "
            )
            .trim();

        const [
          searchQuery,
          searchTerms,
          excludedTerms,
          _allHighlightTerms,
          objectTerms,
        ] =
          Search._parseQuery(
            candidateQuery
          );

        clearSphinxHighlightStorage();

        const candidates =
          Search._performSearch(
            searchQuery,
            searchTerms,
            excludedTerms,
            new Set(),
            objectTerms
          );

        if (
          Search.status
        ) {
          Search.status.innerText =
            `Checking ${candidates.length} ` +
            `candidate page(s) for exact phrase...`;
        }

        const checks =
          await Promise.all(
            candidates.map(
              async (
                result
              ) => {
                try {
                  const pageText =
                    await fetchPageText(
                      result
                    );

                  return (
                    parsed.phrases
                      .every(
                        (
                          phrase
                        ) =>
                          pageText.includes(
                            phrase
                          )
                      )
                      ? result
                      : null
                  );

                } catch (
                  error
                ) {
                  console.warn(
                    "Phrase-search page fetch failed:",
                    error
                  );

                  return null;
                }
              }
            )
          );

        const filteredResults =
          checks.filter(
            (result) =>
              result !== null
          );

        /*
         * Only quoted searches are reordered into book/TOC order.
         */
        const orderedResults =
          orderPhraseResultsByToc(
            filteredResults
          );

        const unquotedHighlightTerms =
          extractHighlightTerms(
            parsed.unquotedQuery
          );

        /*
         * Install highlighting behavior, but DO NOT alter the
         * links generated by Sphinx.
         */
        installResultHighlightHandler(
          parsed.phrases,
          [
            ...unquotedHighlightTerms,
          ]
        );

        /*
         * Search-results-page highlighting.
         */
        const resultHighlightTerms =
          new Set([
            ...[
              ...parsed.phrases,
            ].sort(
              (a, b) =>
                b.length -
                a.length
            ),

            ...unquotedHighlightTerms,
          ]);

        _displayNextItem(
          orderedResults,
          orderedResults.length,
          searchTerms,
          resultHighlightTerms
        );
      };
  }

  /*
   * Install before Search.init() launches the query.
   */
  if (
    document.readyState ===
    "loading"
  ) {
    document.addEventListener(
      "DOMContentLoaded",
      installPhraseSearch
    );
  } else {
    installPhraseSearch();
  }
})();