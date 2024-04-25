from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.contrib.auth import authenticate
from django.core.paginator import Paginator
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt import views as jwt_views

from console.models import UserAccount
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta
from django.db.models import Sum

from api.views import get_tokens_for_user
from django.conf import settings
from collections import Counter


from django import template
register = template.Library()

@register.simple_tag()
def multiply(qty, unit_price, *args, **kwargs):
    # you would need to do any localization of the result here
    return qty * unit_price


# Create your views here.

def validate_user(request):
    if request.COOKIES:

        try:
            if AccessToken(request.COOKIES.get('access')):
                token = AccessToken(request.COOKIES.get('access'))
                payload = token.payload
                if 'user_id' in payload:
                    user = UserAccount.objects.filter(id = payload['user_id'])
                    return {'user': user.first(), 'status': user.exists()}
                else :
                    return {'user': None, 'status': False}

            # token_obj = Token.objects.get(key=request.COOKIES.get('access'))
            # current_time = timezone.now()
            # return token_obj.created < current_time - timezone.timedelta(days=1)  # Adjust the timedelta as needed
        except:
            try:
                refreshToken = RefreshToken(str(request.COOKIES.get('refresh')))
                current_time = datetime.utcnow()

                token_created_at = refreshToken.payload['iat']
                token_life = refreshToken.lifetime.total_seconds()
                if token_created_at + token_life < current_time.timestamp():
                    return {'user': None, 'status': False}
                
                else:
                    user = UserAccount.objects.filter(id = refreshToken['user_id']).first()
                    print(user)
                    return {'user':user, 'status': 'access_expired'}
            except:
                return {'user': None, 'status': False}
    else:
        return {'user': None, 'status': False}



def validate_loggedin(request):
    validation = validate_user(request)
    print(validation,validation)    
    if validation['status'] == False:
        return redirect('/console/login')
    elif validation['status'] == 'access_expired':
        # user = validation['user']
        # generate_access = True
        return validation
    elif validation['status'] == True:
        return validation

def regenerateToken(user, context):
    tokens = get_tokens_for_user(user)
    context['token'] = tokens['access']
    return tokens

def regenerateCookies(res,tokens):
    res.set_cookie(key = 'access', value = tokens['access'], expires= settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'], secure= settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'], httponly= settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'], samesite= settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'])
    # res.set_cookie(key = 'refresh', value = tokens['refresh'], expires= settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'], secure= settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'], httponly= settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'], samesite= settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'])
    



def login(request):
    # print('login worked')
    try:
        validation = validate_loggedin(request)
        if validation['status'] == True or validation['status'] == 'access_expired':
            return redirect('/console/dashboard')
        return render(request, 'console_login.html')
    except:
        return render(request, 'console_login.html')

