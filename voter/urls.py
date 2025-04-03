
from django.urls import include, re_path
from voter.views import *


urlpatterns=[

    re_path(r'^chagua-bodi', BoardVoteView.as_view(), name="chagua_bodi"),
    re_path(r'^board-yako', VotedBoardVoteView.as_view(), name="bodi_yako"),
    re_path(r'^chagua-kamati', NewCommitteeVotingView.as_view(), name="chagua_kamati"),
    re_path(r'^kamati-yako', VotedCommitteView.as_view(), name="kamati_yako"),

    re_path(r'^mwenyekiti-chagua', NewChairViseVotingView.as_view(), name="chagua_mwenyeviti"),
    re_path(r'^wenyeviti-wako', VotedChairView.as_view(), name="wenyeviti_wako"),


    #####CHAGUA
    re_path(r'^matokeo-sion-bodi', MatokeoVBoard.as_view(), name="matokeo_voter_bodi"),
    re_path(r'^kamati-ya-uchaguzi-matokeo', MatokeoVCommitte.as_view(), name="matokeo_voter_kamati"),
    re_path(r'^mwenyekiti-wa-chama', MatokeoVChair.as_view(), name="matokeo_voter_mwenyekiti"),
    re_path(r'^(?P<pk>[0-9]+)/', AttendNow.as_view(), name="attend_a_meetingattend_a_meeting"),

    re_path(r'^(?P<pk>[0-9]+)/', AttendNowViewOnly.as_view(), name="attend_a_meeting_view"),




    re_path(r'^', Votings.as_view(), name="voting"),


    ####HOOKS
    ]
