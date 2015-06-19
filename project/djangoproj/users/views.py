# -*- coding: utf-8 -*-
from users.models import User

def getUserRecord(username, password):
    try:
        user = User.objects.get(username=username, password=password)
    except User.DoesNotExist:
        return None
    return user

def saveNewUser(username, password):
    newuser = User(
            username = username,
            password = password,
        )
    newuser.save()
    return newuser
