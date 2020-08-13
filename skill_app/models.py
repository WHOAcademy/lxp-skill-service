from django.db import models
from django.utils.translation import ugettext_lazy as _


class RoleModel(models.Model):
    name = models.CharField(_('Role name'), max_length=45, unique=True)
    slug = models.SlugField(_('Role slug'), max_length=64, unique=True)

    class Meta:
        db_table = _('roles')
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')


class SkillModel(models.Model):
    roles = models.ManyToManyField(to=RoleModel)
    name = models.CharField(_('Skill name'), max_length=45)
    slug = models.SlugField(_('Skill slug'), max_length=64)

    class Meta:
        db_table = _('skills')
        verbose_name = _('Skill')
        verbose_name_plural = _('Skills')
