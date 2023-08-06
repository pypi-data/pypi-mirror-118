from zpy.api.resource import ZResource, HTTP_METHODS


class GreetingResource(ZResource):

    blocked_methods = [
        HTTP_METHODS.POST,
        HTTP_METHODS.DELETE,
        HTTP_METHODS.PATCH,
        HTTP_METHODS.PUT,
    ]

    def __init__(self, **kwargs) -> None:
        super().__init__()

    def get(self):
        l, i = super().new_operation()
        try:
            return self.success({"greeting": "hello world!"}, logger=l)
        except Exception as e:
            return self.handle_exceptions(e, l, i)
