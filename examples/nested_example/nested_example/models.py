from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50)


class Group(models.Model):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(User, related_name="groups")
    is_active = models.BooleanField(default=False)

    @property
    def active_users(self):
        return self.members.filter(is_active=True)


class Employee(models.Model):
    user = models.ForeignKey(User, related_name="employees", on_delete=models.CASCADE)


class Manager(models.Model):
    user = models.ForeignKey(User, related_name="managers", on_delete=models.CASCADE)


class Role(models.Model):
    name = models.CharField(max_length=200)
    permission = models.CharField(max_length=200)
    employees = models.ManyToManyField(Employee, related_name="roles",
                                       through="nested_example.EmployeeRole")


class EmployeeRole(models.Model):
    name = models.CharField(max_length=200)
    employee = models.ForeignKey(Employee, related_name="employee_roles", on_delete=models.CASCADE)
    role = models.ForeignKey(Role, related_name="employee_roles", on_delete=models.CASCADE)


class Company(models.Model):
    manager = models.ManyToManyField(Manager, related_name="companies")
