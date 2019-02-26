from rest_framework import serializers
from drf_nested.mixins.nestable_mixin import NestableMixin

from .models import User, Group, Manager, Employee, EmployeeRole, Role, Company


class UserSerializer(NestableMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    members = UserSerializer(required=False, many=True, source="active_users",
                             write_source="members")

    class Meta:
        model = Group
        fields = ('name', 'members',)


class ManagerSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Manager
        fields = ('user',)


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employee
        fields = ('user',)


class EmployeeRoleSerializer(serializers.HyperlinkedModelSerializer):
    employee_id = serializers.IntegerField()
    role_id = serializers.IntegerField()

    class Meta:
        model = EmployeeRole
        fields = ('employee_id', 'role_id', 'name')


class RoleSerializer(serializers.HyperlinkedModelSerializer):
    employees = EmployeeRoleSerializer(many=True, required=False)

    class Meta:
        model = Role
        fields = ('employees', 'permission', 'name')


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    managers = ManagerSerializer(many=True, required=False)

    class Meta:
        model = Company
