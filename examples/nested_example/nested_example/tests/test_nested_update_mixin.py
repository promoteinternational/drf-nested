from copy import copy

from django.test import TestCase
from rest_framework.exceptions import ValidationError

from nested_example.serializers import (EmployeeSerializer, CompanySerializer, UserGroupSerializer,
                                        RoleSerializer)


class NestedUpdateMixinTest(TestCase):
    def test_update_direct_nested(self):
        employee = EmployeeSerializer(
            data={"user": {"username": "Some user name"},
                  "status": "Some status"}
        )
        employee.is_valid()
        employee.save()
        self.assertIsNotNone(employee.instance)
        self.assertIsNotNone(employee.instance.user)

        data = copy(employee.data)
        self.assertIsNotNone(data.get('user'))
        self.assertEqual(data['user'].get('username'), "Some user name")

        data["user"]["username"] = "New user name"

        updated_employee = EmployeeSerializer(
            instance=employee.instance,
            data=data
        )
        updated_employee.is_valid()
        updated_employee.save()
        self.assertIsNotNone(updated_employee.instance)
        self.assertIsNotNone(updated_employee.instance.user)

        data = copy(updated_employee.data)
        self.assertIsNotNone(data.get('user'))
        self.assertEqual(data['user'].get('username'), "New user name")

    def test_update_direct_nested_empty(self):
        employee = EmployeeSerializer(
            data={"user": {"username": "Some user name"},
                  "status": "Some status"}
        )
        employee.is_valid()
        employee.save()
        self.assertIsNotNone(employee.instance)
        self.assertIsNotNone(employee.instance.user)

        data = copy(employee.data)
        self.assertIsNotNone(data.get('user'))
        self.assertEqual(data['user'].get('username'), "Some user name")

        data["user"] = None

        updated_employee = EmployeeSerializer(
            instance=employee.instance,
            data=data
        )
        updated_employee.is_valid()
        updated_employee.save()
        updated_employee.instance.refresh_from_db()
        self.assertIsNotNone(updated_employee.instance)
        self.assertIsNone(updated_employee.instance.user)

    def test_update_reverse_nested(self):
        user = UserGroupSerializer(
            data={"username": "Some user name",
                  "groups": [{"name": "First group"}]})
        user.is_valid()
        user.save()
        self.assertIsNotNone(user.instance)
        data = copy(user.data)
        self.assertEqual(len(data.get('groups')), 1)
        self.assertEqual(data['groups'][0]["name"], "First group")

        data['groups'][0]["name"] = "Still first name"

        updated_user = UserGroupSerializer(
            instance=user.instance,
            data=data
        )
        updated_user.is_valid()
        updated_user.save()
        self.assertIsNotNone(user.instance)
        data = copy(user.data)
        self.assertEqual(len(data.get('groups')), 1)
        self.assertEqual(data['groups'][0]["name"], "Still first name")

    def test_update_reverse_nested_empty(self):
        user = UserGroupSerializer(
            data={"username": "Some user name",
                  "groups": [{"name": "First group"}]})
        user.is_valid()
        user.save()
        self.assertIsNotNone(user.instance)
        data = copy(user.data)
        self.assertEqual(len(data.get('groups')), 1)
        self.assertEqual(data['groups'][0]["name"], "First group")

        data['groups'] = []

        updated_user = UserGroupSerializer(
            instance=user.instance,
            data=data,
        )
        updated_user.is_valid()
        updated_user.save()
        self.assertIsNotNone(user.instance)
        self.assertEqual(data.get('groups'), [])
        self.assertEqual(user.instance.groups.count(), 0)

    def test_update_many_to_many_nested(self):
        company = CompanySerializer(
            data={"name": "Company name",
                  "managers": [{"user": {"username": "Some user name"},
                                "level": "high"}]}
        )
        company.is_valid()
        company.save()
        self.assertIsNotNone(company.instance)
        data = copy(company.data)
        self.assertEqual(len(data.get('managers')), 1)
        self.assertEqual(data.get('managers')[0]["level"], "high")
        self.assertEqual(data.get('managers')[0]["user"]["username"], "Some user name")

        data["managers"][0]["level"] = "low"
        data["managers"][0]["user"]["username"] = "Another username"

        updated_company = CompanySerializer(
            instance=company.instance,
            data=data
        )
        updated_company.is_valid()
        updated_company.save()
        self.assertIsNotNone(updated_company.instance)
        self.assertEqual(len(data.get('managers')), 1)
        self.assertEqual(data.get('managers')[0]["level"], "low")
        self.assertEqual(data.get('managers')[0]["user"]["username"], "Another username")

    def test_update_many_to_many_nested_empty(self):
        company = CompanySerializer(
            data={"name": "Company name",
                  "managers": [{"user": {"username": "Some user name"},
                                "level": "high"}]}
        )
        company.is_valid()
        company.save()
        self.assertIsNotNone(company.instance)
        data = copy(company.data)
        self.assertEqual(len(data.get('managers')), 1)
        self.assertEqual(data.get('managers')[0]["level"], "high")
        self.assertEqual(data.get('managers')[0]["user"]["username"], "Some user name")

        data["managers"] = None

        updated_company = CompanySerializer(
            instance=company.instance,
            data=data
        )
        with self.assertRaises(ValidationError):
            updated_company.is_valid(raise_exception=True)

    def test_update_many_to_many_nested_with_through(self):
        role = RoleSerializer(data={"permission": "high",
                                    "name": "admin"})
        role.is_valid()
        role.save()
        employee = EmployeeSerializer(
            data={"user": {"username": "Some user name"},
                  "status": "Some status"}
        )
        employee.is_valid()
        employee.save()

        data = copy(role.data)

        data.update({
            "employees": [{
                "employee_id": employee.instance.id,
                "role_id": role.instance.id,
                "name": "Some Name"
            }]
        })

        employee_role = RoleSerializer(
            instance=role.instance,
            data=data
        )
        employee_role.is_valid()
        employee_role.save()

        self.assertIsNotNone(employee_role.instance)

        data = copy(employee_role.data)
        self.assertEqual(len(data.get('employees')), 1)

    def test_update_generic_relation_nested(self):
        company = CompanySerializer(
            data={"name": "Company name",
                  "comments": [{"text": "Some comment text"}]}
        )
        company.is_valid()
        company.save()
        self.assertIsNotNone(company.instance)
        data = copy(company.data)
        self.assertEqual(len(data.get('comments')), 1)
        self.assertEqual(data.get('comments')[0]["text"], "Some comment text")

        data["comments"][0]["text"] = "Another text"

        updated_company = CompanySerializer(
            instance=company.instance,
            data=data
        )
        updated_company.is_valid()
        updated_company.save()
        self.assertIsNotNone(updated_company.instance)

        data = copy(company.data)
        self.assertEqual(len(data.get('comments')), 1)
        self.assertEqual(data.get('comments')[0]["text"], "Another text")
