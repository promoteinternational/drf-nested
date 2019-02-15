from django.db import transaction

from .base_nested_mixin import BaseNestedMixin


class UpdateNestedMixin(BaseNestedMixin):
    @transaction.atomic
    def update(self, instance, validated_data):
        """
        :param instance:
        :param validated_data:
        :return:
        """
        if self._has_nested_fields(validated_data):
            validated_data, nested_fields_data = self._get_nested_fields(validated_data, remove_fields=True)

            nested_field_types = self.extract_nested_types(nested_fields_data)

            for field in nested_field_types["direct_relations"]:
                field_name = field.get('name')
                field_data = field.get('data')
                if isinstance(field_data, dict):
                    nested_instance = self._update_or_create_direct_relations(field_name, field.get('data'))
                    validated_data[field.get("original_name")] = nested_instance

            model_instance = super().update(instance, validated_data)

            for field in nested_field_types["reverse_relations"]:
                self._update_or_create_reverse_relation(field.get('name'), field.get('data'), model_instance)
            for field in nested_field_types["generic_relations"]:
                self._update_or_create_generic_relation(field.get('name'), field.get('data'), model_instance)
            for field in nested_field_types["many_to_many_fields"]:
                self._update_or_create_many_to_many_field(field.get('name'), field.get('data'), model_instance)
        else:
            model_instance = super().update(instance, validated_data)

        model_instance.refresh_from_db()

        return model_instance
