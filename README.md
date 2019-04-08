## DRF Nested Utils

[![pypi package](https://img.shields.io/pypi/v/drf-nested.svg)](https://pypi.org/project/drf-nested/)

This package provides a set of utils to help developers implement nested data handling for Django Rest Framework.

This package adds support for:
* Direct relation handling (`ForeignKey`)
* Reverse relation handling (i.e. allows working with models that have current as `ForeignKey`)
* Direct and reverse `ManyToMany`, with special flow for the m2m relationships with custom `through` models
* `GenericRelation` with special mixins

It also provides mixins for handling `Unique` and `UniqueTogether` validators.

## Mixins

### Nested Serializer Mixins

#### `BaseNestedMixin`

Base mixin that contains the methods for retrieval of all related fields of the serializer model. 
It also provides all the `update_or_create` methods for each type of fields 
(`direct relation`, `reverse relation`, `many-to-many relation` and `generic relation`).

#### `CreateNestedMixin`

Mixin that allows creation of the nested models on serializer `create` call. 
You can provide a list of fields that should be forbidden on create, 
the list of fields should be placed into the `forbidden_on_create` 
field on serializer `Meta` class.
Mixin uses `BaseNestedMixin` properties and `update_and_create` methods to create nested fields.

#### `UpdateNestedMixin`

Mixin that allows modification of the nested models on serializer `update` call.
Mixin uses `BaseNestedMixin` properties and `update_and_create` methods to update nested fields.

### Validator Mixins

#### `UniqueFieldMixin`

Mixin that allows usage of the `unique` fields with nested mixins. 
This mixin moves the validation process from `is_valid` to `create/update` call. 
This is done because the fields that should be used in the `unique` validation may not be 
set on the initial `is_valid` call and are set just before the nested `create/update` call. 

#### `UniqueTogetherMixin`

Mixin that allows usage of the `unique_together` fields with nested mixins. 
This mixin moves the validation process from `is_valid` to `create/update` call. 
This is done because the fields that should be used in the `unique_together` validation may not be 
set on the initial `is_valid` call and are set just before the nested `create/update` call.

### Helper Mixins

#### `NestableMixin`

Mixin that allows to specify the name of the nested field by setting `write_source` if the initial `source` of the field is different 
from the field name or the initial `source` is not writable (a property, for example).

#### `ThroughMixin`

Mixin that allows to specify if `through` model should be connected to current model after the `through` model `create/update` call.

#### `GenericRelationMixin`

Mixin that should be used on serializers that represent connected by `GenericRelation` models.

## Examples

You can see an example project in `examples/` directory.

## Notes

> If you are using a Many-to-Many field with `source` property or you have a `through` model on your serializer, 
you should add a `NestableMixin` to the target serializer and add a `write_source` field when you initialize that serializer.

> In case of the `source` property you should add an actual model field that would allow you to properly connect your model with related ones. 

> In case of the `through` model you should have it set to the `related_name` of the connected `through` model

> You can also use `ThroughMixin` and set `connect_to_model` to False if you want to have the ability to keep the `through` model connection in case the `through` model ForeignKey should be different from the current model.