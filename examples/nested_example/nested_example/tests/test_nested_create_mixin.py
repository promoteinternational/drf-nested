from django.test import TestCase
from rest_framework.exceptions import ValidationError, ErrorDetail

from nested_example.serializers import EmployeeSerializer, CompanySerializer, UserGroupSerializer


class NestedCreateMixinTest(TestCase):
    def test_create_direct_nested_success(self):
        employee = EmployeeSerializer(
            data={"user": {"username": "Some name"},
                  "status": "Some status"}
        )
        employee.is_valid(raise_exception=True)
        employee.save()
        self.assertIsNotNone(employee.instance)
        self.assertIsNotNone(employee.instance.user)

    def test_create_direct_nested_fail(self):
        employee = EmployeeSerializer(
            data={"user": {"username": "Some name",
                           "is_active": False},
                  "status": "Some status"}
        )
        employee.is_valid(raise_exception=True)
        with self.assertRaises(ValidationError) as verror:
            employee.save()

        error = verror.exception
        self.assertIn("user", error.detail)
        self.assertEqual(
            error.detail["user"],
            {'is_active': [ErrorDetail(string="User should be active", code='invalid')]}
        )

    def test_create_reverse_nested_success(self):
        user = UserGroupSerializer(
            data={"username": "Some name",
                  "groups": [{"name": "First name"},
                             {"name": "Some name"}]})
        user.is_valid(raise_exception=True)
        user.save()
        self.assertIsNotNone(user.instance)
        data = user.data
        self.assertEqual(len(data.get('groups')), 2)

    def test_create_reverse_nested_fail(self):
        user = UserGroupSerializer(
            data={"username": "Some user name",
                  "groups": [{"name": "Other group name"},
                             {"name": "Secondname"}]})
        with self.assertRaises(ValidationError) as verror:
            user.is_valid(raise_exception=True)

        error = verror.exception
        self.assertIn("groups", error.detail)
        self.assertEqual(error.detail["groups"], [
            {'name': [ErrorDetail(string="Name shouldn't be greater than 10 symbols", code='invalid')]},
            {}
        ])

    def test_create_many_to_many_nested_success(self):
        company = CompanySerializer(
            data={"name": "Company name",
                  "managers": [{"user": {"username": "Some user name"},
                                "level": "high"}]}
        )
        company.is_valid(raise_exception=True)
        company.save()
        self.assertIsNotNone(company.instance)
        data = company.data
        self.assertEqual(len(data.get('managers')), 1)
        self.assertEqual(data.get('managers')[0]["user"]["username"], "Some user name")

    def test_create_many_to_many_nested_fail(self):
        company = CompanySerializer(
            data={"name": "Company name",
                  "managers": [{"user": {"username": "Some user name with username greater 20"},
                                "level": "high"}]}
        )
        with self.assertRaises(ValidationError) as verror:
            company.is_valid(raise_exception=True)

        error = verror.exception
        self.assertIn("managers", error.detail)
        self.assertEqual(len(error.detail["managers"]), 1)
        self.assertIn("user", error.detail["managers"][0])
        self.assertEqual(error.detail["managers"][0]["user"],
                         {'username': [
                             ErrorDetail(string="Username shouldn't be greater than 20 symbols", code='invalid')]},
                         )

        company = CompanySerializer(
            data={"name": "Company name",
                  "managers": [{"user": {"username": "Some name"},
                                "level": "super high"}]}
        )
        company.is_valid(raise_exception=True)
        with self.assertRaises(ValidationError) as verror:
            company.save()

        error = verror.exception
        self.assertIn("managers", error.detail)
        self.assertEqual(len(error.detail["managers"]), 1)
        self.assertIn("level", error.detail["managers"][0])
        self.assertEqual(error.detail["managers"][0]["level"],
                         [ErrorDetail(string="Level shouldn't be super high", code='invalid')],
                         )

    def test_create_generic_relation_nested_success(self):
        company = CompanySerializer(
            data={"name": "Company name",
                  "comments": [{"text": "Some comment text"}]}
        )
        company.is_valid(raise_exception=True)
        company.save()
        self.assertIsNotNone(company.instance)
        data = company.data
        self.assertEqual(len(data.get('comments')), 1)

    def test_create_generic_relation_nested_fail(self):
        company = CompanySerializer(
            data={"name": "Company name",
                  "comments": [{"text": "Some comment text with len greater 20"}]}
        )
        company.is_valid(raise_exception=True)
        with self.assertRaises(ValidationError) as verror:
            company.save()

        error = verror.exception
        self.assertIn("comments", error.detail)
        self.assertEqual(len(error.detail["comments"]), 1)
        self.assertIn("text", error.detail["comments"][0])
        self.assertEqual(error.detail["comments"][0],
                         {'text': [
                             ErrorDetail(string="Text shouldn't be greater than 20 symbols", code='invalid')]},
                         )

        company = CompanySerializer(
            data={"name": "Company name",
                  "comments": [{"text": "Some comment text with len greater 20"},
                               {"text": "Some comment text with len greater 20"}]}
        )
        company.is_valid(raise_exception=True)
        with self.assertRaises(ValidationError) as verror:
            company.save()

        error = verror.exception
        self.assertIn("comments", error.detail)
        self.assertEqual(len(error.detail["comments"]), 2)
        self.assertIn("text", error.detail["comments"][0])
        self.assertEqual(error.detail["comments"][0],
                         {'text': [
                             ErrorDetail(string="Text shouldn't be greater than 20 symbols", code='invalid')]},
                         )
