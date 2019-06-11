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


class ManagerSerializer(UniqueTogetherMixin, CreateNestedMixin, UpdateNestedMixin,
                        serializers.HyperlinkedModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Manager
        fields = ('user', 'level')


class EmployeeSerializer(NestedSerializer, serializers.HyperlinkedModelSerializer):
    user = UserSerializer(required=False, allow_null=True)

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


class CompanySerializer(NestableMixin, NestedSerializer, serializers.HyperlinkedModelSerializer):
    managers = ManagerSerializer(many=True, required=False)
    comments = CommentSerializer(many=True, required=False)

    class Meta:
        model = Company
        fields = ('managers', 'comments', 'name')


class GroupSerializer(NestedSerializer, serializers.HyperlinkedModelSerializer):
    members = UserSerializer(required=False, many=True, source="active_users",
                             write_source="members")
    company = CompanySerializer(required=False, allow_null=True)

    class Meta:
        model = Group
        fields = ('name', 'members', 'company')


class SimpleGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class UserGroupSerializer(NestedSerializer, serializers.HyperlinkedModelSerializer):
    groups = SimpleGroupSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('username', 'is_active', "groups")
