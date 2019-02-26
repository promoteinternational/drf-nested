from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from drf_nested.mixins import (NestableMixin, CreateNestedMixin, UpdateNestedMixin, GenericRelationMixin,
                               UniqueTogetherMixin)
from .models import User, Group, Manager, Employee, EmployeeRole, Role, Company, Comment


class UserSerializer(NestableMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'is_active')


class CommentSerializer(GenericRelationMixin, serializers.HyperlinkedModelSerializer):
    content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all())

    class Meta:
        model = Comment
        fields = ('text', 'object_id', 'content_type', 'content_type_id',)


class GroupSerializer(CreateNestedMixin, UpdateNestedMixin, serializers.HyperlinkedModelSerializer):
    members = UserSerializer(required=False, many=True, source="active_users",
                             write_source="members")

    class Meta:
        model = Group
        fields = ('name', 'members',)


class SimpleGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class UserGroupSerializer(CreateNestedMixin, UpdateNestedMixin, serializers.HyperlinkedModelSerializer):
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


class EmployeeSerializer(CreateNestedMixin, UpdateNestedMixin, serializers.HyperlinkedModelSerializer):
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


class RoleSerializer(CreateNestedMixin, UpdateNestedMixin, serializers.HyperlinkedModelSerializer):
    employees = EmployeeRoleSerializer(many=True, required=False, write_source="employee_roles",
                                       source="employee_roles")

    class Meta:
        model = Role
        fields = ('employees', 'permission', 'name')


class CompanySerializer(CreateNestedMixin, UpdateNestedMixin, serializers.HyperlinkedModelSerializer):
    managers = ManagerSerializer(many=True, required=False)
    comments = CommentSerializer(many=True, required=False)

    class Meta:
        model = Company
        fields = ('managers', 'comments', 'name')
