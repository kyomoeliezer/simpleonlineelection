import json
import random
import requests
import datetime
from candidato.models import SmsSent

def sms_header():
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic a3lvbW86Tm9raWExMDUjJQ==",
        "Accept": "application/json"
    }
    return headers


def send_sms(mobile,sms):
    datasms=SmsSent.objects.create(
        mob_b4=mobile,sms=sms
    )
    if len(str(mobile)) == 9:
        mob='255'+str(mobile)
    elif len(str(mobile)) == 12:
        mob =  str(mobile)
    elif len(str(mobile)) == 10:
        mob =  '255'+str(mobile)[1:]
    else:
        mob=None
    if mob:
        datasms.mob_aft=mob
        datasms.save()
        dataSend={"from":"SACCO", "to":str(mob),  "text":str(sms), "reference": 'sms-'+str(random.randint(874378478478,874378478478)) }
        datasms.raw_sent=dataSend
        datasms.save()
        url=' https://messaging-service.co.tz/api/sms/v1/text/single'
        response=requests.post(url,data=json.dumps(dataSend),headers=sms_header())
        if response.status_code == 200:
            datasms.raw_response =  response.text
            datasms.save()
            datajson=response.json()
            if 'messages' in datajson.keys():
                datalist=datajson['messages']
                for li in datalist:
                    if 'messageId' in li.keys():
                        datasms.messageId=li['messageId']
                    if 'status' in li.keys():
                        if li['status']['description']:
                            datasms.status = li['status']['description']
                    datasms.save()


        else:
            datasms.raw_response =str(response.content)
            datasms.save()


