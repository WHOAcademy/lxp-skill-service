from django.db import DataError
from django.test import SimpleTestCase, TestCase
from skill_app.models import SkillModel, RoleModel


class TestRoleModel(TestCase):

    def test_create_role(self):
        RoleModel.objects.create(name="Title", slug="title")

    def test_get_all(self):
        RoleModel.objects.create(name="Title1", slug="title-1")
        RoleModel.objects.create(name="Title2", slug="title-2")
        RoleModel.objects.create(name="Title3", slug="title-3")

        roles = RoleModel.objects.all()
        self.assertEqual(len(roles), 3)

    def test_role_obj(self):
        RoleModel.objects.create(name="Title", slug="title")
        role = RoleModel.objects.all()[0]
        self.assertTrue(isinstance(role, RoleModel))
        self.assertEqual(role.name, "Title")
        self.assertEqual(role.slug, "title")

    def test_name_max_length(self):
        with self.assertRaises(DataError):
            title = "This is a test This is a test This is a test This is a test "
            RoleModel.objects.create(name=title, slug="title")

    def test_slug_max_length(self):
        with self.assertRaises(DataError):
            slug = "This is a test This is a test This is a test This is a test This is a test "
            RoleModel.objects.create(name="Title", slug=slug)

    def test_name_unique(self):
        with self.assertRaises(DataError):
            RoleModel.objects.create(name="Title", slug="title-1")
            RoleModel.objects.create(name="Title", slug="title-2")

    def test_slug_unique(self):
        with self.assertRaises(DataError):
            RoleModel.objects.create(name="Title 1", slug="title")
            RoleModel.objects.create(name="Title 2", slug="title")
