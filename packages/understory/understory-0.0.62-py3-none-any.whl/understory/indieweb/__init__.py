"""Mountable IndieWeb apps and helper functions."""

from understory import kv, mm, sql, web
from understory.web import framework as fw
from understory.web import tx

from . import indieauth, micropub, microsub, webmention, websub
from .indieauth.server import get_card

__all__ = [
    "indieauth",
    "micropub",
    "microsub",
    "webmention",
    "websub",
    "content",
    "cache",
]

content = fw.application(
    "Content",
    db=False,
    year=r"\d{4}",
    month=r"\d{2}",
    day=r"\d{2}",
    post=web.nb60_re + r"{,4}",
    slug=r"[\w_-]+",
)
about = web.application("About", mount_prefix="about", db=False)
people = fw.application("People", mount_prefix="people", db=False)
cache = fw.application("Cache", mount_prefix="admin/cache", db=False, resource=r".+")
templates = mm.templates(__name__)


def site(name: str, host: str = None, port: int = None) -> web.Application:
    def set_data_sources(handler, app):
        host = tx.request.uri.host  # TODO FIXME check for filename safety!!
        db = sql.db(f"{host}.db")
        tx.host.db = db
        tx.host.cache = web.cache(db=db)
        tx.host.kv = kv.db(host, ":", {"jobs": "list"})
        yield
        # TODO XXX if tx.request.uri.path == "" and tx.response.body:
        # TODO XXX     doc = web.parse(tx.response.body)
        # TODO XXX     try:
        # TODO XXX         head = doc.select("head")[0]
        # TODO XXX     except IndexError:
        # TODO XXX         tx.response.body = (
        # TODO XXX             f"<!doctype html><head></head>"
        # TODO XXX             f"<body>{tx.response.body}</body></html>"
        # TODO XXX         )

    return web.application(
        name,
        host=host,
        port=port,
        mounts=(
            web.framework.data_app,
            web.framework.debug_app,
            indieauth.server.app,
            indieauth.client.app,
            micropub.server,
            micropub.editors.text,
            micropub.editors.photo,
            webmention.receiver,
            about,
            people,
            content,
        ),
        wrappers=(
            set_data_sources,
            web.resume_session,
            indieauth.server.wrap,
            indieauth.client.wrap,
            micropub.wrap_server,
            webmention.wrap_receiver,
        ),
    )


@about.route(r"")
class About:
    """"""

    def get(self):
        return templates.about.index(get_card(), tx.pub.get_posts())


@about.route(r"editor")
class AboutEditor:
    """"""

    def get(self):
        return templates.about.editor(get_card(), tx.pub.get_posts())

    def post(self):
        if not tx.user.is_owner:
            raise web.Unauthorized("must be owner")
        try:
            self.set_name(web.form("name").name)
        except web.BadRequest:
            pass
        try:
            self.set_note(web.form("note").note)
        except web.BadRequest:
            pass
        try:
            self.set_github(web.form("github").github)
        except web.BadRequest:
            pass
        try:
            self.set_twitter(web.form("twitter").twitter)
        except web.BadRequest:
            pass
        try:
            self.set_skills(web.form("skills").skills)
        except web.BadRequest:
            pass
        return "saved"

    def set_name(self, name):
        card = get_card()
        card.update(name=[name])
        tx.db.update("identities", card=card)

    def set_note(self, note):
        card = get_card()
        card["note"] = [note]
        tx.db.update("identities", card=card)

    def set_github(self, name):
        card = get_card()
        card["url"].append(f"https://github.com/{name}")
        tx.db.update("identities", card=card)

    def set_twitter(self, name):
        card = get_card()
        card["url"].append(f"https://twitter.com/{name}")
        tx.db.update("identities", card=card)

    def set_skills(self, skills):
        resume = get_resume()
        if resume is None:
            resume = {}
        resume.update(skills=skills.split())
        tx.db.update("identities", resume=resume)


@people.route(r"")
class People:
    def get(self):
        return templates.people.index(
            indieauth.server.get_clients(), indieauth.client.get_users()
        )


@content.route(r"")
class Homepage:
    """Your name, avatar and one or more streams of posts."""

    def get(self):
        # resource = tx.pub.read(tx.request.uri.path)["resource"]
        # if resource["visibility"] == "private" and not tx.user.session:
        #     raise web.Unauthorized(f"/auth?return_to={tx.request.uri.path}")
        # # mentions = web.indie.webmention.get_mentions(str(tx.request.uri))
        # return templates.content.entry(resource)  # , mentions)
        return templates.content.homepage(
            get_card(),  # TODO tx.auth.get_card
            tx.pub.get_posts(),
        )


# XXX @content.route(r"understory.js")
# XXX class UnderstoryJS:
# XXX     def get(self):
# XXX         web.header("Content-Type", "application/javascript")
# XXX         with (pathlib.Path(__file__).parent / "understory.js").open() as fp:
# XXX             return fp.read()


@content.route(r"{year}/{month}/{day}/{post}(/{slug})?")
class Permalink:
    """An individual entry."""

    def get(self):
        resource = tx.pub.read(tx.request.uri.path)["resource"]
        if resource["visibility"] == "private" and not tx.user.session:
            raise web.Unauthorized(f"/auth?return_to={tx.request.uri.path}")
        # mentions = web.indie.webmention.get_mentions(str(tx.request.uri))
        return templates.content.entry(resource)  # , mentions)


@cache.route(r"")
class Cache:
    def get(self):
        return templates.cache.index(fw.tx.db.select("cache"))


@cache.route(r"{resource}")
class Resource:
    """"""

    resource = None

    def get(self):
        resource = fw.tx.db.select(
            "cache",
            where="url = ? OR url = ?",
            vals=[f"https://{self.resource}", f"http://{self.resource}"],
        )[0]
        return templates.cache.resource(resource)