def dashboard(request):
    try:
        validation = validate_loggedin(request)
        if validation['status'] == False:
            return redirect('/console/login')
    except:
            return redirect('/console/login')
    
    # booking = Booking.objects.all()[0:5]
    today = datetime.today().date()
    current_month = datetime.now().month
    current_year = datetime.now().year
    # print('today',today)
    shoot_date = Booking_ShootDate.objects.filter(date__gte=today).order_by('date')[0:10]
    
    # print(booking)
    if shoot_date.exists():
        data = []
        for s in shoot_date:
            # print(s.id)
            booking = Booking.objects.filter(shoot_date=s.id, booking_status__title='confirmed').first()
            data.append({'date': s, 'data': booking})

        
        # print('data')
        # for b in booking:
            # print('b',b.shoot_date.all())
        # p = Paginator(booking, limit)
        # pages = p.page(page)
        # context = {'pages': pages, 'current_page': page}
        total_payment = 0
        total_payment_list = []
        pending_payment = 0
        pending_payment_list = []
        booking = Booking.objects.filter(shoot_date__date__month=current_month,shoot_date__date__year=current_year, booking_status__title='confirmed').distinct()
        # print('booking',booking)
        client = Client.objects.filter(created_at__month=current_month,created_at__year=current_year).count()
        pre_wedding = Pre_Wedding.objects.filter(created_at__month=current_month,created_at__year=current_year).count()
        wedding = Wedding.objects.filter(created_at__month=current_month,created_at__year=current_year).count()
        events = Events.objects.filter(created_at__month=current_month,created_at__year=current_year).count()
        reels = Reels.objects.filter(created_at__month=current_month,created_at__year=current_year).count()
        for b in booking:
            print(b.user)
            total_payment += (b.package.price - b.discount)
            # print(b.package.price - b.discount, b.discount)
            # total_payment -= 
            additional_price = b.shoot_date.all()
            for a in additional_price:
                for c in a.additional_service.all():
                    total_payment += (c.count * c.additional_service.price)

            payment = Payments.objects.filter(user=b.user.id)
            for p in payment:
                pending_payment += p.amount

            total_payment_list.append({'name': b, 'amount': total_payment, 'pending_payment': total_payment-pending_payment})
            # pending_payment_list.append({'name':b, 'amount': pending_payment})
            
            total_payment = 0
            pending_payment= 0



        context = {'data': data, 'payment': {'total_payment': total_payment_list, 'booking': booking, 'client': client, 'pre_wedding': pre_wedding, 'wedding': wedding, 'events': events, 'reels': reels} }
    else:   
        context = {'date': 'no data' ,'data': 'no data'}


    # context = {'data' : 'no data'}
    if validation['status']=='access_expired':
        tokens = regenerateToken(validation['user'],context)
    res = HttpResponse(render(request, 'console_dashboard.html', context))
    if validation['status']=='access_expired':
        regenerateCookies(res, tokens)
    return res




# def dashboard(request):
#     return render(request, 'console_dashboard.html')

def booking(request):
    try:
        validation = validate_loggedin(request)
        if validation['status'] == False:
            return redirect('/console/login')
    except:
            return redirect('/console/login')
    

    try:
        page = int(request.GET.get('page'))
    except:
        page = 1
    
    limit = 5


    try:
        dateSelector = request.GET.get('date')
        if dateSelector==None:
            dateSelector=='today'

        current_month = datetime.now().month
        client = Booking.objects.filter(shoot_date__date__month=current_month).distinct()
        data = []

        print('client',client)

        if client.exists():
            p = Paginator(client, limit)
            pages = p.page(page)
            context = {'pages': pages, 'current_page': page, 'date': current_month}
        else:
            context = {'pages': 'no data', 'current_page': page}
    except:
        context = {'pages': 'no data', 'current_page': page}

        
    # context = {'data' : 'no data'}
    if validation['status']=='access_expired':
        tokens = regenerateToken(validation['user'],context)
    res = HttpResponse(render(request, 'console_booking.html', context))
    if validation['status']=='access_expired':
        regenerateCookies(res, tokens)
    return res


def clients(request):
    try:
        validation = validate_loggedin(request)
        if validation['status'] == False:
            return redirect('/console/login')
    except:
            return redirect('/console/login')
    
    try:
        page = int(request.GET.get('page'))
    except:
        page = 1

    limit = 10
    try:
        client = Client.objects.all().order_by('-id')
        if client.exists():
            p = Paginator(client, limit)
            pages = p.page(page)
            
            context = {'pages': pages, 'current_page': page}
        else:
            context = {'pages': 'no data', 'current_page': page}
    except:
        context = {'pages': 'no data', 'current_page': page}

    if validation['status']=='access_expired':
        tokens = regenerateToken(validation['user'],context)
    res = HttpResponse(render(request, 'console_clients.html', context))
    if validation['status']=='access_expired':
        regenerateCookies(res, tokens)
    return res




