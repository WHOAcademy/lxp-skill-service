from django.db import DataError, IntegrityError
from django.test import TestCase
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
        with self.assertRaises(IntegrityError):
            RoleModel.objects.create(name="Title", slug="title-1")
            RoleModel.objects.create(name="Title", slug="title-2")

    def test_slug_unique(self):
        with self.assertRaises(IntegrityError):
            RoleModel.objects.create(name="Title 1", slug="title")
            RoleModel.objects.create(name="Title 2", slug="title")


class TestSkillModel(TestCase):

    def test_create_skill(self):
        role = RoleModel.objects.create(name="Role Title", slug="role-title")
        skill = SkillModel.objects.create(name='Skill Title', slug='skill-slug')
        skill.roles.add(role.pk)

    def test_get_all(self):
        role = RoleModel.objects.create(name="Role Title", slug="role-title")

        skill_1 = SkillModel.objects.create(name='Skill Title 1', slug='skill-slug-1')
        skill_1.roles.add(role.pk)
        skill_2 = SkillModel.objects.create(name='Skill Title 2', slug='skill-slug-2')
        skill_2.roles.add(role.pk)
        skill_3 = SkillModel.objects.create(name='Skill Title 3', slug='skill-slug-3')
        skill_3.roles.add(role.pk)

        skills = SkillModel.objects.all()
        self.assertEqual(len(skills), 3)

    def test_skill_obj(self):
        role = RoleModel.objects.create(name="Role Title", slug="role-title")
        skill = SkillModel.objects.create(name='Skill Title', slug='skill-slug')
        skill.roles.add(role.pk)

        skill = SkillModel.objects.all()[0]
        print(skill.roles)
        self.assertTrue(isinstance(skill, SkillModel))
        self.assertEqual(skill.name, "Skill Title")
        self.assertEqual(skill.slug, "skill-slug")
        # todo: check assert for role object

    def test_name_max_length(self):
        with self.assertRaises(DataError):
            title = "This is a test This is a test This is a test This is a test "
            SkillModel.objects.create(name=title, slug="title")

    def test_slug_max_length(self):
        with self.assertRaises(DataError):
            slug = "This is a test This is a test This is a test This is a test This is a test "
            SkillModel.objects.create(name="Title", slug=slug)

    def test_name_unique(self):
        with self.assertRaises(IntegrityError):
            role = RoleModel.objects.create(name="Title", slug="title")
            skill_1 = SkillModel.objects.create(name='Skill Title', slug='skill-slug-1')
            skill_1.roles.add(role.pk)
            skill_2 = SkillModel.objects.create(name='Skill Title', slug='skill-slug-2')
            skill_2.roles.add(role.pk)

    def test_slug_unique(self):
        with self.assertRaises(IntegrityError):
            role = RoleModel.objects.create(name="Title", slug="title")
            skill_1 = SkillModel.objects.create(name='Skill Title 1', slug='skill-slug')
            skill_1.roles.add(role.pk)
            skill_2 = SkillModel.objects.create(name='Skill Title 2', slug='skill-slug')
            skill_2.roles.add(role.pk)
