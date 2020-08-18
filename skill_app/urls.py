from django.urls import path

from skill_app import views


urlpatterns = [
    path('skills', views.SkillListView.as_view(), name='list-skills')
]
