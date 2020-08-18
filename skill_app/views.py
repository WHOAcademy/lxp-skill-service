from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from skill_app import serializers, models, filters


class SkillListView(generics.ListAPIView):
    """
    Use this endpoint to GET all skills.
    """
    serializer_class = serializers.SkillSerializer
    queryset = models.SkillModel.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.SkillListFilter
