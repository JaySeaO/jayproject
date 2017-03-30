from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the SFV index.")

def detail(request, character_id):
    return HttpResponse("You're looking at character %s.", character_id)

