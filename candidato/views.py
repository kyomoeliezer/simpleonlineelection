import datetime
import os
import csv
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
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

class ChairCandidates(CreateView):
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

            form = form.save(commit=False)
            form.created_by_id = self.request.user.id
            form.save()
            messages.success(request, 'Succes!, Umejaza taarifa za  mgombea wa board')

            return redirect(self.success_url)
        lists=Voter.objects.all().order_by('memberNo')
        return render(self.request, self.template_name, {'header':self.header,'form': form, 'header': 'Wagombea','lists':lists})
class VotersUpdateView(LoginRequiredMixin,UpdateView):
    model = Voter
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    template_name = 'voters/new_voter.html'
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
            if Voter.objects.filter(~Q(id=self.kwargs['pk'])&Q(Q(mobile__iexact=mobile)|Q(mobile2__iexact=mobile))).exists():
                voterOb=Voter.objects.filter(~Q(id=self.kwargs['pk'])&Q(Q(mobile__iexact=mobile)|Q(mobile2__iexact=mobile))).first()
                mess='Mobile number ('+str(mobile)+') exists to other voters ('+voterOb.name+')'
                return render(self.request, self.template_name,
                              {'header': self.header, 'form': form, 'header': 'Wagombea', 'error': mess})
            if Voter.objects.filter(~Q(id=self.kwargs['pk'])&Q(Q(mobile__iexact=mobile2)|Q(mobile2__iexact=mobile2))).exists():
                voterOb=Voter.objects.filter(~Q(id=self.kwargs['pk'])&Q(Q(mobile__iexact=mobile2)|Q(mobile2__iexact=mobile2))).first()
                mess='Mobile number ('+str(mobile2)+') exists to other voters ('+voterOb.name+')'
                return render(self.request, self.template_name,
                              {'header': self.header, 'form': form, 'header': 'Wagombea', 'error': mess})

            if Voter.objects.filter(~Q(id=self.kwargs['pk'])&Q(memberNo__iexact=memberNo)).exists():
                voterOb=Voter.objects.filter(~Q(id=self.kwargs['pk'])&Q(memberNo__iexact=memberNo)).first()
                mess='Reg number ('+str(memberNo)+') exists to other voters ('+voterOb.name+')'
                return render(self.request, self.template_name,
                              {'header': self.header, 'form': form, 'header': 'Wagombea', 'error': mess})

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
    login_url = reverse_lazy('auths:login_user')
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
                        if Voter.objects.filter(memberNo__iexact=row['MEMBER_NO']).exists():
                            Voter.objects.filter(memberNo__iexact=row['MEMBER_NO']).update(
                                mobile=row['MOBILE'],
                                name=row['NAME'],
                                updated_by_id=request.user.id,
                                updated_on=datetime.datetime.now(),
                                bywhat='import'
                            )
                            html=html+' Updated</td>'

                            coAdd=coAdd+1

                        else:
                            Voter.objects.create(
                                memberNo=row['MEMBER_NO'],
                                mobile=row['MOBILE'],
                                name=row['NAME'],
                                updated_by_id=request.user.id,
                                updated_on=datetime.datetime.now(),
                                bywhat='import'
                            )
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
    login_url = reverse_lazy('auths:login_user')
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
    login_url = reverse_lazy('auths:login_user')
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
    login_url = reverse_lazy('auths:login_user')
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

class SmsList(View):
    template_name='sms/lists.html'
    def get(self,request,*args,**kwargs):
        lists=SmsSent.objects.all().order_by('-created_on')
        return render(request,self.template_name,{'lists':lists,'header':'Sent SMS Lists'})

class SendTestSMs(View):
    def get(self,request,*args,**kwargs):
        return HttpResponse(send_sms('0752350620','Texting from View'));

class Dashboard(View):
    template_name='dashboard/dashboard.html'
    def get(self,request,*args,**kwargs):
        lists=SmsSent.objects.all().order_by('-created_on')
        return render(request,self.template_name,{'lists':lists,'header':'Sent SMS Lists'})
