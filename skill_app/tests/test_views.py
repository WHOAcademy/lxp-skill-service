from rest_framework.test import APITestCase
from django.urls import reverse

from skill_app.models import SkillModel, RoleModel


class TestSkillView(APITestCase):

    def test_get_all(self):

        role = RoleModel.objects.create(name="Role Title", slug="role-title")
        skill = SkillModel.objects.create(name='Skill Title', slug='skill-title')
        skill.roles.add(role.pk)

        url = reverse("list-skills")
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        self.assertEquals(skill.name, response.data[0]["name"])
        self.assertEquals(skill.slug, response.data[0]["slug"])
        self.assertTrue(response.data[0].get("role") is None)

    def test_get_skills_for_role(self):
        role_slug = "role-title"
        role = RoleModel.objects.create(name="Role Title", slug=role_slug)
        role_2 = RoleModel.objects.create(name="Role Title 2", slug="role-title-2")

        skill = SkillModel.objects.create(name='Skill Title', slug='skill-title')
        skill.roles.add(role.pk)
        skill_2 = SkillModel.objects.create(name='Skill Title 2', slug='skill-title-2')
        skill_2.roles.add(role_2.pk)

        role_slug_for_query = "role-title"

        url = reverse("list-skills")
        data = {'role_slug': role_slug_for_query}
        response = self.client.get(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        self.assertEquals(skill.name, response.data[0]["name"])
        self.assertEquals(skill.slug, response.data[0]["slug"])
        self.assertTrue(response.data[0].get("role") is None)

    def test_get_skills_for_invalid_role(self):
        role_slug = "role-title"
        role = RoleModel.objects.create(name="Role Title", slug=role_slug)
        role_2 = RoleModel.objects.create(name="Role Title 2", slug="role-title-2")

        skill = SkillModel.objects.create(name='Skill Title', slug='skill-title')
        skill.roles.add(role.pk)
        skill_2 = SkillModel.objects.create(name='Skill Title 2', slug='skill-title-2')
        skill_2.roles.add(role_2.pk)

        role_slug_for_query = "invalid-role-title"

        url = reverse("list-skills")
        data = {'role_slug': role_slug_for_query}
        response = self.client.get(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
