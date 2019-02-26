from django.test import TestCase

from nested_example.serializers import EmployeeSerializer, CompanySerializer, UserGroupSerializer


class NestedCreateMixinTest(TestCase):
    def test_create_direct_nested(self):
        employee = EmployeeSerializer(
            data={"user": {"username": "Some user name"},
                  "status": "Some status"}
        )
        employee.is_valid()
        employee.save()
        self.assertIsNotNone(employee.instance)
        self.assertIsNotNone(employee.instance.user)

    def test_create_reverse_nested(self):
        user = UserGroupSerializer(
            data={"username": "Some user name",
                  "groups": [{"name": "First group"},
                             {"name": "Second group"}]})
        user.is_valid()
        user.save()
        self.assertIsNotNone(user.instance)
        data = user.data
        self.assertEqual(len(data.get('groups')), 2)

    def test_create_many_to_many_nested(self):
        company = CompanySerializer(
            data={"name": "Company name",
                  "managers": [{"user": {"username": "Some user name"},
                                "level": "high"}]}
        )
        company.is_valid()
        company.save()
        self.assertIsNotNone(company.instance)
        data = company.data
        self.assertEqual(len(data.get('managers')), 1)
        self.assertEqual(data.get('managers')[0]["user"]["username"], "Some user name")

    def test_create_generic_relation_nested(self):
        company = CompanySerializer(
            data={"name": "Company name",
                  "comments": [{"text": "Some comment text"}]}
        )
        company.is_valid()
        company.save()
        self.assertIsNotNone(company.instance)
        data = company.data
        self.assertEqual(len(data.get('comments')), 1)
