
from django.urls import include, re_path
from candidato.views import *


urlpatterns=[

    re_path(r'^test-sms', SendTestSMs.as_view(), name="test_sms"),
    re_path(r'^sms', SmsList.as_view(), name="sms"),

    re_path(r'^import-voters', ImportVoters.as_view(), name="import_voter"),
    re_path(r'^import-board', ImportBoard.as_view(), name="import_board"),
    re_path(r'^import-chair', ImportChair.as_view(), name="import_chair"),
    re_path(r'^import-committe', ImportCommittee.as_view(), name="import_committee"),

    re_path(r'^(?P<pk>[0-9]+)/voter/update', VotersUpdateView.as_view(), name="update_voter"),
    re_path(r'^(?P<pk>[0-9]+)/voter/delete', DeleteVoter.as_view(), name="delete_voter"),
    re_path(r'new-voter', VotersRegView.as_view(), name="new_voter"),

    re_path(r'voters-lists', VotersView.as_view(), name="voters"),


    re_path(r'^(?P<pk>[0-9]+)/committee/update', UpdateCommitteeCandidate.as_view(), name="update_committeecandidate"),
    re_path(r'^(?P<pk>[0-9]+)/committee/delete', CommitteeCandidateDelete.as_view(), name="delete_committeecandidate"),
    re_path(r'committee-d', CommitteeCandidatesView.as_view(), name="committee_candidates"),


    re_path(r'^(?P<pk>[0-9]+)/board/update', UpdateBoardCandidate.as_view(), name="update_boardcandidate"),
    re_path(r'^(?P<pk>[0-9]+)/board/delete', BaordCandidateDelete.as_view(), name="delete_boardcandidate"),
    re_path(r'board-d', BoardCandidatesView.as_view(), name="board_candidates"),

    re_path(r'^(?P<pk>[0-9]+)/chair/update', UpdateChairCandidate.as_view(), name="update_chaircandidate"),
    re_path(r'^(?P<pk>[0-9]+)/chair/delete', ChairCandidateDelete.as_view(), name="delete_chaircandidate"),
    re_path(r'', ChairCandidates.as_view(), name="chair_candidates"),


    ####HOOKS
    ]
