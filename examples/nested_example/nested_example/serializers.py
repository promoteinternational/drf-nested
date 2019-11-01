from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from drf_nested.mixins import (NestableMixin, CreateNestedMixin, UpdateNestedMixin, GenericRelationMixin,
                               UniqueTogetherMixin)
from drf_nested.utils.queryset_to_instance import nested_validate
from .models import User, Group, Manager, Employee, EmployeeRole, Role, Company, Comment


class NestedSerializer(CreateNestedMixin, UpdateNestedMixin):
    pass


class UserSerializer(NestableMixin, serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)

    @nested_validate
    def validate(self, attrs):
        username = attrs.get('username')
        if username and len(username) > 20:
            raise ValidationError({"username": ["Username shouldn't be greater than 20 symbols"]})
        return super().validate(attrs)

    def create(self, validated_data):
        if validated_data.get("is_active") is False:
            raise ValidationError({"is_active": ["User should be active"]})
        return super().create(validated_data)

    class Meta:
        model = User
        fields = ('id', 'username', 'is_active')


class CommentSerializer(GenericRelationMixin, serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all())

    def create(self, validated_data):
        if len(validated_data.get("text")) > 20:
            raise ValidationError({"text": ["Text shouldn't be greater than 20 symbols"]})
        return super().create(validated_data)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'object_id', 'content_type', 'content_type_id',)


class ManagerSerializer(UniqueTogetherMixin, CreateNestedMixin, UpdateNestedMixin,
                        serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    user = UserSerializer()

    def create(self, validated_data):
        if validated_data.get("level") == "super high":
            raise ValidationError({"level": ["Level shouldn't be super high"]})
        return super().create(validated_data)

    class Meta:
        model = Manager
        fields = ('id', 'user', 'level')


class EmployeeSerializer(NestedSerializer, serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    user = UserSerializer(required=False, allow_null=True)

    class Meta:
        model = Employee
        fields = ('id', 'user', 'status')


class EmployeeRoleSerializer(NestableMixin, serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    employee_id = serializers.IntegerField()
    role_id = serializers.IntegerField()

    class Meta:
        model = EmployeeRole
        fields = ('id', 'employee_id', 'role_id', 'name')


class RoleSerializer(NestedSerializer, serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    employees = EmployeeRoleSerializer(many=True, required=False, write_source="employee_roles",
                                       source="employee_roles")

    class Meta:
        model = Role
        fields = ('id', 'employees', 'permission', 'name')


class CompanySerializer(NestableMixin, NestedSerializer, serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    managers = ManagerSerializer(many=True, required=False)
    comments = CommentSerializer(many=True, required=False)

    class Meta:
        model = Company
        fields = ('id', 'managers', 'comments', 'name')


class GroupSerializer(NestedSerializer, serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    members = UserSerializer(required=False, many=True, source="active_users",
                             write_source="members")
    company = CompanySerializer(required=False, allow_null=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'members', 'company')


class SimpleGroupSerializer(NestableMixin, serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)

    @nested_validate
    def validate(self, attrs):
        name = attrs.get('name')
        if name and len(name) > 10:
            raise ValidationError({"name": ["Name shouldn't be greater than 10 symbols"]})
        return super().validate(attrs)

    class Meta:
        model = Group
        fields = ('id', 'name',)


class UserGroupSerializer(NestedSerializer, serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    groups = SimpleGroupSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'is_active', "groups")
