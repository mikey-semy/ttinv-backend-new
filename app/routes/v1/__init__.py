from app.routes.base import BaseRouter
from app.routes.v1.header import HeaderRouter


class APIv1(BaseRouter):
    def configure_routes(self):
        self.router.include_router(HeaderRouter().get_router())
