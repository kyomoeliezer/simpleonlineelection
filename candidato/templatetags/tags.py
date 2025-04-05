from django import template
from django.urls import reverse,reverse_lazy
from django.contrib.auth.models import Group
from django.db.models import Q
from candidato.models import *
from voting.models import ChairVote
register = template.Library()

@register.simple_tag
def vota():
    return Voter.objects.filter(is_attended=True).count()

@register.simple_tag
def percentage(vt1,totalV,which):

    if vt1 and totalV:
        return (float(vt1)/(float(totalV)*which))*100
    else:
        return 0


@register.simple_tag
def published():

    if Publishing.objects.first():
        return Publishing.objects.first()
    else:
        return Publishing.objects.create()


@register.simple_tag
def chair_votes(id):
    return ChairVote.objects.filter(chair_id=id).count()

@register.simple_tag
def vise_votes(id):
    return ChairVote.objects.filter(vise_id=id).count()

@register.simple_tag
def voting_opened_for():
    pub = Publishing.objects.first()
    if pub.startVoting:
        return pub.open_voting_for
    else:
        return ' bb'



