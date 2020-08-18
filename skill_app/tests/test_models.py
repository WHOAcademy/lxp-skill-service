from django.test import SimpleTestCase
from skill_app.models import RoleModel


class TestRoleModel(SimpleTestCase):
    def test_obj(self):
        role = RoleModel(name="Title", slug="title")
        self.assertTrue(isinstance(role, RoleModel))
        self.assertEqual(role.name, "Title")
