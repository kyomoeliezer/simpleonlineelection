from django.db import models
import os
class BaseDB(models.Model):
    is_active = models.BooleanField(default=True)
    bywhat = models.CharField(max_length=300, verbose_name='ByWhat', null=True)
    created_by = models.ForeignKey("auths.User", on_delete=models.CASCADE, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True

class ChairCandidate(BaseDB):
    memberNo = models.CharField(max_length=300,verbose_name='Member Registration Number')
    candidate_name = models.CharField(max_length=300,verbose_name='Candidate Name')

    def __str__(self):
        return (str(self.memberNo)+' '+self.candidate_name).upper()


class ViseCandidate(BaseDB):
    memberNo = models.CharField(max_length=300,verbose_name='Member Registration No')
    candidate_name = models.CharField(max_length=300,verbose_name='Candidate Name')

    def __str__(self):
        return (str(self.memberNo)+' '+self.candidate_name).upper()


class BoardCandidate(BaseDB):
    memberNo = models.CharField(max_length=300,verbose_name='Member Registration Number')
    candidate_name = models.CharField(max_length=300,verbose_name='Candidate Name')

    def __str__(self):
        return (str(self.memberNo)+' '+self.candidate_name).upper()


class CommitteeCandidate(BaseDB):
    memberNo = models.CharField(max_length=300,verbose_name='Member Registration Number')
    candidate_name = models.CharField(max_length=300,verbose_name='Candidate Name')

    def __str__(self):
        return (str(self.memberNo)+' '+self.candidate_name).upper()


class CommitteeCandidate2(BaseDB):
    memberNo = models.CharField(max_length=300,verbose_name='Member Registration Number')
    candidate_name = models.CharField(max_length=300,verbose_name='Candidate Name')

    def __str__(self):
        return (str(self.memberNo)+' '+self.candidate_name).upper()


class Voter(BaseDB):
    memberNo = models.CharField(max_length=300,verbose_name='Member Reg No.')
    name = models.CharField(max_length=300,verbose_name='Name')
    mobile = models.CharField(max_length=300, verbose_name='Mobile')
    mobile2 = models.CharField(max_length=300, verbose_name='Second Mobile',null=True)
    updated_by = models.ForeignKey("auths.User",related_name='userRelatedUpdate',on_delete=models.CASCADE, null=True, blank=True)
    user=models.ForeignKey("auths.User",related_name='votinglogin',on_delete=models.CASCADE, null=True, blank=True)
    is_attended = models.BooleanField(default=False)
    attended_at = models.DateTimeField(null=True)
    is_on_meetin_option = models.BooleanField(default=True)
    is_special = models.BooleanField(default=False)
    def __str__(self):
        return (str(self.memberNo)+' '+self.name).upper()

class SmsSent(BaseDB):
    sms = models.TextField( verbose_name='Text')
    mob_b4 = models.TextField(verbose_name='Mob_b4',null=True)
    mob_aft = models.TextField(verbose_name='Mob_b4',null=True)
    raw_sent = models.TextField(verbose_name='Sent', null=True)
    raw_response = models.TextField(verbose_name='Sent', null=True)
    messageId = models.TextField(verbose_name='Msg Id', null=True)
    status = models.TextField(verbose_name='Status', null=True)

    def __str__(self):
        return (str(self.mob_b4)+' '+self.sms).upper()



def content_matokeo_bodi(instance, filename):
    ext = filename.split('.')[-1]
    if instance.bodi_file:
        filename = "%s-MATOKEO-YA-BODI.%s" % (instance.id, ext)
    else:
        filename = "%s-MATOKEO-YA-BODI.%s" % (instance.id, ext)

    if instance.bodi_file.storage.exists(instance.bodi_file.name):
        os.remove(os.path.join('matokeo/bodi/', filename))
        if instance.bodi_file:
            filename = "%s-MATOKEO-YA-BODI.%s" % (instance.id, ext)
        else:
            filename = "%s-MATOKEO-YA-BODI.%s" % (instance.id, ext)

        return os.path.join('matokeo/bodi/', filename)
    return os.path.join('matokeo/bodi/', filename)

def content_matokeo_kamati(instance, filename):
    ext = filename.split('.')[-1]
    if instance.kamati_file:
        filename = "%s-MATOKEO-YA-KAMATI.%s" % (instance.id, ext)
    else:
        filename = "%s-MATOKEO-YA-KAMATI.%s" % (instance.id, ext)

    if instance.kamati_file.storage.exists(instance.kamati_file.name):
        os.remove(os.path.join('matokeo/kamati/', filename))
        if instance.kamati_file:
            filename = "%s-MATOKEO-YA-KAMATI.%s" % (instance.id, ext)
        else:
            filename = "%s-MATOKEO-YA-KAMATI.%s" % (instance.id, ext)

        return os.path.join('matokeo/kamati/', filename)
    return os.path.join('matokeo/kamati/', filename)

def content_matokeo_mwenyekiti(instance, filename):
    ext = filename.split('.')[-1]
    if instance.mkiti_file:
        filename = "%s-MATOKEO-YA-MKITI.%s" % (instance.id, ext)
    else:
        filename = "%s-MATOKEO-YA-MKITI.%s" % (instance.id, ext)

    if instance.mkiti_file.storage.exists(instance.mkiti_file.name):
        os.remove(os.path.join('matokeo/kiti/', filename))
        if instance.mkiti_file:
            filename = "%s-MATOKEO-YA-MKITI.%s" % (instance.id, ext)
        else:
            filename = "%s-MATOKEO-YA-MKITI.%s" % (instance.id, ext)

        return os.path.join('matokeo/kiti/', filename)
    return os.path.join('matokeo/kiti/', filename)




class Publishing(BaseDB):
    publish_board_result = models.BooleanField(default=False)
    publish_committee_result = models.BooleanField(default=False)
    publish_chair_result = models.BooleanField(default=False)
    start_attendance_time = models.DateTimeField(null=True)
    end_attendance_time = models.DateTimeField(null=True)
    open_for_special_only=models.BooleanField(default=False)
    open_voting_for=models.CharField(max_length=300,null=True,choices=(('Bodi','Bodi'),('Kamati','Kamati'),('Mwenyekiti','Mwenyekeit')))
    voting_start_time=models.DateTimeField(null=True)
    voting_end_time=models.DateTimeField(null=True)
    def __str__(self):
        return self.publish_board_result

class Matokeo(BaseDB):
    which = models.CharField(max_length=300, choices=(('Bodi','Bodi'),('Kamati','Kamati'),('Mwenyekiti','Mwenyekiti')),verbose_name='Kichwa ')
    title=models.TextField(verbose_name='Kichwa ')
    maelezo = models.TextField(null=True,verbose_name='Maelezo ')
    is_published=models.BooleanField(default=False)
    bodi_file = models.FileField(upload_to='matokeo/bodi/', null=True, verbose_name='File ya bodi')
    mkiti_file = models.FileField(upload_to=content_matokeo_mwenyekiti, null=True, verbose_name='File ya mwenyekiti')
    kamati_file= models.FileField(upload_to=content_matokeo_kamati, null=True, verbose_name='File ya Kamati')
    def __str__(self):
        return self.title
