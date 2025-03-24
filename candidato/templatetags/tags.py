from django import template
from django.urls import reverse,reverse_lazy
from django.contrib.auth.models import Group
from django.db.models import Q
from candidato.models import Voter
register = template.Library()

@register.simple_tag
def vota():
    return Voter.objects.all().count()