def client_edit(request):
    try:
        validation = validate_loggedin(request)
        if validation['status'] == False:
            return redirect('/console/login')
    except:
            return redirect('/console/login')
    
    try:
        id = int(request.GET.get('id'))
        sec = request.GET.get('sec')
        if sec == None:
            sec='client'
    except:
        page = 1
        sec = 'client'
    try:
        client = Client.objects.filter(id = id).values()
        
        if sec == 'client':
            if client.exists():
                data = {}
                for c in client:
                    for k,v in c.items():
                        data[k.replace('_', ' ')] = v

                booking_status = Drp_booking_status.objects.all()
                booking = Booking.objects.filter(user=data['id'])

                context = {'data': data, 'booking_status_list': booking_status, 'booking': booking}
            else:
                context = {'data': 'no data'}
        elif sec == 'booking':
            bookings = Booking.objects.filter(user=client.first()['id'])
            segment = Segment.objects.all()



            # booked_service = []
            # for b in bookings:
            #     booked_service_obj = {}
            #     booked_service_obj['shoot_date'] = str(b.shoot_date)
            #     booked_service_obj['service'] = [c.service_name for c in  b.service.all()]
            #     booked_service_obj['additional_service'] = [c.service_name for c in  b.additional_service.all()]
            #     booked_service.append(booked_service_obj)

    
            if bookings.exists():
                data = []
                for b in bookings:
                    for d in b.shoot_date.all():
                        data.append(str(d.date))
                
                selected_segment = Booking.objects.filter(user=id)

                additional_service = AdditionalService.objects.filter(segment=int(selected_segment.first().package.segment.id))

                # print(d)
                # context = {'booking_data': bookings, "booked_service": booked_service, 'client_data': client.first()}
                context = {'booking_data': data, "booked_service": bookings, 'segment': segment, 'client_data': client.first(), 'pre_selected': {
                           'package': {'id':selected_segment.first().package.id, 'name': selected_segment.first().package.package, 'price': selected_segment.first().package.price },
                        }}
            else:
                context = {'booking_data': '-', 'client_data': client.first()}

        elif sec == 'segment':
            segment = Segment.objects.all()
            selected_segment = Booking.objects.filter(user=id)
            # print(selected_segment)
        
            # print('client.first()', selected_segment.first())
            if selected_segment.exists():
                context = {'segment': segment, 'package': Package.objects.filter(segment=selected_segment.first().package.segment.id),
                       'pre_selected': {
                           'segment':{'id': selected_segment.first().package.segment.id, 'name': selected_segment.first().package.segment.segment.replace('_',' ')},
                           'package': {'id':selected_segment.first().package.id, 'name': selected_segment.first().package.package, 'price': selected_segment.first().package.price },
                           'service': selected_segment.first().package.service.all()
                        },
                           'client_data': client.first()
                    }
                
            else:
                context = {'segment': segment,
                       'pre_selected': {
                        #    'segment':{'id': selected_segment.first().package.segment.id, 'name': selected_segment.first().package.segment.segment.replace('_',' ')},
                        #    'package': {'id':selected_segment.first().package.id, 'name': selected_segment.first().package.package, 'price': selected_segment.first().package.price },
                        #    'service': selected_segment.first().package.service.all()
                        },
                           'client_data': client.first()
                    }

            

        elif sec == 'payment':

            bookings = Booking.objects.filter(user=client.first()['id'])
            payment = Payments.objects.filter(user=client.first()['id']).order_by('-id')
            if bookings.exists():
                context = {'data' : bookings, 'client_data': client.first(), 'payment' :payment}
            else:
                context = {'data' : '-', 'client_data': client.first()}


        elif sec == 'quotation':
            bookings = Booking.objects.filter(user=client.first()['id']).order_by('-id')
            deliverables = Deliverables.objects.filter(trash=False)
            terms_conditions = Terms_Conditions.objects.filter(trash=False)
            if bookings.exists():
                context = {'data' : bookings, 'client_data': client.first(), 'deliverables': deliverables, 'terms_conditions': terms_conditions}
            else:
                context = {'data' : '-', 'client_data': client.first()}
            # context = {'data' : 'no data'}


    except:
        context = {'data': 'no data'}

    if validation['status']=='access_expired':
        tokens = regenerateToken(validation['user'],context)
    res = HttpResponse(render(request, 'console_client_edit.html', context))
    if validation['status']=='access_expired':
        regenerateCookies(res, tokens)
    return res  





