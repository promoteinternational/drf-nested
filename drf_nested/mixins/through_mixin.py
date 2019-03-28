from typing import Optional

from rest_framework import serializers
from rest_framework.fields import empty


class ThroughMixin(serializers.ModelSerializer):
    connect_to_model: Optional[bool] = None

    def __init__(self, instance=None, data=empty, **kwargs):
        if 'connect_to_model' in kwargs:
            self.connect_to_model = kwargs.pop('connect_to_model')

        super().__init__(instance, data, **kwargs)
