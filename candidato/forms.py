from candidato.models import *
from django.db.models import *
from django import forms
from django.forms import ValidationError
def validate_file_extension(value):
  import os
  ext = os.path.splitext(value.name)[1]
  valid_extensions = ['.pdf','.pdf']
  if not ext in valid_extensions:
    raise ValidationError(u' only .PDF file are allowed !')


class AddBoardCandidateForm(forms.ModelForm):
    class Meta:
        model=BoardCandidate
        fields=['memberNo','candidate_name']


    def clean_memberNo(self):
        memberNo = self.cleaned_data["memberNo"]
        memberNo=str(memberNo)

        if BoardCandidate.objects.filter(memberNo=memberNo).exists():
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

class AddViseCandidateForm(forms.ModelForm):
    class Meta:
        model=ViseCandidate
        fields=['memberNo','candidate_name']


    def clean_memberNo(self):
        memberNo = self.cleaned_data["memberNo"]
        memberNo=str(memberNo)

        if ViseCandidate.objects.filter(memberNo=memberNo).exists():
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
        if mobile:

            if Voter.objects.filter(Q(mobile=mobile)|Q(mobile2=mobile)).exists():
                voterob = Voter.objects.filter(Q(mobile=mobile)|Q(mobile2=mobile)).first()
                raise forms.ValidationError(' This mobile2 already exists('+voterob.name+') please recheck ')

        return mobile

class UpdateVoterForm(forms.ModelForm):
    mobile2=forms.CharField(required=False)
    class Meta:
        model=Voter
        fields=['memberNo','name','mobile','mobile2']
class UpdateVoterEditForm(forms.ModelForm):
    mobile2=forms.CharField(required=False)
    class Meta:
        model=Voter
        fields=['memberNo','name','mobile','mobile2','is_special']


class VoterImport(forms.ModelForm):
    file=forms.FileField(label='Select a Voters CSV',required=False,widget=forms.FileInput(attrs={'accept':'application/csv'}))
    memberNo=forms.CharField(required=False)

    class Meta:
        model = Voter
        fields = ["memberNo", ]

class ChapishaMatokeoBoardForm(forms.ModelForm):
    bodi_file=forms.FileField(label='Weka Attachment',validators=[validate_file_extension],required=True,widget=forms.FileInput(attrs={'accept':'application/pdf'}))
    class Meta:
        model = Matokeo
        fields = ["title",'maelezo','bodi_file' ]

class ChapishaMatokeoKamatiForm(forms.ModelForm):
    kamati_file=forms.FileField(label='Weka Attachment',required=False,widget=forms.FileInput(attrs={'accept':'application/csv'}))

    class Meta:
        model = Matokeo
        fields = ["title",'maelezo' ]

class ChapishaMatokeoMKitiForm(forms.ModelForm):
    mkiti_file=forms.FileField(label='Weka Attachment',required=False,widget=forms.FileInput(attrs={'accept':'application/csv'}))

    class Meta:
        model = Matokeo
        fields = ["title",'maelezo' ]

