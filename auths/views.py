from http.client import HTTPException
import csv
from django.core.files.storage import FileSystemStorage
from  datetime import datetime
from django.contrib import messages
from auths import models


def import_roles():
    fs=FileSystemStorage(location='import/permission/')
    file_name='perm.csv'
    counter = 0
    with open(fs.path(file_name), 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        counter = 0
        #return HttpResponse(reader)
        #models.CustPermission.objects.all().delete()
        for row in reader:
            if row['perm_name'] and row['perm_desc'] :
                radio=False
                if row['radio']:
                    if int(row['radio']) == 1:
                        radio=True

                if models.CustPermission.objects.filter(perm_name__iexact=row['perm_name']).exists():

                    models.CustPermission.objects.filter(perm_name__iexact=row['perm_name']).update(
                        perm_name=row['perm_name'],
                        perm_desc=row['perm_desc'],
                        is_single=radio
                    )
                else:
                    models.CustPermission.objects.create(
                    perm_name=row['perm_name'],
                    perm_desc=row['perm_desc'],
                        is_single=radio
                   )
                counter += 1
        return (counter)
    return counter


class User:
    def __init__(self):
        pass

    def add_user(request, user_schema):
        try:
            if type(user_schema) != "dict":
                user_schema = user_schema.dict()
            hash_password =''
            hashed_password = hash_password.decode("utf8")
            print("Schema", user_schema)
            user_schema["password"] = hashed_password
            user = models.User.objects.create(**user_schema)
            user.save()
            return user
        except:
            raise "Internal server Error"

    def get_users(request):
        try:
            users = models.User.objects.filter(is_active=True)
            return users
        except:
            pass

    def update_user(request, user_data):
        if type(user_data) != "dict":
            user_data = dict(user_data)
        user = models.User.objects.filter(id=user_data["id"])
        id=user_data["id"]
        if not models.Staff.objects.filter(user_id=user_data["id"]).exists():
            models.Staff.objects.create(user_id=user_data["id"],full_name=user_data["full_name"],phone_number=user_data["phone_number"])

        user_data.pop("id")
        user.update(**user_data)
        userob=models.User.objects.get(id=id)
        userob.set_password(user_data['password'])
        userob.save()

        return "user updated successfully"

    def get_user_by_username(request, username: str):
        try:
            user = models.User.objects.filter(username=username)
            if user:
                return user[0]
            return None
        except:
            raise HTTPException(
                data={"status_code": 500, "detail": "Internal Server Error"}
            )

    def change_password(request, password_schema):
        try:
            if type(password_schema) != "dict":
                user = user.objects.get(**password_schema)
                user.save()
                return user

        except:
            pass

    def delete_user(request, id: str):
        try:
            user = models.User.objects.filter(id=id)[0]
            if user:
                user.delete()
                return "User has been deleted"
            return "user not found"

        except:
            raise "Internal Server Error"
