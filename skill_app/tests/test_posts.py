from django.test import SimpleTestCase
from skill_app.models import CourseModel


class TestCourse(SimpleTestCase):
    def setUp(self):
        self.course = CourseModel(title="Title", description="text")

    def test_title(self):
        self.assertEqual(self.course.title, "Title")
