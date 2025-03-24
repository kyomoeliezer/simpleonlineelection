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

from voter.forms import *


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

class Votings(View):
    template_name='dashboard_voter.html'
    def get(self,request,*args,**kwargs):
        lists=SmsSent.objects.all().order_by('-created_on')
        return render(request,self.template_name,{'lists':lists,'header':'Sent SMS Lists'})

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
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():

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
                return render(request,self.template_name,{'voter':'','header':self.header,'form': form, 'header': 'Chagua wajumbe wa bodi','htmlmsg':htmlmsg})
            else:
                return render(request, self.template_name,
                              {'voter': '', 'header': self.header, 'form': form, 'header': 'Chagua wajumbe wa bodi', })

        return render(self.request, self.template_name, {'header':self.header,'form': form, 'header': 'Wagombea'})