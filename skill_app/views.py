from rest_framework import generics

from skill_app import serializers, models


class SkillListView(generics.ListAPIView):
    """
    Use this endpoint to GET all skills.
    """
    serializer_class = serializers.SkillSerializer
    queryset = models.SkillModel.objects.all()
