"""Compatibility patch for custom Sphinx nodes in singlehtml builds.

Some HTML themes use a custom translator class that does not inherit the
HTML handlers registered by extensions such as MyST-NB and sphinx-proof.
This copies all registered HTML node handlers onto the active translator.
"""

from __future__ import annotations

from sphinx.application import Sphinx


def patch_singlehtml_translator(app: Sphinx) -> None:
    """Install all registered HTML handlers on the active translator."""

    if app.builder.name != "singlehtml":
        return

    translator_class = app.builder.get_translator_class()

    # Extensions normally register their custom-node handlers for the
    # generic "html" output format. Some may register them specifically
    # for "singlehtml", so collect both.
    handlers = dict(
        app.registry.translation_handlers.get("html", {})
    )
    handlers.update(
        app.registry.translation_handlers.get("singlehtml", {})
    )

    for node_name, (visit_function, depart_function) in handlers.items():
        if visit_function is not None:
            setattr(
                translator_class,
                f"visit_{node_name}",
                visit_function,
            )

        if depart_function is not None:
            setattr(
                translator_class,
                f"depart_{node_name}",
                depart_function,
            )


def setup(app: Sphinx):
    # Use a late priority so that the theme and the other extensions have
    # already registered their translator and custom-node handlers.
    app.connect(
        "builder-inited",
        patch_singlehtml_translator,
        priority=999,
    )

    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }