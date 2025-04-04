import datetime
from dateutil.relativedelta import relativedelta
import os
import csv
from django.core.files.storage import FileSystemStorage
from django.db.models import *
from django.shortcuts import render,HttpResponse
from django.urls import reverse_lazy
import requests
from django.contrib import messages
import json
from django.shortcuts import render, redirect,reverse
from django.views.generic import CreateView,ListView,UpdateView,View,DeleteView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from candidato.models import ChairCandidate
from candidato.common import *
from candidato.forms import *
from voting.models import *
from auths.models import User

####CHAIR
class ChairCandidates(LoginRequiredMixin,CreateView):
    model = ChairCandidate
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    template_name = 'candidate/candidates_chair.html'
    model=ChairCandidate
    form_class=AddChairCandidateForm

    header = 'Chair Candidates'
    success_url = reverse_lazy('chair_candidates')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['lists'] =ChairCandidate.objects.all().order_by('candidate_name')
        context['form']=self.form_class
        context['header']=self.header
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():

            form = form.save(commit=False)
            form.created_by_id = self.request.user.id
            form.save()
            messages.success(request, 'Succes!, Umejaza taarifa za  mgombea')

            return redirect(reverse('chair_candidates'))
        lists=ChairCandidate.objects.all().order_by('candidate_name')
        return render(self.request, self.template_name, {'header':self.header,'form': form, 'header': 'Wagombea','lists':lists})

class UpdateChairCandidate(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = ChairCandidate
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    template_name = 'candidate/candidates_chair.html'
    model=ChairCandidate
    context_object_name = 'form'
    fields=['memberNo','candidate_name']
    header = 'Add Chair Candidate'
    success_message = "Success!  Success Updated"
    success_url = reverse_lazy('chair_candidates')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['mgombea'] = ChairCandidate.objects.filter(id=self.kwargs['pk']).first()
        context['lists'] = ChairCandidate.objects.all().order_by('candidate_name')
        context['header']='Update Chair Candidate'
        return context


class ChairCandidateDelete(LoginRequiredMixin,DeleteView,SuccessMessageMixin):
    """DELETE"""
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model = ChairCandidate
    success_message = "Success!  deleted successfully."
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
            messages.success(request,'Success!,Deleted')
        except ProtectedError:
            messages.warning(request,'Faile!,You cannot delete this it is related to others')
            return redirect(reverse('chair_candidates'))

    def get(self, request, *args, **kwargs):
            return self.post(request, *args, **kwargs)
    def get_success_url(self):
        return reverse('chair_candidates')
#####VISE CHAIR
class ViseCandidates(LoginRequiredMixin,CreateView):
    model = ViseCandidate
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    template_name = 'candidate/candidates_vise.html'
    form_class=AddViseCandidateForm

    header = 'Vise Candidates'
    success_url = reverse_lazy('vise_candidates')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['lists'] =ViseCandidate.objects.all().order_by('candidate_name')
        context['form']=self.form_class
        context['header']=self.header
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():

            form = form.save(commit=False)
            form.created_by_id = self.request.user.id
            form.save()
            messages.success(request, 'Succes!, Umejaza taarifa za  mgombea')

            return redirect(reverse('vise_candidates'))
        lists=ViseCandidate.objects.all().order_by('candidate_name')
        return render(self.request, self.template_name, {'header':self.header,'form': form, 'header': 'Wagombea','lists':lists})

class ViseUpdateCandidate(LoginRequiredMixin,SuccessMessageMixin,UpdateView):

    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    template_name = 'candidate/candidates_vise.html'
    model=ViseCandidate
    context_object_name = 'form'
    fields=['memberNo','candidate_name']
    header = 'Add Vise Candidate'
    success_message = "Success!  Success Updated"
    success_url = reverse_lazy('vise_candidates')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['mgombea'] = ViseCandidate.objects.filter(id=self.kwargs['pk']).first()
        context['lists'] = ViseCandidate.objects.all().order_by('candidate_name')
        context['header']='Update Vise Candidate'
        return context
class ViseChairCandidateDelete(LoginRequiredMixin,DeleteView,SuccessMessageMixin):
    """DELETE"""
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model = ViseCandidate
    success_message = "Success!  deleted successfully."
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
            messages.success(request,'Success!,Deleted')
        except ProtectedError:
            messages.warning(request,'Faile!,You cannot delete this it is related to others')
            return redirect(reverse('vise_candidates'))

    def get(self, request, *args, **kwargs):
            return self.post(request, *args, **kwargs)
    def get_success_url(self):
        return reverse('vise_candidates')
######## COMMITTEE
class CommitteeCandidatesView(CreateView):
    model = CommitteeCandidate
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    template_name = 'candidate/candidates_committee.html'

    form_class=AddComitteCandidateForm

    header = 'Committee Candidates'
    success_url = reverse_lazy('committee_candidates')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['lists'] =CommitteeCandidate.objects.all().order_by('candidate_name')
        context['form']=self.form_class
        context['header']=self.header
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():

            form = form.save(commit=False)
            form.created_by_id = self.request.user.id
            form.save()
            messages.success(request, 'Succes!, Umejaza taarifa za  mgombea wa board')

            return redirect(reverse('committee_candidates'))
        lists=CommitteeCandidate.objects.all().order_by('candidate_name')
        return render(self.request, self.template_name, {'header':self.header,'form': form, 'header': 'Wagombea','lists':lists})



class UpdateCommitteeCandidate(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = CommitteeCandidate
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    template_name = 'candidate/candidates_committee.html'
    context_object_name = 'form'
    fields=['memberNo','candidate_name']
    header = 'Add Committee Candidate'
    success_message = "Success!  Success Updated"
    success_url = reverse_lazy('committee_candidates')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['mgombea'] = CommitteeCandidate.objects.filter(id=self.kwargs['pk']).first()
        context['lists'] = CommitteeCandidate.objects.all().order_by('candidate_name')
        context['header']='Update Committee Candidate'
        return context


class CommitteeCandidateDelete(LoginRequiredMixin,DeleteView,SuccessMessageMixin):
    """DELETE"""
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model = CommitteeCandidate
    success_message = "Success!  deleted successfully."
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
            messages.success(request,'Success!,Deleted')
        except ProtectedError:
            messages.warning(request,'Faile!,You cannot delete this it is related to others')
            return redirect(reverse('committee_candidates'))

    def get(self, request, *args, **kwargs):
            return self.post(request, *args, **kwargs)
    def get_success_url(self):
        return reverse('committee_candidates')

######## BOARD
class BoardCandidatesView(CreateView):
    model = BoardCandidate
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    template_name = 'candidate/candidates_board.html'

    form_class=AddBoardCandidateForm

    header = 'Board Candidates'
    success_url = reverse_lazy('board_candidates')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['lists'] =BoardCandidate.objects.all().order_by('candidate_name')
        context['form']=self.form_class
        context['header']=self.header
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():

            form = form.save(commit=False)
            form.created_by_id = self.request.user.id
            form.save()
            messages.success(request, 'Succes!, Umejaza taarifa za  mgombea wa board')

            return redirect(reverse('board_candidates'))
        lists=ChairCandidate.objects.all().order_by('candidate_name')
        return render(self.request, self.template_name, {'header':self.header,'form': form, 'header': 'Wagombea','lists':lists})



class UpdateBoardCandidate(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = BoardCandidate
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    template_name = 'candidate/candidates_board.html'
    context_object_name = 'form'
    fields=['memberNo','candidate_name']
    header = 'Add Board Candidate'
    success_message = "Success!  Success Updated"
    success_url = reverse_lazy('board_candidates')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['mgombea'] = BoardCandidate.objects.filter(id=self.kwargs['pk']).first()
        context['lists'] = BoardCandidate.objects.all().order_by('candidate_name')
        context['header']='Update Board Candidate'
        return context


class BaordCandidateDelete(LoginRequiredMixin,DeleteView,SuccessMessageMixin):
    """DELETE"""
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model = BoardCandidate
    success_message = "Success!  deleted successfully."
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
            messages.success(request,'Success!,Deleted')
        except ProtectedError:
            messages.warning(request,'Faile!,You cannot delete this it is related to others')
            return redirect(reverse('board_candidates'))

    def get(self, request, *args, **kwargs):
            return self.post(request, *args, **kwargs)
    def get_success_url(self):
        return reverse('board_candidates')

###########VOTERS REGISTRATION
class VotersRegView(LoginRequiredMixin,CreateView):
    model = Voter
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    template_name = 'voters/new_voter.html'

    form_class=AddVoterForm

    header = 'Andikisha Mpiga Kura'
    success_url = reverse_lazy('voters')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['lists'] =Voter.objects.all().order_by('memberNo')
        context['form']=self.form_class
        context['header']=self.header
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():

            form2 = form.save(commit=False)
            form2.created_by_id = self.request.user.id
            form2.save()

            user=User.objects.create(mobile=request.POST.get('mobile'),username=request.POST.get('memberNo'),name=request.POST.get('candidate_name'))
            form2.user = user
            form2.save()
            messages.success(request, 'Succes!, Umejaza taarifa za  mgombea wa board')

            return redirect(self.success_url)
        lists=Voter.objects.all().order_by('memberNo')
        return render(self.request, self.template_name, {'header':self.header,'form': form, 'header': 'Wagombea','lists':lists})
class VotersUpdateView(LoginRequiredMixin,UpdateView):
    model = Voter
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    template_name = 'voters/update_voter.html'
    form_class=UpdateVoterForm
    header = 'Update Mpiga Kura'
    success_url = reverse_lazy('voters')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['header']=self.header
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():

            form2 = form.save(commit=False)
            memberNo = request.POST.get('memberNo')
            mobile=request.POST.get('mobile')
            mobile2 = request.POST.get('mobile2')
            name = request.POST.get('name')
            if Voter.objects.filter(~Q(id=self.kwargs['pk'])&Q(Q(mobile__iexact=mobile)|Q(mobile2__iexact=mobile))).exists():
                voterOb=Voter.objects.filter(~Q(id=self.kwargs['pk'])&Q(Q(mobile__iexact=mobile)|Q(mobile2__iexact=mobile))).first()
                mess='Mobile number ('+str(mobile)+') exists to other voters ('+voterOb.name+')'
                return render(self.request, self.template_name,
                              {'header': self.header, 'form': form, 'header': 'Wagombea', 'error': mess})
            elif Voter.objects.filter(~Q(id=self.kwargs['pk'])&Q(Q(mobile__iexact=mobile2)|Q(mobile2__iexact=mobile2))).exists() and mobile2:
                voterOb=Voter.objects.filter(~Q(id=self.kwargs['pk'])&Q(Q(mobile__iexact=mobile2)|Q(mobile2__iexact=mobile2))).first()
                mess='Mobile number ('+str(mobile2)+') exists to other voters ('+voterOb.name+')'
                return render(self.request, self.template_name,
                              {'header': self.header, 'form': form, 'header': 'Wagombea', 'error': mess})

            elif Voter.objects.filter(~Q(id=self.kwargs['pk'])&Q(memberNo__iexact=memberNo)).exists():
                voterOb=Voter.objects.filter(~Q(id=self.kwargs['pk'])&Q(memberNo__iexact=memberNo)).first()
                mess='Reg number ('+str(memberNo)+') exists to other voters ('+voterOb.name+')'
                return render(self.request, self.template_name,
                              {'header': self.header, 'form': form, 'header': 'Wagombea', 'error': mess})
            else:
                Voter.objects.filter(id=self.kwargs['pk']).update(
                    memberNo=memberNo,
                    mobile=mobile,
                    mobile2=mobile2,
                    name=name
                )
                voter=Voter.objects.filter(id=self.kwargs['pk']).first()
                User.objects.filter(id=voter.user_id).update(
                    username=memberNo,name=name,
                mobile = mobile
                )
            messages.success(request, 'Succes!, Umejaza taarifa za  mgombea wa board')

            return redirect(reverse('voters'))
        lists=Voter.objects.all().order_by('memberNo')
        return render(self.request, self.template_name, {'header':self.header,'form': form, 'header': 'Wagombea','lists':lists})

####Voters Lists
class VotersView(LoginRequiredMixin,ListView):
    model = Voter
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    template_name = 'voters/voters.html'
    model=Voter
    header = 'Wapiga Kura'
    success_url = reverse_lazy('voters')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['lists'] =Voter.objects.all().order_by('memberNo')
        context['header']=self.header
        return context

class DeleteVoter(LoginRequiredMixin,DeleteView,SuccessMessageMixin):
    """DELETE"""
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model = Voter
    success_message = "Success!  deleted successfully."
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
            messages.success(request,'Success!,Deleted')
        except ProtectedError:
            messages.warning(request,'Faile!,You cannot delete this it is related to others')
            return redirect(reverse('voters'))

    def get(self, request, *args, **kwargs):
            return self.post(request, *args, **kwargs)
    def get_success_url(self):
        return reverse('voters')

class ImportVoters(LoginRequiredMixin,CreateView):
    login_url = reverse_lazy('login_user')
    redirect_field_name = 'next'
    template_name = 'import/import_voters.html'
    model = Voter
    header='Import Voters'
    form_class=VoterImport
    def get(self, request, *args, **kwargs):

        header=self.header
        return render(request,self.template_name,{'form':self.form_class,'header':header})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        html=''
        if form.is_valid():
            file = request.FILES['file']
            fs = FileSystemStorage()
            name = 'Import-voters-file.csv'
            file_name = fs.save(name, file)
            file_path = fs.path(file_name)
            with open(fs.path(file_name), 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                counter = 0
                cou=0
                coAdd=0
                for row in reader:
                    html=html+'<tr><td>'+row['MEMBER_NO']+'</td><td>'+row['NAME']+'</td><td>'+row['MOBILE']+'</td>'+row['MOBILE2']+'</td><td>'
                    if row['MEMBER_NO'] and row['NAME'] and row['MOBILE'] :
                        if Voter.objects.filter(memberNo__iexact=row['MEMBER_NO']).exists() and Voter.objects.filter(mobile__iexact=row['MOBILE']).exists():
                            Voter.objects.filter(memberNo__iexact=row['MEMBER_NO']).update(
                                mobile=row['MOBILE'],
                                name=row['NAME'],
                                updated_by_id=request.user.id,
                                updated_on=datetime.datetime.now(),
                                bywhat='import'
                            )
                            voter = Voter.objects.filter(memberNo__iexact=row['MEMBER_NO']).first()
                            User.objects.filter(id=voter.user_id).update(
                                username=row['MEMBER_NO'], name=row['NAME'],mobile=row['MOBILE'],
                            )
                            html=html+' Updated</td>'

                            coAdd=coAdd+1

                        else:
                            voter=Voter.objects.create(
                                memberNo=row['MEMBER_NO'],
                                mobile=row['MOBILE'],
                                name=row['NAME'],
                                updated_by_id=request.user.id,
                                updated_on=datetime.datetime.now(),
                                bywhat='import'
                            )
                            user=User.objects.create(mobile=row['MOBILE'],
                                username=row['MEMBER_NO'], name=row['NAME']
                            )
                            voter.user=user
                            voter.save()
                            cou=cou+1

                            html = html + ' Registered</td>'
                    else:
                        html = html + ' Some data is missing</td>'

                    html = html+'</tr>'
                    counter += 1
            messages.success(request,'Succesful imported added-'+str(cou)+' updated - '+str(coAdd))
            return redirect(reverse('voters'))
            return render(request,self.template_name,{'form':form,'header':'Imported Data Report','htmldata':html})

        return render(request,self.template_name,{'form':form,'header':self.header})

class ImportCommittee(LoginRequiredMixin,CreateView):
    login_url = reverse_lazy('login_user')
    redirect_field_name = 'next'
    template_name = 'import/import_committee.html'
    model = CommitteeCandidate
    header='Import Committee'
    form_class=VoterImport
    def get(self, request, *args, **kwargs):

        header=self.header
        return render(request,self.template_name,{'form':self.form_class,'header':header})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        html=''
        if form.is_valid():
            file = request.FILES['file']
            fs = FileSystemStorage()
            name = 'Import-committe-file.csv'
            file_name = fs.save(name, file)
            file_path = fs.path(file_name)
            with open(fs.path(file_name), 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                counter = 0
                cou=0
                coAdd=0
                for row in reader:
                    html=html+'<tr><td>'+row['MEMBER_NO']+'</td><td>'+row['NAME']+'</td>'
                    if row['MEMBER_NO'] and row['NAME'] :
                        if CommitteeCandidate.objects.filter(memberNo__iexact=row['MEMBER_NO']).exists():
                            CommitteeCandidate.objects.filter(memberNo__iexact=row['MEMBER_NO']).update(

                                candidate_name=row['NAME'],
                                bywhat='import'
                            )
                            html=html+' Updated</td>'

                            coAdd=coAdd+1

                        else:
                            CommitteeCandidate.objects.create(
                                memberNo=row['MEMBER_NO'],
                                candidate_name=row['NAME']
                            )
                            cou=cou+1

                            html = html + ' Registered</td>'
                    else:
                        html = html + ' Some data is missing</td>'

                    html = html+'</tr>'
                    counter += 1
            messages.success(request,'Succesful imported added-'+str(cou)+' updated - '+str(coAdd))
            return redirect(reverse('committee_candidates'))
            return render(request,self.template_name,{'form':form,'header':'Imported Data Report','htmldata':html})

        return render(request,self.template_name,{'form':form,'header':self.header})

class ImportBoard(LoginRequiredMixin,CreateView):
    login_url = reverse_lazy('login_user')
    redirect_field_name = 'next'
    template_name = 'import/import_board.html'
    model = BoardCandidate
    header='Import Board'
    form_class=VoterImport
    def get(self, request, *args, **kwargs):

        header=self.header
        return render(request,self.template_name,{'form':self.form_class,'header':header})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        html=''
        if form.is_valid():
            file = request.FILES['file']
            fs = FileSystemStorage()
            name = 'Import-committe-file.csv'
            file_name = fs.save(name, file)
            file_path = fs.path(file_name)
            with open(fs.path(file_name), 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                counter = 0
                cou=0
                coAdd=0
                for row in reader:
                    html=html+'<tr><td>'+row['MEMBER_NO']+'</td><td>'+row['NAME']+'</td>'
                    if row['MEMBER_NO'] and row['NAME'] :
                        if BoardCandidate.objects.filter(memberNo__iexact=row['MEMBER_NO']).exists():
                            BoardCandidate.objects.filter(memberNo__iexact=row['MEMBER_NO']).update(

                                candidate_name=row['NAME'],
                                bywhat='import'
                            )
                            html=html+' Updated</td>'

                            coAdd=coAdd+1

                        else:
                            BoardCandidate.objects.create(
                                memberNo=row['MEMBER_NO'],
                                candidate_name=row['NAME']
                            )
                            cou=cou+1

                            html = html + ' Registered</td>'
                    else:
                        html = html + ' Some data is missing</td>'

                    html = html+'</tr>'
                    counter += 1
            messages.success(request,'Succesful imported added-'+str(cou)+' updated - '+str(coAdd))
            return redirect(reverse('board_candidates'))
            return render(request,self.template_name,{'form':form,'header':'Imported Data Report','htmldata':html})

        return render(request,self.template_name,{'form':form,'header':self.header})

class ImportChair(LoginRequiredMixin,CreateView):
    login_url = reverse_lazy('login_user')
    redirect_field_name = 'next'
    template_name = 'import/import_chair.html'
    model = ChairCandidate
    header='Import Chair'
    form_class=VoterImport
    def get(self, request, *args, **kwargs):

        header=self.header
        return render(request,self.template_name,{'form':self.form_class,'header':header})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        html=''
        if form.is_valid():
            file = request.FILES['file']
            fs = FileSystemStorage()
            name = 'Import-committe-file.csv'
            file_name = fs.save(name, file)
            file_path = fs.path(file_name)
            with open(fs.path(file_name), 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                counter = 0
                cou=0
                coAdd=0
                for row in reader:
                    html=html+'<tr><td>'+row['MEMBER_NO']+'</td><td>'+row['NAME']+'</td>'
                    if row['MEMBER_NO'] and row['NAME'] :
                        if ChairCandidate.objects.filter(memberNo__iexact=row['MEMBER_NO']).exists():
                            ChairCandidate.objects.filter(memberNo__iexact=row['MEMBER_NO']).update(

                                candidate_name=row['NAME'],
                                bywhat='import'
                            )
                            html=html+' Updated</td>'

                            coAdd=coAdd+1

                        else:
                            ChairCandidate.objects.create(
                                memberNo=row['MEMBER_NO'],
                                candidate_name=row['NAME']
                            )
                            cou=cou+1

                            html = html + ' Registered</td>'
                    else:
                        html = html + ' Some data is missing</td>'

                    html = html+'</tr>'
                    counter += 1
            messages.success(request,'Succesful imported added-'+str(cou)+' updated - '+str(coAdd))
            return redirect(reverse('chair_candidates'))
            return render(request,self.template_name,{'form':form,'header':'Imported Data Report','htmldata':html})

        return render(request,self.template_name,{'form':form,'header':self.header})
class ImportViseChair(LoginRequiredMixin,CreateView):
    login_url = reverse_lazy('login_user')
    redirect_field_name = 'next'
    template_name = 'import/import_chair.html'
    model = ViseCandidate
    header='Import Vise Chair'
    form_class=VoterImport
    def get(self, request, *args, **kwargs):

        header=self.header
        return render(request,self.template_name,{'form':self.form_class,'header':header})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        html=''
        if form.is_valid():
            file = request.FILES['file']
            fs = FileSystemStorage()
            name = 'Import-committe-file.csv'
            file_name = fs.save(name, file)
            file_path = fs.path(file_name)
            with open(fs.path(file_name), 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                counter = 0
                cou=0
                coAdd=0
                for row in reader:
                    html=html+'<tr><td>'+row['MEMBER_NO']+'</td><td>'+row['NAME']+'</td>'
                    if row['MEMBER_NO'] and row['NAME'] :
                        if ViseCandidate.objects.filter(memberNo__iexact=row['MEMBER_NO']).exists():
                            ViseCandidate.objects.filter(memberNo__iexact=row['MEMBER_NO']).update(

                                candidate_name=row['NAME'],
                                bywhat='import'
                            )
                            html=html+' Updated</td>'

                            coAdd=coAdd+1

                        else:
                            ViseCandidate.objects.create(
                                memberNo=row['MEMBER_NO'],
                                candidate_name=row['NAME']
                            )
                            cou=cou+1

                            html = html + ' Registered</td>'
                    else:
                        html = html + ' Some data is missing</td>'

                    html = html+'</tr>'
                    counter += 1
            messages.success(request,'Succesful imported added-'+str(cou)+' updated - '+str(coAdd))
            return redirect(reverse('vise_candidates'))
            return render(request,self.template_name,{'form':form,'header':'Imported Data Report','htmldata':html})

        return render(request,self.template_name,{'form':form,'header':self.header})

class SmsList(View):
    template_name='sms/lists.html'
    def get(self,request,*args,**kwargs):
        lists=SmsSent.objects.all().order_by('-created_on')
        return render(request,self.template_name,{'lists':lists,'header':'Sent SMS Lists'})

class SendTestSMs(View):
    def get(self,request,*args,**kwargs):

        mob=request.GET.get('mob')
        nowTime=datetime.datetime.now()
        newTimeAfter30Min = nowTime + relativedelta(minutes=30)


        userId=request.GET.get('userid')
        dataOb=User.objects.filter(id=userId).first()

        dataOb.otp_code=random.randint(101000,900000)
        dataOb.otp_time = newTimeAfter30Min
        dataOb.save()
        return send_sms(dataOb.mobile,'Uchaguzi OTP ni '+str(dataOb.otp_code)+'. Itumie ndani ya dakika 30.');

class Dashboard(LoginRequiredMixin,View):
    login_url = reverse_lazy('login_user')
    redirect_field_name = 'next'
    template_name='dashboard/dashboard.html'
    def get(self,request,*args,**kwargs):
        context={}
        context['board']=BoardVote.objects.aggregate(countT=Count('voter_id',distinct=True))['countT']
        context['chair'] = ChairVote.objects.aggregate(countT=Count('voter_id', distinct=True))['countT']
        context['committee'] = CommittteeVote.objects.aggregate(countT=Count('voter_id', distinct=True))['countT']

        return render(request,self.template_name,context)

class MatokeoBoard(LoginRequiredMixin,View):
    login_url = reverse_lazy('login_user')
    redirect_field_name = 'next'
    template_name='matokeo/board_matokeo.html'
    def get(self,request,*args,**kwargs):
        context={}
        context['boardAll']=BoardVote.objects.aggregate(countT=Count('voter_id',distinct=True))['countT']

        context['board']=BoardCandidate.objects.values(
            'memberNo',
            candidateName=F('candidate_name'),


        ).annotate(
            votes=Sum(
            Case(
                When(Q(boardvote__isnull=False), then=1),
                default=Value(0),
                output_field=IntegerField(),
            )
        ),
        ).order_by('-votes','candidateName')

        return render(request,self.template_name,context)

class MatokeoCommitte(LoginRequiredMixin,View):
    login_url = reverse_lazy('login_user')
    redirect_field_name = 'next'
    template_name='matokeo/committee_matokeo.html'
    def get(self,request,*args,**kwargs):
        context={}
        context['committeeAll']=CommittteeVote.objects.aggregate(countT=Count('voter_id',distinct=True))['countT']

        context['committee']=CommitteeCandidate.objects.values(
            'memberNo',
            candidateName=F('candidate_name'),


        ).annotate(
            votes=Sum(
            Case(
                When(Q(committteevote__isnull=False), then=1),
                default=Value(0),
                output_field=IntegerField(),
            )
        ),
        ).order_by('-votes','candidateName')

        return render(request,self.template_name,context)
class MatokeoChair(LoginRequiredMixin,View):
    login_url = reverse_lazy('login_user')
    redirect_field_name = 'next'
    template_name='matokeo/chair_matokeo.html'
    def get(self,request,*args,**kwargs):
        context={}
        context['chairCount'] = ChairVote.objects.filter(chair_id__isnull=False).count()
        context['viseCount'] = ChairVote.objects.filter(vise_id__isnull=False).count()

        context['chairs']=ChairCandidate.objects.all()
        context['vise'] = ViseCandidate.objects.all()

        return render(request,self.template_name,context)




class FlushButton(LoginRequiredMixin,View):
    login_url = reverse_lazy('login_user')
    redirect_field_name = 'next'
    template_name='dashboard/dashboard.html'
    def get(self,request,*args,**kwargs):
        """
        BoardVote.objects.all().delete()
        ChairCandidate.objects.all().delete()
        CommitteeCandidate.objects.all().delete()
        BoardCandidate.objects.all().delete()
        ViseCandidate.objects.all().delete()
        """
        BoardVote.objects.all().delete()
        ChairVote.objects.all().delete()
        CommittteeVote.objects.all().delete()
        Publishing.objects.all().delete()
        voter=Voter.objects.all()
        for v in voter:
          User.objects.filter(id=v.user_id).delete()
        Voter.objects.all().delete()


        return redirect(reverse('dashboard'))

class PublishUnPublishBodiView(LoginRequiredMixin,View):
    login_url = reverse_lazy('login_user')
    redirect_field_name = 'next'

    def get(self,*args,**kwargs):
        pub=Publishing.objects.first()
        if not pub:
            pub=Publishing.objects.create()
        if pub.publish_board_result:
            pub.publish_board_result=False
        else:
            pub.publish_board_result=True
        pub.save()
        #return HttpResponse(pub.publish_board_result)
        return redirect(reverse('matokeo_bodi'))

class PublishUnPublishCommitteeView(LoginRequiredMixin,View):
    login_url = reverse_lazy('login_user')
    redirect_field_name = 'next'

    def get(self,*args,**kwargs):
        pub=Publishing.objects.first()
        if not pub:
            pub=Publishing.objects.create()

        if pub.publish_committee_result:
            pub.publish_committee_result=False
        else:
            pub.publish_committee_result=True

        pub.save()
        return redirect(reverse('matokeo_kamati'))


class PublishUnPublishChairView(LoginRequiredMixin,View):
    login_url = reverse_lazy('login_user')
    redirect_field_name = 'next'

    def get(self,*args,**kwargs):
        pub=Publishing.objects.first()
        if not pub:
            pub=Publishing.objects.create()
        if pub.publish_chair_result:
            pub.publish_chair_result = False
        else:
            pub.publish_chair_result = True

        pub.save()

        return redirect(reverse('matokeo_chair'))


