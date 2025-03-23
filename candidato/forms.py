from candidato.models import *
from django.db.models import *
from django import forms
class AddBoardCandidateForm(forms.ModelForm):
    class Meta:
        model=BoardCandidate
        fields=['memberNo','candidate_name']


    def clean_memberNo(self):
        memberNo = self.cleaned_data["memberNo"]
        memberNo=str(memberNo)

        if ChairCandidate.objects.filter(memberNo=memberNo).exists():
            raise forms.ValidationError('This memberNo already added please recheck  ')

        return memberNo


class AddChairCandidateForm(forms.ModelForm):
    class Meta:
        model=ChairCandidate
        fields=['memberNo','candidate_name']


    def clean_memberNo(self):
        memberNo = self.cleaned_data["memberNo"]
        memberNo=str(memberNo)

        if ChairCandidate.objects.filter(memberNo=memberNo).exists():
            raise forms.ValidationError('This memberNo already added please recheck  ')

        return memberNo


class AddComitteCandidateForm(forms.ModelForm):
    class Meta:
        model=CommitteeCandidate
        fields=['memberNo','candidate_name']


    def clean_memberNo(self):
        memberNo = self.cleaned_data["memberNo"]
        memberNo=str(memberNo)

        if CommitteeCandidate.objects.filter(memberNo=memberNo).exists():
            raise forms.ValidationError(' This memberNo already added please recheck ')

        return memberNo

class AddVoterForm(forms.ModelForm):
    mobile2 = forms.CharField(required=False)
    class Meta:
        model=Voter
        fields=['memberNo','name','mobile','mobile2']


    def clean_memberNo(self):
        memberNo = self.cleaned_data["memberNo"]
        memberNo=str(memberNo)

        if Voter.objects.filter(memberNo=memberNo).exists():
            voterob=Voter.objects.filter(memberNo=memberNo).first()
            raise forms.ValidationError(' This memberNo already exists('+voterob.name+') please recheck ')

        return memberNo

    def clean_mobile(self):
        mobile = self.cleaned_data["mobile"]
        mobile=str(mobile)

        if Voter.objects.filter(Q(mobile=mobile)|Q(mobile2=mobile)).exists():
            voterob = Voter.objects.filter(Q(mobile=mobile)|Q(mobile2=mobile)).first()
            raise forms.ValidationError(' This mobile already exists('+voterob.name+') please recheck ')

        return mobile

    def clean_mobile2(self):
        mobile2 = self.cleaned_data["mobile2"]
        mobile=str(mobile2)

        if Voter.objects.filter(Q(mobile=mobile)|Q(mobile2=mobile)).exists():
            voterob = Voter.objects.filter(Q(mobile=mobile)|Q(mobile2=mobile)).first()
            raise forms.ValidationError(' This mobile2 already exists('+voterob.name+') please recheck ')

        return mobile

class UpdateVoterForm(forms.ModelForm):
    mobile2=forms.CharField(required=False)
    class Meta:
        model=Voter
        fields=['memberNo','name','mobile','mobile2']


class VoterImport(forms.ModelForm):
    file=forms.FileField(label='Select a Voters CSV',required=False,widget=forms.FileInput(attrs={'accept':'application/csv'}))
    memberNo=forms.CharField(required=False)

    class Meta:
        model = Voter
        fields = ["memberNo", ]

