
from django.urls import include, re_path
from voter.views import *


urlpatterns=[

    re_path(r'^chagua-bodi', BoardVoteView.as_view(), name="chagua_bodi"),
    re_path(r'^', Votings.as_view(), name="voting"),


    ####HOOKS
    ]
