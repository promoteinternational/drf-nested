from django.db.models import QuerySet


def nested_validate(validate):
    def wrapped(self, data):
        with QuerySetInstanceManager(self, data):
            return validate(self, data)

    return wrapped


def nested_update(update):
    def wrapped(self, instance, validated_data):
        with QuerySetInstanceManager(self, validated_data):
            return update(self, instance, validated_data)

    return wrapped


def nested_run_validators(run_validators):
    def wrapped(self, value):
        with QuerySetInstanceManager(self, value):
            return run_validators(self, value)

    return wrapped


class QuerySetInstanceManager:
    def __init__(self, serializer_instance, validated_data: dict):
        self.serializer_instance = serializer_instance
        self.validated_data = validated_data

    def __enter__(self):
        self.original_instance = self.serializer_instance.instance
        if self.serializer_instance.instance is not None and isinstance(self.serializer_instance.instance, QuerySet):
            self.serializer_instance._set_instance(self.validated_data,
                                                   self.original_instance)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.serializer_instance.instance = self.original_instance
