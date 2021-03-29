from rest_framework import mixins


class BaseCreateListDestroyMixin(mixins.CreateModelMixin,
                                 mixins.ListModelMixin,
                                 mixins.DestroyModelMixin):
    pass


class BaseCreateListRetrieveUpdateDestroyMixin(BaseCreateListDestroyMixin,
                                               mixins.UpdateModelMixin,
                                               mixins.RetrieveModelMixin):
    pass
