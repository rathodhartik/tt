from rest_framework.response import Response
from rest_framework import status

def success(code,message,dataser):
    return {"code":code,"message":message,"Data":dataser}

def unsuccess(code,dataser):
    message = "Data Error...Bad Reuest!"
    return {"code":code,"message":message,"Data":dataser}
