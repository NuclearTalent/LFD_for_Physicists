/*
 * phrase-search.js
 *
 * Exact quoted-phrase searching plus persistent result-page highlighting
 * for Jupyter Book 1 / Sphinx 7.4.x.
 *
 * Examples:
 *
 *   statistical model
 *       -> ordinary Sphinx search
 *       -> each result page highlights "statistical" and "model"
 *
 *   "statistical model"
 *       -> only pages containing the exact phrase are returned
 *       -> each result page highlights the whole phrase as a unit
 *
 *   "statistical model" likelihood
 *       -> pages must contain the exact phrase and satisfy the normal
 *          Sphinx search for likelihood
 *       -> the destination page highlights the phrase as a unit and
 *          also highlights likelihood
 *
 * Curly double quotes (“...”) are treated like straight quotes ("...").
 *
 * Phrase filtering fetches candidate HTML pages in the browser, so quoted
 * searches require HTTP/HTTPS (GitHub Pages or a local web server), not file://.
 */

(function () {
  "use strict";

  const PHRASE_PARAM = "phrase-highlight";
  const WORD_PARAM = "word-highlight";

  function normalizeText(text) {
    return text
      .toLowerCase()
      .replace(/\u00ad/g, "")                    // soft hyphen
      .replace(/[\u200b-\u200d\uFEFF]/g, "")    // zero-width characters
      .replace(/\s+/g, " ")
      .trim();
  }

  function escapeRegExp(text) {
    return text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  function parseQuotedPhrases(query) {
    const normalizedQuery = query.replace(/[“”]/g, '"');
    const phrases = [];
    const re = /"([^"]+)"/g;
    let match;

    while ((match = re.exec(normalizedQuery)) !== null) {
      const phrase = normalizeText(match[1]);

      if (phrase) {
        phrases.push(phrase);
      }
    }

    const unquotedQuery = normalizedQuery
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
      document.documentElement.dataset.content_root || "";

    if (DOCUMENTATION_OPTIONS.BUILDER === "dirhtml") {
      let dirname = docName + "/";

      if (dirname.match(/\/index\/$/)) {
        dirname = dirname.substring(0, dirname.length - 6);
      } else if (dirname === "index/") {
        dirname = "";
      }

      return contentRoot + dirname;
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
      // Safe to ignore if localStorage is unavailable.
    }
  }

  /*
   * ----------------------------------------------------------------------
   * Destination-page highlighting
   * ----------------------------------------------------------------------
   */

  function getCustomHighlightsFromCurrentUrl() {
    const url =
      new URL(window.location.href);

    const phrases =
      url.searchParams
        .getAll(PHRASE_PARAM)
        .map(normalizeText)
        .filter(Boolean);

    const words =
      url.searchParams
        .getAll(WORD_PARAM)
        .map(normalizeText)
        .filter(Boolean);

    return {
      phrases,
      words,
    };
  }

  function removeCustomHighlightParamsFromAddressBar() {
    const url =
      new URL(window.location.href);

    if (
      !url.searchParams.has(PHRASE_PARAM) &&
      !url.searchParams.has(WORD_PARAM)
    ) {
      return;
    }

    url.searchParams.delete(
      PHRASE_PARAM
    );

    url.searchParams.delete(
      WORD_PARAM
    );

    window.history.replaceState(
      {},
      "",
      url
    );
  }

  function unwrapExistingHighlights(root) {
    const parents =
      new Set();

    root
      .querySelectorAll(
        "span.highlighted"
      )
      .forEach((span) => {
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
        parents.add(parent);
      });

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
       * Allow arbitrary rendered whitespace between words.
       * Thus "statistical model" also matches text containing
       * a newline or several spaces between the two words.
       */
      const pieces =
        text
          .trim()
          .split(/\s+/)
          .map(escapeRegExp);

      if (!pieces.length) {
        return;
      }

      const pattern =
        new RegExp(
          pieces.join("\\s+"),
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
       * There may be additional occurrences in the remainder
       * of this text node.
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
    /*
     * Don't add another link if the theme/Sphinx already
     * supplied one.
     */
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
      typeof _ === "function"
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
    searchBox.appendChild(p);
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

    /*
     * Remove any built-in Sphinx word highlights that may
     * already have appeared.
     */
    unwrapExistingHighlights(
      root
    );

    /*
     * Highlight complete quoted phrases first.
     * Longest phrases come first in case one phrase contains
     * another.
     */
    [...phrases]
      .sort(
        (a, b) =>
          b.length - a.length
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
     * Then highlight ordinary unquoted search words.
     *
     * highlightTextInNode() skips existing .highlighted spans,
     * so individual words will not break apart a quoted phrase
     * that has already been highlighted as one unit.
     */
    [
      ...new Set(words),
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

    /*
     * The highlighting information no longer needs to remain
     * visible in the address bar after it has been applied.
     */
    removeCustomHighlightParamsFromAddressBar();
  }

  const destinationHighlights =
    getCustomHighlightsFromCurrentUrl();

  if (
    destinationHighlights
      .phrases.length ||
    destinationHighlights
      .words.length
  ) {
    /*
     * Prevent Sphinx's normal one-shot localStorage highlighter
     * from competing with this script's persistent highlighting.
     */
    clearSphinxHighlightStorage();

    if (
      document.readyState ===
      "loading"
    ) {
      document.addEventListener(
        "DOMContentLoaded",
        () => {
          highlightDestinationTerms(
            destinationHighlights
              .phrases,
            destinationHighlights
              .words
          );
        }
      );
    } else {
      highlightDestinationTerms(
        destinationHighlights
          .phrases,
        destinationHighlights
          .words
      );
    }
  }

  /*
   * ----------------------------------------------------------------------
   * Search-result handling
   * ----------------------------------------------------------------------
   */

  function extractHighlightTerms(
    query
  ) {
    const terms =
      new Set();

    if (!query.trim()) {
      return terms;
    }

    /*
     * Mirror Sphinx's rules for which raw query terms are
     * highlighted: omit stopwords and pure numbers.
     */
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

        terms.add(lower);
      }
    );

    return terms;
  }

  function installResultLinkDecorator(
    phrases,
    words
  ) {
    if (!Search.output) {
      return;
    }

    function decorateLink(
      link
    ) {
      if (
        !link ||
        link.dataset
          .phraseSearchDecorated ===
          "true"
      ) {
        return;
      }

      const url =
        new URL(
          link.href,
          window.location.href
        );

      /*
       * Remove stale copies before adding the current search's
       * highlighting information.
       */
      url.searchParams.delete(
        PHRASE_PARAM
      );

      url.searchParams.delete(
        WORD_PARAM
      );

      phrases.forEach(
        (phrase) => {
          url.searchParams.append(
            PHRASE_PARAM,
            phrase
          );
        }
      );

      words.forEach(
        (word) => {
          url.searchParams.append(
            WORD_PARAM,
            word
          );
        }
      );

      link.href =
        url.toString();

      link.dataset
        .phraseSearchDecorated =
        "true";
    }

    function decorateNode(
      node
    ) {
      if (
        node.nodeType !==
        Node.ELEMENT_NODE
      ) {
        return;
      }

      if (
        node.matches("a")
      ) {
        decorateLink(node);
      }

      node
        .querySelectorAll("a")
        .forEach(
          decorateLink
        );
    }

    /*
     * Decorate links that may already exist.
     */
    Search.output
      .querySelectorAll("a")
      .forEach(
        decorateLink
      );

    /*
     * Sphinx inserts result entries asynchronously.
     * Watch for each new result and decorate its link immediately.
     *
     * Doing this at insertion time rather than at click time also
     * makes right-click -> Open Link in New Tab work.
     */
    const observer =
      new MutationObserver(
        (mutations) => {
          mutations.forEach(
            (mutation) => {
              mutation.addedNodes
                .forEach(
                  decorateNode
                );
            }
          );
        }
      );

    observer.observe(
      Search.output,
      {
        childList: true,
        subtree: true,
      }
    );
  }

  /*
   * ----------------------------------------------------------------------
   * Search implementation
   * ----------------------------------------------------------------------
   */

  function installPhraseSearch() {
    /*
     * Search exists only on Sphinx's dedicated search page.
     */
    if (
      typeof Search ===
      "undefined"
    ) {
      return;
    }

    /*
     * Avoid installing twice.
     */
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

                return response.text();
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

      return pageTextCache.get(
        url
      );
    }

    Search.query =
      async function (query) {
        const parsed =
          parseQuotedPhrases(
            query
          );

        /*
         * ------------------------------------------------------
         * Ordinary unquoted search
         * ------------------------------------------------------
         *
         * Use Sphinx's normal parser and normal indexed search.
         * The only change is destination-page highlighting:
         * instead of transient localStorage state, put the terms
         * directly into every result link.
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

          /*
           * _parseQuery() just populated Sphinx's one-shot
           * localStorage highlighting. We don't need it because
           * every result link will carry its own terms.
           */
          clearSphinxHighlightStorage();

          const results =
            Search._performSearch(
              searchQuery,
              searchTerms,
              excludedTerms,
              highlightTerms,
              objectTerms
            );

          /*
           * Add persistent word highlighting information to
           * every result URL.
           */
          installResultLinkDecorator(
            [],
            [...highlightTerms]
          );

          /*
           * Use Sphinx's standard result rendering, including
           * normal highlighting of snippets on the search page.
           */
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
         * First use the Sphinx index to get candidate pages.
         *
         * For example,
         *
         *   "statistical model" likelihood
         *
         * becomes
         *
         *   statistical model likelihood
         *
         * for the indexed candidate search.
         */
        const candidateQuery =
          parsed.normalizedQuery
            .replace(/"/g, " ")
            .replace(/\s+/g, " ")
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

        /*
         * Again, do not use Sphinx's one-shot localStorage state.
         */
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

        /*
         * Fetch each candidate's actual page text and require
         * every quoted phrase to occur exactly after
         * case/whitespace normalization.
         */
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

                  return parsed
                    .phrases
                    .every(
                      (
                        phrase
                      ) =>
                        pageText.includes(
                          phrase
                        )
                    )
                    ? result
                    : null;
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
         * Determine which terms were genuinely outside quotes.
         *
         * Thus for
         *
         *   "statistical model" likelihood
         *
         * the complete phrase is highlighted as one unit and
         * likelihood is highlighted separately.
         */
        const unquotedHighlightTerms =
          extractHighlightTerms(
            parsed.unquotedQuery
          );

        /*
         * Put both phrase and ordinary-word highlighting into
         * every result link.
         */
        installResultLinkDecorator(
          parsed.phrases,
          [
            ...unquotedHighlightTerms,
          ]
        );

        /*
         * On the search-results page itself, highlight complete
         * quoted phrases plus any additional unquoted words.
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

        /*
         * Preserve Sphinx's normal result renderer, result order,
         * snippets, links, and result-count message.
         */
        _displayNextItem(
          filteredResults,
          filteredResults.length,
          searchTerms,
          resultHighlightTerms
        );
      };
  }

  /*
   * Install after Sphinx's searchtools.js has defined Search,
   * but before Search.init() starts the search.
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