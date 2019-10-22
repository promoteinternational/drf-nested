from typing import Optional

from rest_framework.fields import empty

from drf_nested.mixins.base_nestable_mixin import BaseNestableMixin
from drf_nested.utils.queryset_to_instance import nested_validate, nested_update


class NestableMixin(BaseNestableMixin):
    write_source: Optional[str] = None

    def __init__(self, instance=None, data=empty, **kwargs):
        if 'write_source' in kwargs:
            self.write_source = kwargs.pop('write_source')

        super().__init__(instance, data, **kwargs)

    @nested_validate
    def validate(self, data):
        return super().validate(data)

    @nested_update
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
