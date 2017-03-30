from django.http import HttpResponse
from django.shortcuts import render

from .models import Fight

def index(request):
    latest_fight_list =  Fight.objects.order_by('-fight_date')[:10]
    context = {
        'latest_fight_list': latest_fight_list
    }

    return render(request, 'sfv/index.html', context)

def detail(request, character_id):
    return HttpResponse("You're looking at character %s." % character_id)

