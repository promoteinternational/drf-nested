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
    user = models.ForeignKey("nested_example.User", related_name="employees", on_delete=models.CASCADE,
                             null=True, blank=True)


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
