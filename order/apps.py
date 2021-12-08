from django.apps import AppConfig


class OrderConfig(AppConfig):
    name = 'order'
    verbose_name = ('order')

    def ready(self):
        import order.signals  # noqa
