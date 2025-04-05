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
from candidato.models import Publishing

from voter.forms import *
def voting_opened_for():
    pub = Publishing.objects.first()
    if pub.startVoting:
        return pub.open_voting_for
    else:
        return ' bb'




def no_check_duplicate_choice(choice,request,no):
    bod1 = request.POST.get('bodi1')
    bod2 = request.POST.get('bodi2')
    bod3 = request.POST.get('bodi3')
    bod4 = request.POST.get('bodi4')
    bod5 = request.POST.get('bodi5')
    bod6 = request.POST.get('bodi6')
    bod7 = request.POST.get('bodi7')

    if bod1 == choice and no != 1:
        return {'inafanana':'Mjumbe No.1'}
    if bod2 == choice and no != 2:
        return {'inafanana':'Mjumbe No.2'}
    if bod3 == choice and no != 3:
        return {'inafanana':'Mjumbe No.3'}
    if bod4 == choice and no != 4:
        return {'inafanana':'Mjumbe No.4'}
    if bod5 == choice and no != 5:
        return {'inafanana':'Mjumbe No.5'}

    if bod6 == choice and no != 6:
        return {'inafanana':'Mjumbe No.6'}
    if bod7 == choice and no != 7:
        return {'inafanana':'Mjumbe No.7'}
    return None

class Votings(LoginRequiredMixin,View):
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    template_name='dashboard_voter.html'
    def get(self,request,*args,**kwargs):
        context={}
        context['pub']=Publishing.objects.first()
        context['voter']=voter=Voter.objects.filter(user_id=request.user.id).first()
        if not voter.is_attended and voter.is_on_meetin_option:
            voter.is_on_meetin_option=False
            voter.save()
            return redirect(reverse('attend_a_meeting_view',kwargs={'pk':voter.id}))
        context['board']=BoardVote.objects.filter(voter_id=voter.id).exists()
        context['committee'] = CommittteeVote.objects.filter(voter_id=voter.id).exists()
        context['chair'] = ChairVote.objects.filter(voter_id=voter.id).exists()
        lists=SmsSent.objects.all().order_by('-created_on')
        return render(request,self.template_name,context)

class BoardVoteView(LoginRequiredMixin,CreateView):
    model = Voter
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    template_name = 'voter/chagua_board.html'
    form_class=ChaguaBodiForm
    success_url = reverse_lazy('voting')
    header='Chagua wajumbe wa bodi'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form']=self.form_class
        context['header']=self.header
        context['voter'] = Voter.objects.filter(user_id=self.request.user.id).first()
        return context

    def post(self, request, *args, **kwargs):
        voter = Voter.objects.filter(user_id=self.request.user.id).first()

        form = self.form_class(request.POST)

        if form.is_valid():
            dataOg=voting_opened_for()
            if not 'Bodi' in  dataOg:
                messages.warning(request,'Subiri Muda wa kura bado/umeisha, sikiliza maelekezo ya mkutano/mwenyekiti wa uchaguzi')

                return redirect(reverse('voting'))


            form1 = form.save(commit=False)
            bod1=request.POST.get('bodi1')
            bod2 = request.POST.get('bodi2')
            bod3 = request.POST.get('bodi3')
            bod4 = request.POST.get('bodi4')
            bod5 = request.POST.get('bodi5')
            bod6 = request.POST.get('bodi6')
            bod7 = request.POST.get('bodi7')
            htmlmsg=''
            found=False
            if no_check_duplicate_choice(bod1,request,1):
                found=True
                htmlmsg=htmlmsg+'<li>Mjumbe No.1 umemchagua kwenye nafasi mbili</li>'

            if no_check_duplicate_choice(bod2, request, 2):
                found = True
                htmlmsg = htmlmsg + '<li>Mjumbe No.2 umemchagua kwenye nafasi mbili</li>'

            if no_check_duplicate_choice(bod3, request, 3):
                found = True
                htmlmsg = htmlmsg + '<li>Mjumbe No.3 umemchagua kwenye nafasi mbili</li>'

            if no_check_duplicate_choice(bod4, request, 4):
                found = True
                htmlmsg = htmlmsg + '<li>Mjumbe No.4 umemchagua kwenye nafasi mbili</li>'

            if no_check_duplicate_choice(bod5, request, 5):
                found = True
                htmlmsg = htmlmsg + '<li>Mjumbe No.5 umemchagua kwenye nafasi mbili</li>'

            if no_check_duplicate_choice(bod6, request, 6):
                print(no_check_duplicate_choice(bod6, request, 6))
                found = True
                htmlmsg = htmlmsg + '<li>Mjumbe No.6 umemchagua kwenye nafasi mbili</li>'

            if no_check_duplicate_choice(bod7, request, 7):
                found = True
                htmlmsg = htmlmsg + '<li>Mjumbe No.7 umemchagua kwenye nafasi mbili</li>'

            if found:
                return render(request,self.template_name,{'voter':voter,'header':self.header,'form': form, 'header': 'Chagua wajumbe wa bodi','htmlmsg':htmlmsg})
            else:

                if Voter.objects.filter(user_id=request.user.id).exists():

                    dataCreate=[]
                    dataCreate.append(BoardVote(voter_id=voter.id,candidate_id=bod1,is_voted=True))
                    dataCreate.append(BoardVote(voter_id=voter.id, candidate_id=bod2, is_voted=True))
                    dataCreate.append(BoardVote(voter_id=voter.id, candidate_id=bod3, is_voted=True))
                    dataCreate.append(BoardVote(voter_id=voter.id, candidate_id=bod4, is_voted=True))
                    dataCreate.append(BoardVote(voter_id=voter.id, candidate_id=bod5, is_voted=True))
                    dataCreate.append(BoardVote(voter_id=voter.id, candidate_id=bod6, is_voted=True))
                    dataCreate.append(BoardVote(voter_id=voter.id, candidate_id=bod7, is_voted=True))

                    if len(dataCreate) == 7:
                        BoardVote.objects.filter(voter_id=voter.id).delete()
                        BoardVote.objects.bulk_create(dataCreate)
                        if BoardVote.objects.filter(voter_id=voter.id).count() == 7:
                            messages.success(request,'Success! Umechagua taari')
                            return redirect(reverse('bodi_yako'))
                        else:
                            messages.warning(request, 'Failed! Umechagua Kuna tatizo tafadhali jaribu tena')
                            return render(request, self.template_name,
                                          {'voter': voter, 'header': self.header, 'form': form,
                                           'header': 'Chagua wajumbe wa bodi','htmlmsg':'Kuna tatizo jaribu tena' })
                    else:
                        return render(request, self.template_name,
                                      {'voter': voter, 'header': self.header, 'form': form,
                                       'header': 'Chagua wajumbe wa bodi', })

                return render(request, self.template_name,
                              {'voter': voter, 'header': self.header, 'form': form, 'header': 'Chagua wajumbe wa bodi', })

        return render(self.request, self.template_name, {'voter':voter,'header':self.header,'form': form, 'header': 'Wagombea'})


class VotedBoardVoteView(LoginRequiredMixin,ListView):
    model = BoardVote
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    template_name = 'voter/board_choice.html'
    success_url = reverse_lazy('voting')
    header='Wajumbe Uliowachagua'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['voter'] = voter = Voter.objects.filter(user_id=self.request.user.id).first()
        context['board'] = board = BoardVote.objects.filter(voter_id=voter.id).all().order_by(
            'candidate__candidate_name')

        if board.count():
            context['umeshapiga']=True


        context['voter'] = Voter.objects.filter(user_id=self.request.user.id).first()

        return context


##############CHAGUA KAMATI
class NewCommitteeVotingView(LoginRequiredMixin,CreateView):
    model = Voter
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    template_name = 'voter/chagua_committee.html'
    form_class=ChaguaCommitteForm
    success_url = reverse_lazy('voting')
    header='Chagua wajumbe wa bodi'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form']=self.form_class
        context['header']=self.header
        context['voter'] = Voter.objects.filter(user_id=self.request.user.id).first()
        return context

    def post(self, request, *args, **kwargs):
        voter = Voter.objects.filter(user_id=self.request.user.id).first()

        form = self.form_class(request.POST)

        if form.is_valid():
            dataOg = voting_opened_for()
            if not 'Kamati' in dataOg:
                messages.warning(request,'Subiri Muda wa kura bado/umeisha, sikiliza maelekezo ya mkutano/mwenyekiti wa uchaguzi')

                return redirect(reverse('voting'))

            form1 = form.save(commit=False)
            bod1=request.POST.get('bodi1')
            bod2 = request.POST.get('bodi2')
            bod3 = request.POST.get('bodi3')

            htmlmsg=''
            found=False
            if no_check_duplicate_choice(bod1,request,1):
                found=True
                htmlmsg=htmlmsg+'<li>Mjumbe No.1 umemchagua kwenye nafasi mbili</li>'

            if no_check_duplicate_choice(bod2, request, 2):
                found = True
                htmlmsg = htmlmsg + '<li>Mjumbe No.2 umemchagua kwenye nafasi mbili</li>'

            if no_check_duplicate_choice(bod3, request, 3):
                found = True
                htmlmsg = htmlmsg + '<li>Mjumbe No.3 umemchagua kwenye nafasi mbili</li>'


            if found:
                return render(request,self.template_name,{'voter':voter,'header':self.header,'form': form, 'header': 'Chagua wajumbe wa bodi','htmlmsg':htmlmsg})
            else:

                if Voter.objects.filter(user_id=request.user.id).exists():

                    dataCreate=[]
                    dataCreate.append(CommittteeVote(voter_id=voter.id,candidate_id=bod1,is_voted=True))
                    dataCreate.append(CommittteeVote(voter_id=voter.id, candidate_id=bod2, is_voted=True))
                    dataCreate.append(CommittteeVote(voter_id=voter.id, candidate_id=bod3, is_voted=True))


                    if len(dataCreate) == 3:
                        CommittteeVote.objects.filter(voter_id=voter.id).delete()
                        CommittteeVote.objects.bulk_create(dataCreate)
                        if CommittteeVote.objects.filter(voter_id=voter.id).count() == 3:
                            messages.success(request,'Success! Umechagua taari')
                            return redirect(reverse('kamati_yako'))
                        else:
                            messages.warning(request, 'Failed!  Kuna tatizo tafadhali jaribu tena')
                            return render(request, self.template_name,
                                          {'voter': voter, 'header': self.header, 'form': form,
                                           'header': 'Chagua wajumbe wa Kamati','htmlmsg':'Kuna tatizo jaribu tena' })
                    else:
                        return render(request, self.template_name,
                                      {'voter': voter, 'header': self.header, 'form': form,
                                       'header': 'Chagua wajumbe wa kamati', })

                return render(request, self.template_name,
                              {'voter': voter, 'header': self.header, 'form': form, 'header': 'Chagua wajumbe wa kamati', })

        return render(self.request, self.template_name, {'voter':voter,'header':self.header,'form': form, 'header': 'Wagombea'})

class VotedCommitteView(LoginRequiredMixin,ListView):
    model = CommittteeVote
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    template_name = 'voter/committee_choice.html'
    header='Wajumbe Kamati Uliowachagua'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['voter'] = voter=Voter.objects.filter(user_id=self.request.user.id).first()
        context['board'] = board = CommittteeVote.objects.filter(voter_id=voter.id).all().order_by('candidate__candidate_name')

        if board.count():
            context['umeshapiga'] = True

        context['voter'] = Voter.objects.filter(user_id=self.request.user.id).first()
        return context

##########chagua chair and Vise Chair
class NewChairViseVotingView(LoginRequiredMixin,CreateView):
    model = Voter
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    template_name = 'voter/chagua_chair.html'
    form_class=ChaguaChairForm
    success_url = reverse_lazy('voting')
    header='Chagua Mwenyekiti na Makamu'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        dataOg = voting_opened_for()

        context['form']=self.form_class
        context['header']=self.header
        context['voter'] = Voter.objects.filter(user_id=self.request.user.id).first()
        return context

    def post(self, request, *args, **kwargs):
        voter = Voter.objects.filter(user_id=self.request.user.id).first()

        form = self.form_class(request.POST)

        if form.is_valid():
            dataOg = voting_opened_for()
            if not 'Mwenyekiti' in dataOg:
                messages.warning(request,'Subiri Muda wa kura bado/umeisha, sikiliza maelekezo ya mkutano/mwenyekiti wa uchaguzi')
                return redirect(reverse('voting'))

            form1 = form.save(commit=False)
            chair=request.POST.get('chair')
            vise = request.POST.get('vise')

            htmlmsg=''
            found=False

            if chair and vise:
                ChairVote.objects.filter(voter_id=voter.id).delete()
                ChairVote.objects.create(
                    vise_id=vise,
                    chair_id=chair,
                    voter_id=voter.id,
                    created_by_id=request.user.id
                )
                if ChairVote.objects.filter(voter_id=voter.id).count() == 1:
                    messages.success(request, 'Success! Umechagua taari')
                    return redirect(reverse('wenyeviti_wako'))
                else:
                    htmlmsg='<li>Failed! Tafadhali rudia tena , ukishindwa contact support</li>'
                    messages.warning(request, 'Failed! Tafadhali rudia tena , ukishindwa contact support')
                    return render(request,self.template_name,{'voter':voter,'header':self.header,'form': form, 'header': 'Chagua mwenyekiti na makamu mwenyekiti','htmlmsg':htmlmsg})

            else:
                htmlmsg = '<li>Failed! Tafadhali rudia tena , ukishindwa contact support</li>'
                messages.warning(request, 'Failed! Tafadhali rudia tena , ukishindwa contact support')
                return render(request, self.template_name, {'voter': voter, 'header': self.header, 'form': form,
                                                            'header': 'Chagua mwenyekiti na makamu mwenyekiti',
                                                            'htmlmsg': htmlmsg})


        return render(self.request, self.template_name, {'voter':voter,'header':self.header,'form': form, 'header': 'Wagombea'})

class VotedChairView(LoginRequiredMixin,ListView):
    model = ChairVote
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    template_name = 'voter/chair_choice.html'
    header='Chair and vise chair'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['voter'] = voter=Voter.objects.filter(user_id=self.request.user.id).first()
        context['chair'] = chair = ChairVote.objects.filter(voter_id=voter.id).all()
        if chair.count():
            context['umeshapiga'] = True

        context['voter'] = Voter.objects.filter(user_id=self.request.user.id).first()
        return context



#############################################
###MATOKEO ##################################
#############################################
class MatokeoVBoard(LoginRequiredMixin,View):
    login_url = reverse_lazy('login_user')
    redirect_field_name = 'next'
    template_name='matokeov/board_matokeo.html'
    def get(self,request,*args,**kwargs):
        context={}

        context['pub'] = Publishing.objects.first()
        context['matokeo'] = matokeo = Matokeo.objects.filter(is_published=True,which='Bodi').order_by('-created_on')
        if matokeo.count() > 0:

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

class MatokeoVCommitte(LoginRequiredMixin,View):
    login_url = reverse_lazy('login_user')
    redirect_field_name = 'next'
    template_name='matokeov/committee_matokeo.html'
    def get(self,request,*args,**kwargs):
        context={}
        context['pub'] = Publishing.objects.first()
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
class MatokeoVChair(LoginRequiredMixin,View):
    login_url = reverse_lazy('login_user')
    redirect_field_name = 'next'
    template_name='matokeov/chair_matokeo.html'
    def get(self,request,*args,**kwargs):
        context = {}
        context['matokeo'] = matokeo = Matokeo.objects.filter(is_published=True, which='Mwenyekiti').order_by('-created_on')
        if matokeo.count() > 0:

            context['chairCount'] = ChairVote.objects.filter(chair_id__isnull=False).count()
            context['viseCount'] = ChairVote.objects.filter(vise_id__isnull=False).count()

            context['chairs'] = ChairCandidate.objects.all()
            context['vise'] = ViseCandidate.objects.all()
        return render(request, self.template_name, context)

class AttendNow(LoginRequiredMixin,View):
    login_url = reverse_lazy('login_user')
    redirect_field_name = 'next'
    def get(self,request,*args,**kwargs):
        context = {}
        voter=Voter.objects.filter(id=self.kwargs['pk']).first()
        if not voter.is_attended:
            voter.attended_at=datetime.datetime.now()
            voter.is_attended=True
            voter.save()
        messages.success(request,'Attend the meeting')
        return redirect(reverse('voting'))

class AttendNowViewOnly(LoginRequiredMixin,View):
    login_url = reverse_lazy('login_user')
    redirect_field_name = 'next'
    def get(self,request,*args,**kwargs):
        context = {}
        voter=Voter.objects.filter(id=self.kwargs['pk']).first()
        template_name='voter/attend_meeting.html'
        return render(request,template_name,{'voter':voter})

############################################
####END MATOKEO#############################
###########################################