def uploads(request):
    try:
        validation = validate_loggedin(request)
        if validation['status'] == False:
            return redirect('/console/login')
    except:
            return redirect('/console/login')
    
    try:
        # id = int(request.GET.get('id'))
        sec = request.GET.get('sec')
        if sec == None:
            sec='pre_wedding'
    except:
        page = 1
        sec = 'pre_wedding'
    try:
        # client = Client.objects.filter(id = id).values()
        # print('client',client)

        if sec == 'pre_wedding':
            try:
                page = int(request.GET.get('page'))
            except:
                page = 1
                limit = 10
            try:
                reels = Pre_Wedding.objects.all().values()
                if reels.exists():
                    p = Paginator(reels, limit)
                    pages = p.page(page)
                    context = {'pages': pages, 'current_page': page}
                else:
                    context = {'pages': 'no data', 'current_page': page}
            except:
                context = {'pages': 'no data', 'current_page': page}


        elif sec == 'wedding':
            try:
                page = int(request.GET.get('page'))
            except:
                page = 1
            limit = 10
            try:
                reels = Wedding.objects.all().values()
                if reels.exists():
                    p = Paginator(reels, limit)
                    pages = p.page(page)
                    context = {'pages': pages, 'current_page': page}
                else:
                    context = {'pages': 'no data', 'current_page': page}
            except:
                context = {'pages': 'no data', 'current_page': page}

        elif sec == 'events':
            try:
                page = int(request.GET.get('page'))
            except:
                page = 1
            limit = 10
            try:
                reels = Events.objects.all().values()
                if reels.exists():
                    p = Paginator(reels, limit)
                    pages = p.page(page)
                    context = {'pages': pages, 'current_page': page}
                else:
                    context = {'pages': 'no data', 'current_page': page}
            except:
                context = {'pages': 'no data', 'current_page': page}

        elif sec == 'reels':
            try:
                page = int(request.GET.get('page'))
            except:
                page = 1
            limit = 10
            try:
                reels = Reels.objects.all().values()
                if reels.exists():
                    p = Paginator(reels, limit)
                    pages = p.page(page)
                    context = {'pages': pages, 'current_page': page}
                else:
                    context = {'pages': 'no data', 'current_page': page}
            except:
                context = {'pages': 'no data', 'current_page': page}
            # context = {'data' : 'no data', 'client_data': client.first()}

    except:
        context = {'data': 'no data'}

    if validation['status']=='access_expired':
        tokens = regenerateToken(validation['user'],context)
    res = HttpResponse(render(request, 'console_uploads.html', context))
    if validation['status']=='access_expired':
        regenerateCookies(res, tokens)
    return res      




# def pre_wedding(request):
#     try:
#         validation = validate_loggedin(request)
#         if validation['status'] == False:
#             return redirect('/console/login')
#     except:
#             return redirect('/console/login')
    
#     try:
#         page = int(request.GET.get('page'))
#     except:
#         page = 1
#     limit = 10
#     try:
#         reels = Pre_Wedding.objects.all().values()
#         if reels.exists():
#             p = Paginator(reels, limit)
#             pages = p.page(page)
#             context = {'pages': pages, 'current_page': page}
#         else:
#             context = {'pages': 'no data', 'current_page': page}
#     except:
#         context = {'pages': 'no data', 'current_page': page}

#     if validation['status']=='access_expired':
#         tokens = regenerateToken(validation['user'],context)
#     res = HttpResponse(render(request, 'console_pre-wedding.html', context))
#     if validation['status']=='access_expired':
#         regenerateCookies(res, tokens)
#     return res



# def wedding(request):
#     try:
#         validation = validate_loggedin(request)
#         if validation['status'] == False:
#             return redirect('/console/login')
#     except:
#             return redirect('/console/login')
    
