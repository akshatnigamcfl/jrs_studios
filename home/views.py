from django.shortcuts import render
from console.models import *
import random

# Create your views here.

def home(request):
    banner_video = Banner_video.objects.all().values()
    if banner_video.exists():
        int = random.randint(0, len(banner_video) - 1)
        return render(request, 'home_adarsh.html', {'data': banner_video[int]})
    return render(request, 'home_adarsh.html')

def home2(request):
    banner_video = Banner_video.objects.all().values()
    if banner_video.exists():
        int = random.randint(0, len(banner_video) - 1)
        return render(request, 'home_2.html', {'data': banner_video[int]})
    return render(request, 'home_2.html')
    

def wedding(request):
    context = Wedding.objects.all().values()
    return render(request, 'wedding.html', {'data':context})

def cinematic(request):
    context = Wedding.objects.all().values()
    return render(request, 'cinematic.html', {'data':context})

def pre_wedding(request):
    context = Pre_Wedding.objects.all().values()
    return render(request, 'pre-wedding.html', {'data':context})

def pre_wedding_view(request, id):
    context = Pre_Wedding.objects.filter(id=id).values()
    recommended = Pre_Wedding.objects.all().values()
    return render(request, 'pre-wedding-view.html', {'data': context, 'recommended': recommended, 'most_recent': recommended})

def events(request):
    context = Events.objects.all().values()
    return render(request, 'events.html', {'data':context}) 


def reels(request):

    reels = Reels.objects.all().values()
    return render(request, 'reels.html', {'reels' : reels})

def team(request):
    return render(request, 'team.html')

def gallery(request):
    return render(request, 'gallery.html')


def booking(request):
    return render(request, 'booking.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


def client_info(request, client_id, client_token):
    try:
        client = Client.objects.filter(id = client_id, client_token = client_token ).values()
        if client.exists():
            data = {}
            for c in client:
                for k,v in c.items():
                    data[k.replace('_', ' ')] = v
            context = {'data': data}
        else:
            context = {'data': 'no data'}
    except:
            context = {'data': 'no data'}

    return render(request, 'client_info.html', context)


def client_info_confirm_booking(request, client_id, client_token):
    try:
        client = Client.objects.filter(id = client_id, client_token = client_token )
        if client.exists():
            # data = {}
            # for c in client:
            #     for k,v in c.items():
            #         data[k.replace('_', ' ')] = v
            context = {'data': client.first()}
        else:
            context = {'data': 'no data'}
    except:
            context = {'data': 'no data'}


    return render(request, 'confirm_booking.html', context)


def scroller_test(request):
    return render(request, 'scroller_test.html')

