from django_filters import rest_framework as filters

from skill_app import models


class SkillListFilter(filters.FilterSet):
    role_slug = filters.CharFilter(field_name='roles__slug')

    class Meta:
        model = models.SkillModel
        fields = ['role_slug']