#     try:
#         page = int(request.GET.get('page'))
#     except:
#         page = 1
#     limit = 10
#     try:
#         reels = Wedding.objects.all().values()
#         if reels.exists():
#             p = Paginator(reels, limit)
#             pages = p.page(page)
#             context = {'pages': pages, 'current_page': page}
#         else:
#             context = {'pages': 'no data', 'current_page': page}
#     except:
#         context = {'pages': 'no data', 'current_page': page}




#     if validation['status']=='access_expired':
#         tokens = regenerateToken(validation['user'],context)
#     res = HttpResponse(render(request, 'console_wedding.html', context))
#     if validation['status']=='access_expired':
#         regenerateCookies(res, tokens)
#     return res


# def events(request):
#     try:
#         validation = validate_loggedin(request)
#         if validation['status'] == False:
#             return redirect('/console/login')
#     except:
#             return redirect('/console/login')

#     try:
#         page = int(request.GET.get('page'))
#     except:
#         page = 1
#     limit = 10
#     try:
#         reels = Events.objects.all().values()
#         if reels.exists():
#             p = Paginator(reels, limit)
#             pages = p.page(page)
#             context = {'pages': pages, 'current_page': page}
#         else:
#             context = {'pages': 'no data', 'current_page': page}
#     except:
#         context = {'pages': 'no data', 'current_page': page}

#     if validation['status']=='access_expired':
#         tokens = regenerateToken(validation['user'],context)
#     res = HttpResponse(render(request, 'console_events.html', context))
#     if validation['status']=='access_expired':
#         regenerateCookies(res, tokens)
#     return res



# def reels(request):
#     try:
#         validation = validate_loggedin(request)
#         if validation['status'] == False:
#             return redirect('/console/login')
#     except:
#             return redirect('/console/login')
    
#     try:
#         page = int(request.GET.get('page'))
#     except:
#         page = 1
#     limit = 10
#     try:
#         reels = Reels.objects.all().values()
#         if reels.exists():
#             p = Paginator(reels, limit)
#             pages = p.page(page)
#             context = {'pages': pages, 'current_page': page}
#         else:
#             context = {'pages': 'no data', 'current_page': page}
#     except:
#         context = {'pages': 'no data', 'current_page': page}
    
#     if validation['status']=='access_expired':
#         tokens = regenerateToken(validation['user'],context)
#     res = HttpResponse(render(request, 'console_reels.html', context))
#     if validation['status']=='access_expired':
#         regenerateCookies(res, tokens)
#     return res


def payments(request):
    try:
        validation = validate_loggedin(request)
        if validation['status'] == False:
            return redirect('/console/login')
    except:
            return redirect('/console/login')
    
    try:    
        page = int(request.GET.get('page'))
    except:
        page = 1

    limit = 10
    offset = int((page - 1)*limit)

    print(limit, offset, 'offset')

    try:
        dateSelector = request.GET.get('date')
        if dateSelector==None or dateSelector=='this_month' :
            dateSelector=='this_month'
            date = datetime.now().month
            client = Payments.objects.filter(date__month=date).distinct().order_by('-id')
        
        elif dateSelector=='this_year':
            date = datetime.now().year
            client = Payments.objects.filter(date__year=date).distinct().order_by('-id')

        elif dateSelector=='today':
            date = datetime.today().date()
            client = Payments.objects.filter(date=date).order_by('-id')
            print('this working', date, client)

        elif dateSelector=='custom':
            date_from = request.GET.get("date_from")
            date_to = request.GET.get("date_to")

            date = {'date_from': date_from,'date_to': date_to } 
            
            start_date = datetime.strptime(date_from, '%Y-%m-%d')
            end_date = datetime.strptime(date_to, '%Y-%m-%d')
            end_date += timedelta(days=1)
            
            client = Payments.objects.filter(date__range=(start_date,end_date)).order_by('-id')
 
        data = []

        if client.exists():
            p = Paginator(client, limit)
            pages = p.page(page)
            context = {'pages': pages, 'current_page': page, 'date': date, 'dateSelector': dateSelector.replace('_',' ')}
        else:
            context = {'pages': 'no data', 'current_page': page}
    except:
        context = {'pages': 'no data', 'current_page': page}





    # try:
    #     invoice = Invoice.objects.all()
    #     if invoice.exists():
    #         p = Paginator(invoice, limit)
    #         pages = p.page(page)
    #         context = {'pages': pages, 'current_page': page}
    #     else:
    #         context = {'pages': 'no data', 'current_page': page}
    # except:
    #     context = {'pages': 'no data', 'current_page': page}





    # context = {'data': 'no data',}
    if validation['status']=='access_expired':
        tokens = regenerateToken(validation['user'],context)
    res = HttpResponse(render(request, 'console_payment.html', context))
    if validation['status']=='access_expired':
        regenerateCookies(res, tokens)
    return res



