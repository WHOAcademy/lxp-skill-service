from django.test import SimpleTestCase
from skill_app.models import SkillModel


class TestCourseModel(SimpleTestCase):
    def test_obj(self):
        course = SkillModel(title="Title", slug="title")
        self.assertTrue(isinstance(course, SkillModel))
        self.assertEqual(course.title, "Title")
