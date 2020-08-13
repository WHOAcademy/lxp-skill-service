from django.urls import path

from skill_app import views


urlpatterns = [
    path('Skills', views.SkillListView.as_view(), name='list-skills')
]
