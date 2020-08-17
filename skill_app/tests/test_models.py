from django.test import SimpleTestCase, TestCase
from skill_app.models import SkillModel, RoleModel


class TestRoleModel(TestCase):
    def test_create_role(self):
        RoleModel.objects.create(name="Title", slug="title")
