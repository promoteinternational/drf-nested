from typing import List

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator


class UniqueFieldMixin(serializers.ModelSerializer):
    """
    Extracts unique validators for every field.
    The validators are being run on `create`/`update` instead of `is_valid`
    """
    _unique_validators: List[str] = []

    def _is_unique_validator(self, validator):
        return isinstance(validator, UniqueValidator)

    def _has_unique_validator(self, field_serializer):
        for validator in field_serializer.validators:
            if self._is_unique_validator(validator):
                return True
        return None

    def get_fields(self):
        fields = super().get_fields()
        for field_name, field_serializer in fields.items():
            if self._has_unique_validator(field_serializer):
                self._unique_validators.append(field_name)
            field_serializer.validators = [
                validator for validator in field_serializer.validators
                if not self._is_unique_validator(validator)
            ]
        return fields

    def _validate_unique(self, validated_data):
        for field in self._unique_validators:
            unique_together_validator = UniqueValidator(self.Meta.model.objects.all())
            unique_together_validator.set_context(self.fields[field])
            try:
                unique_together_validator(validated_data[field])
            except ValidationError as exc:
                raise ValidationError({field: exc.detail})

    def create(self, validated_data):
        self._validate_unique(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self._validate_unique(validated_data)
        return super().update(instance,validated_data)
