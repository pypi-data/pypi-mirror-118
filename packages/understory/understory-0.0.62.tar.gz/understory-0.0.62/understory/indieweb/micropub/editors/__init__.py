"""Micropub editors."""

from understory import web

text = web.application(
    "TextEditor",
    mount_prefix="editors/text",
    db=False,
)
photo = web.application(
    "PhotoEditor",
    mount_prefix="editors/photo",
    db=False,
)
templates = web.templates(__name__)


@text.route(r"")
class TextEditor:
    """."""

    def get(self):
        return templates.editors.text(get_config())


@photo.route(r"")
class PhotoEditor:
    """."""

    def get(self):
        return templates.editors.photo(get_config())
