from django.db.models import QuerySet

from drf_nested.mixins.base_nestable_mixin import BaseNestableMixin


def nested_validate(validate):
    def wrapped(self: BaseNestableMixin, data):
        with QuerySetInstanceManager(self, data):
            return validate(self, data)
    return wrapped


def nested_update(update):
    def wrapped(self: BaseNestableMixin, instance, validated_data):
        with QuerySetInstanceManager(self, validated_data):
            return update(self, instance, validated_data)
    return wrapped


class QuerySetInstanceManager:
    def __init__(self, serializer_instance: BaseNestableMixin, validated_data: dict):
        self.serializer_instance = serializer_instance
        self.validated_data = validated_data

    def __enter__(self):
        self.original_instance = self.serializer_instance.instance
        if self.serializer_instance.instance and isinstance(self.serializer_instance.instance, QuerySet):
            self.serializer_instance._set_instance(self.validated_data,
                                                   self.original_instance)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.serializer_instance.instance = self.original_instance
