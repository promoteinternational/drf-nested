## DRF Nested Utils

[![pypi package](https://img.shields.io/pypi/v/drf-nested.svg)](https://pypi.org/project/drf-nested/)

This package provides a set of utils to help developers implement nested data handling for Django Rest Framework.

This package adds support for:
* Direct relation handling (`ForeignKey`)
* Reverse relation handling (i.e. allows working with models that have current as `ForeignKey`)
* Direct and reverse `ManyToMany`, with special flow for the m2m relationships with custom `through` models
* `GenericRelation` with special mixins

It also provides mixins for handling `Unique` and `UniqueTogether` validators.

## Examples

__models.py__

```python
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)


class Comment(models.Model):
    text = models.CharField(max_length=400)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey("contenttypes.ContentType", on_delete=models.CASCADE,
                                     related_name="comments")


class Group(models.Model):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField("nested_example.User", related_name="groups")
    company = models.ForeignKey("nested_example.Company", related_name="groups", on_delete=models.CASCADE,
                                null=True, blank=True)

    @property
    def active_users(self):
        return self.members.filter(is_active=True)


class Employee(models.Model):
    status = models.CharField(max_length=200)
    user = models.ForeignKey("nested_example.User", related_name="employees", on_delete=models.CASCADE)


class Manager(models.Model):
    level = models.CharField(max_length=200)
    user = models.ForeignKey("nested_example.User", related_name="managers", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("level", "user")


class Role(models.Model):
    name = models.CharField(max_length=200)
    permission = models.CharField(max_length=200)
    employees = models.ManyToManyField("nested_example.Employee", related_name="roles",
                                       through="nested_example.EmployeeRole")


class EmployeeRole(models.Model):
    name = models.CharField(max_length=200)
    employee = models.ForeignKey("nested_example.Employee", related_name="employee_roles", on_delete=models.CASCADE)
    role = models.ForeignKey("nested_example.Role", related_name="employee_roles", on_delete=models.CASCADE)


class Company(models.Model):
    name = models.CharField(max_length=200)
    managers = models.ManyToManyField("nested_example.Manager", related_name="companies")
    comments = GenericRelation(Comment, related_name="companies")
```

__serializers.py__
```python
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from drf_nested.mixins import (NestableMixin, CreateNestedMixin, UpdateNestedMixin, GenericRelationMixin,
                               UniqueTogetherMixin)
from .models import User, Group, Manager, Employee, EmployeeRole, Role, Company, Comment


class NestedSerializer(CreateNestedMixin, UpdateNestedMixin):
    pass


class UserSerializer(NestableMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'is_active')


class CommentSerializer(GenericRelationMixin, serializers.HyperlinkedModelSerializer):
    content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all())

    class Meta:
        model = Comment
        fields = ('text', 'object_id', 'content_type', 'content_type_id',)


class GroupSerializer(NestedSerializer, serializers.HyperlinkedModelSerializer):
    members = UserSerializer(required=False, many=True, source="active_users",
                             write_source="members")

    class Meta:
        model = Group
        fields = ('name', 'members',)


class SimpleGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class UserGroupSerializer(NestedSerializer, serializers.HyperlinkedModelSerializer):
    groups = SimpleGroupSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = ('username', 'is_active', "groups")


class ManagerSerializer(UniqueTogetherMixin, CreateNestedMixin, UpdateNestedMixin,
                        serializers.HyperlinkedModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Manager
        fields = ('user', 'level')


class EmployeeSerializer(NestedSerializer, serializers.HyperlinkedModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employee
        fields = ('user', 'status')


class EmployeeRoleSerializer(NestableMixin, serializers.HyperlinkedModelSerializer):
    employee_id = serializers.IntegerField()
    role_id = serializers.IntegerField()

    class Meta:
        model = EmployeeRole
        fields = ('employee_id', 'role_id', 'name')


class RoleSerializer(NestedSerializer, serializers.HyperlinkedModelSerializer):
    employees = EmployeeRoleSerializer(many=True, required=False, write_source="employee_roles",
                                       source="employee_roles")

    class Meta:
        model = Role
        fields = ('employees', 'permission', 'name')


class CompanySerializer(NestedSerializer, serializers.HyperlinkedModelSerializer):
    managers = ManagerSerializer(many=True, required=False)
    comments = CommentSerializer(many=True, required=False)

    class Meta:
        model = Company
        fields = ('managers', 'comments', 'name')
        
```

You can see examples of usage in `examples/` directory.

> Note: If you are using a Many-to-Many field with `source` property or you have a `through` model on your serializer, 
you should add a `NestableMixin` to the target serializer and add a `write_source` field when you initialize that serializer.

> In case of the `source` property you should add an actual model field that would allow you to properly connect your model with related ones. 

> In case of the `through` model you should have it set to the `related_name` of the connected `through` model