from voting.models import *
from candidato.models import *
from django.db.models import *
from django import forms


class ChaguaBodiForm(forms.ModelForm):
    is_voted=forms.BooleanField(required=False)
    bodi1=forms.ModelChoiceField(queryset=BoardCandidate.objects.order_by('candidate_name'),label='Mjumbe wa Bodi No.1',widget=forms.Select(attrs={'class': 'form-control bod1'}))
    bodi2 = forms.ModelChoiceField(queryset=BoardCandidate.objects.order_by('candidate_name'),label='Mjumbe wa Bodi No.2',widget=forms.Select(attrs={'class': 'form-control bod2'}))
    bodi3 = forms.ModelChoiceField(queryset=BoardCandidate.objects.order_by('candidate_name'),label='Mjumbe wa Bodi No.3',widget=forms.Select(attrs={'class': 'form-control bod3'}))
    bodi4 = forms.ModelChoiceField(queryset=BoardCandidate.objects.order_by('candidate_name'),label='Mjumbe wa Bodi No.4',widget=forms.Select(attrs={'class': 'form-control bod4'}))
    bodi5 = forms.ModelChoiceField(queryset=BoardCandidate.objects.order_by('candidate_name'),label='Mjumbe wa Bodi No.5',widget=forms.Select(attrs={'class': 'form-control bod5'}))
    bodi6 = forms.ModelChoiceField(queryset=BoardCandidate.objects.order_by('candidate_name'),label='Mjumbe wa Bodi No.6',widget=forms.Select(attrs={'class': 'form-control bod6'}))
    bodi7 = forms.ModelChoiceField(queryset=BoardCandidate.objects.order_by('candidate_name'),label='Mjumbe wa Bodi No.7',widget=forms.Select(attrs={'class': 'form-control bod7'}))
    class Meta:
        model=BoardVote
        fields=['is_voted']



