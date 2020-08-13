from django.test import SimpleTestCase
from skill_app.models import SkillModel


class TestSkill(SimpleTestCase):
    def setUp(self):
        self.skill = SkillModel(name="Test", slug="test")

    def test_title(self):
        self.assertEqual(self.skill.name, "Test")
