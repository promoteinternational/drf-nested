from typing import List, Tuple

from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty
from rest_framework.validators import UniqueTogetherValidator


class UniqueTogetherMixin(serializers.ModelSerializer):
    """
    Extracts unique together validators for every field.
    The validators are being run on `create`/`update` instead of `is_valid`
    """
    _unique_together_validators: List[Tuple[str]] = []

    def __init__(self, instance=None, data=empty, **kwargs):
        for validator in self.validators:
            if self._is_unique_together_validator(validator):
                self._unique_together_validators.append(validator.fields)
        self.validators = [validator for validator in self.validators
                           if not self._is_unique_together_validator(validator)]
        super().__init__(instance, data, **kwargs)

    def _is_unique_together_validator(self, validator):
        return isinstance(validator, UniqueTogetherValidator)

    def _validate_unique_together_instance(self, validated_data):
        for fields in self._unique_together_validators:
            unique_together_validator = UniqueTogetherValidator(self.Meta.model.objects.all(),
                                                                fields)
            unique_together_validator.set_context(self)
            try:
                unique_together_validator(validated_data)
            except ValidationError as exc:
                raise ValidationError({"non_field_errors": exc.detail})

    def _validate_unique_together(self, validated_data):
        # It is possible that instance set for the nested serializer is a QuerySet
        # In that case we run validation for each item on the list individually
        if isinstance(self.instance, QuerySet):
            queryset = self.instance
            for item in self.instance.all():
                self.instance = item
                self._validate_unique_together_instance(validated_data)
            self.instance = queryset
        else:
            self._validate_unique_together_instance(validated_data)

    def create(self, validated_data):
        self._validate_unique_together(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self._validate_unique_together(validated_data)
        return super().update(instance, validated_data)