# def quotation(request):
#     try:
#         validation = validate_loggedin(request)
#         if validation['status'] == False:
#             return redirect('/console/login')
#     except:
#             return redirect('/console/login')
    
#     context = {'data': 'no data',}
#     if validation['status']=='access_expired':
#         tokens = regenerateToken(validation['user'],context)
#     res = HttpResponse(render(request, 'console_quotation.html', context))
#     if validation['status']=='access_expired':
#         regenerateCookies(res, tokens)
#     return res


def invoice_template(request):
    try:
        validation = validate_loggedin(request)
        if validation['status'] == False:
            return redirect('/console/login')
    except:
            return redirect('/console/login')
    
    context = {'data': 'no data',}
    if validation['status']=='access_expired':
        tokens = regenerateToken(validation['user'],context)
    res = HttpResponse(render(request, 'console-layout/invoice.html', context))
    if validation['status']=='access_expired':
        regenerateCookies(res, tokens)
    return res



def administration(request):
    try:
        validation = validate_loggedin(request)
        if validation['status'] == False:
            return redirect('/console/login')
    except:
            return redirect('/console/login')
    
    try:
        # id = int(request.GET.get('id'))
        sec = request.GET.get('sec')
        if sec == None:
            sec='banners'
    except:
        page = 1
        sec = 'banners'
    try:
        # client = Client.objects.filter(id = id).values()
        # print('client',client)

        if sec == 'banners':
            try:
                page = int(request.GET.get('page'))
            except:
                page = 1
                limit = 10
            try:
                banner = Banner_video.objects.all().values()
                showcase_image = Showcase_images.objects.all().values()
                if banner.exists():
                    # p = Paginator(banner, limit)
                    # pages = p.page(page)
                    context = {'banner': banner, 'showcase_image': showcase_image, 'current_page': page}
                else:
                    context = {'pages': 'no data', 'current_page': page}
            except:
                context = {'pages': 'no data', 'current_page': page}


        elif sec == 'packages':
            try:
                page = int(request.GET.get('page'))
            except:
                page = 1
            limit = 10
            try:
                package = Package.objects.all()
                service = Service.objects.all()
                additional_service = AdditionalService.objects.all()
                deliverables = Deliverables.objects.all()
                terms_conditions = Terms_Conditions.objects.all()
                print(package)
                if package.exists():
                    # p = Paginator(reels, limit)
                    # pages = p.page(page)
                    context = {'packages': package, 'service': service, 'additional_service': additional_service, 'deliverables': deliverables, 'terms_conditions': terms_conditions}
                else:
                    context = {'pages': 'no data'}
            except:
                context = {'pages': 'no data', 'current_page': page}


            # context = {'data' : 'no data', 'client_data': client.first()}

    except:
        context = {'data': 'no data'}

    if validation['status']=='access_expired':
        tokens = regenerateToken(validation['user'],context)
    res = HttpResponse(render(request, 'console_administration.html', context))
    if validation['status']=='access_expired':
        regenerateCookies(res, tokens)
    return res      



