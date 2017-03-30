from django.http import HttpResponse
from django.template import loader

from .models import Fight

def index(request):
    latest_fight_list =  Fight.objects.order_by('-fight_date')[:10]
    template = loader.get_template('sfv/index.html')
    context = {
        'latest_fight_list': latest_fight_list
    }

    return HttpResponse(template.render(context, request))

def detail(request, character_id):
    return HttpResponse("You're looking at character %s." % character_id)

