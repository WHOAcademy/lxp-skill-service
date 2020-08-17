from django.test import SimpleTestCase, TestCase
from skill_app.models import SkillModel, RoleModel


class TestRoleModel(TestCase):
    def test_create_role(self):
        RoleModel.objects.create(name="Title", slug="title")

    def test_get_all(self):
        RoleModel.objects.create(title="Title1", slug="title-1")
        RoleModel.objects.create(title="Title2", slug="title-2")
        RoleModel.objects.create(title="Title3", slug="title-3")

        courses = RoleModel.objects.all()
        self.assertEqual(len(courses), 3)