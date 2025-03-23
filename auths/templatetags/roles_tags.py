from django import template
from django.urls import reverse,reverse_lazy
from django.contrib.auth.models import Group
from django.db.models import Q

register = template.Library()

@register.simple_tag
def is_admin(user):
    if user.role:
        return user.role.perm.filter(perm_name__in=['admin','can_add_role','manage_setting','manage_buying']).exists()
    return False
@register.simple_tag
def is_checklogin(user):
     if user.is_anonymous:
         return redirect(reverse('auths:login_user'))
     return ''

