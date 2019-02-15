from rest_framework import serializers
from rest_framework.fields import empty


class NestableMixin(serializers.ModelSerializer):
    write_source = None

    def __init__(self, instance=None, data=empty, **kwargs):
        if 'write_source' in kwargs:
            self.write_source = kwargs.pop('write_source')

        super().__init__(instance, data, **kwargs)