def team(request):
    try:
        validation = validate_loggedin(request)
        if validation['status'] == False:
            return redirect('/console/login')
    except:
            return redirect('/console/login')
    
    try:
        # id = int(request.GET.get('id'))
        sec = request.GET.get('sec')
        if sec == None:
            sec='members'
    except:
        page = 1
        sec = 'members'
    try:
        # client = Client.objects.filter(id = id).values()
        # print('client',client)

        try:
            page = int(request.GET.get('page'))
        except:
            page = 1
        limit = 10
        
        if sec == 'members':

            try:
                reels = Team_member.objects.all().values()
                if reels.exists():
                    p = Paginator(reels, limit)
                    pages = p.page(page)
                    context = {'data': pages, 'current_page': page}
                else:
                    context = {'data': 'no data', 'current_page': page}
            except:
                context = {'data': 'no data', 'current_page': page}


        elif sec == 'payments':


            try:
                team = Team_member.objects.all().values()
                team_mates_ind=None

                if request.GET.get('team_mate'):
                    team_mate = int(request.GET.get('team_mate'))
                    # print(team)
                    team_mates_ind = Team_member.objects.filter(id=team_mate)
                    # print('else woking')

                    # if tab == 'fund_history':
                    #     tab_instance = fund_history.objects.filter()
                    # elif tab == 'payment_history':
                    #     tab_instance = payments_history.objects.all()

                    # tab_paginator = Paginator(tab_instance, limit)
                    # tab_data = tab_paginator.page(page)

                if not request.GET.get('tab'):
                    tab = 'fund_history'
                else:
                    tab = request.GET.get('tab')

                if team.exists():
                    # print(team)
                    p = Paginator(team, limit)
                    pages = p.page(page)

                    # context = {'data': pages, 'current_page': page}
                    context = {'data': pages, "data_indv":  team_mates_ind if team_mates_ind != None else "no data",'current_page': page}

                    if team_mates_ind != None:
                        context['payment'] = {'fund_history': [t for t in team_mates_ind.first().fund.all().order_by('-id') ], 'payment_history': [t for t in team_mates_ind.first().payments.all().order_by('-id') ]} 

                else:
                    context = {'data': 'no data', "data_indv": 'no data', 'tab_data': 'no data' , 'current_page': page}
            except:
                context = {'data': 'no data', "data_indv": 'no data', 'tab_data': 'no data', 'current_page': page}

            # try:

                # try:
            # if not request.GET.get('tab'):
            #     tab = 'fund_history'
            # else:
            #     tab = request.GET.get('tab')

            # team = Team_member.objects.all().values()

            # if team.exists():
                # p = Paginator(team, limit)
                # pages = p.page(page)

                # if tab == 'fund_history':
                #     tab_instance = fund_history.objects.all()
                # elif tab == 'payment_history':
                #     tab_instance = payments_history.objects.all()

                # tab_paginator = Paginator(tab_instance, limit)
                # tab_data = tab_paginator.page(page)
                # print('tab_data',tab_data)

            #     context = {'data': team, "data_indv":  team_mates_ind if team_mates_ind.exists() else "no data" ,'current_page': page}
            # else:
            #     context = {'data': 'no data', "data_indv": "no data", 'tab_data': 'no data', 'current_page': page}

            # except:
            #     context = {'data': 'no data', "data_indv": "no data", 'tab_data': 'no data', 'current_page': page}
            

    except:
        context = {'data': 'no data'}


    print('context', context)

    if validation['status']=='access_expired':
        tokens = regenerateToken(validation['user'],context)
    res = HttpResponse(render(request, 'console_team.html', context))
    if validation['status']=='access_expired':
        regenerateCookies(res, tokens)
    return res      




def logout(request):
    validation =  validate_loggedin(request)
    print('validation',validation)
    if validation['status'] == True or validation['status'] == 'access_expired':
        resp = HttpResponseRedirect('/console/login')
        resp.delete_cookie('access')
        resp.delete_cookie('refresh')
        resp.delete_cookie('csrftoken')
        return resp
    else:
        return redirect('/console/login')