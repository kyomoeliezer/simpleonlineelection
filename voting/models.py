from candidato.models import *
from django.db import models

class BoardVote(BaseDB):
    candidate=models.ForeignKey(BoardCandidate, on_delete=models.CASCADE)
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    is_voted=models.BooleanField(default=True)

    def __str__(self):
        return  self.candidate.candidate_name