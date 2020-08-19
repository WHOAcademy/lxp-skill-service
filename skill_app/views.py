from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

from skill_app import serializers, models


role_slug_param = openapi.Parameter('role_slug',
                                    openapi.IN_QUERY,
                                    description="Returns skills for a given role",
                                    type=openapi.TYPE_STRING)


class SkillListView(generics.ListAPIView):
    """
    Use this endpoint to GET all skills.
    """
    serializer_class = serializers.SkillSerializer
    model = models.SkillModel

    @swagger_auto_schema(manual_parameters=[role_slug_param])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        role_slug = self.request.query_params.get('role_slug', None)
        if not role_slug:
            return self.model.objects.all()
        else:
            queryset = self.model.objects.filter(roles__slug=role_slug)
            if queryset:
                return queryset
            else:
                return self.model.objects.all()
