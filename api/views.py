from django.shortcuts import render
from django.contrib.auth import authenticate
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.db.models import Sum

import secrets
import string




from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from .serializer import *
from console.forms import *
# from console.models import *

from datetime import datetime

from io import BytesIO
from xhtml2pdf import pisa


from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import locale

# from weasyprint import HTML

# import pdfkit
from django.template.loader import render_to_string

from django.http import FileResponse


from collections import Counter

import os






def resFun(status,message,data):
    res = Response()
    res.status_code = status
    res.data = {
        'status': status,
        'message': message,
        'data': data,
    }
    return res

# Create your views here.


class IgnoreBearerTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']

            if auth_header.startswith('Bearer'):
                return None
        return super().authenticate(request)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    

# @method_decorator(csrf_exempt, name='csrftoken')
class api_login(GenericAPIView):
    authentication_classes = [IgnoreBearerTokenAuthentication]
    serializer_class = loginSerializer
    def post(self, request, format=None, *args, **kwargs):
        serializer = loginSerializer(data=request.data)
        resp = Response()
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            try:
                UserAccount.objects.get(email=email)
            except:
                return Response({'status': status.HTTP_404_NOT_FOUND,'message':'no user account with this email id','data':[]}, status=status.HTTP_404_NOT_FOUND)
            user = authenticate(email=email, password=password)
            if user != None:

                token = get_tokens_for_user(user)
                # token = Token.objects.get_or_create(user=user)
                resp.status_code = status.HTTP_200_OK
                resp.data = {
                    'data': {'token': token},
                    'message': 'login successful'
                }

                resp.set_cookie(
                    key = settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value=token['access'],
                    expires= settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure= settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly= settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite= settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                resp.set_cookie(
                    key = settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                    value=token['refresh'],
                    expires= settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    secure= settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly= settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite= settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                # res.data = {'token':token, 'message': 'user registered'}
                # res.status_code = status.HTTP_201_CREATED
                # redirect_response = HttpResponseRedirect('/dashboard')
                # redirect_response.set_cookie('')
                # return redirect_response
                
            else:
                resp.status_code = status.HTTP_400_BAD_REQUEST
                resp.data = {
                    'data': [], 
                    'message': 'login failed', 
                }

        else:
            resp.status_code = status.HTTP_400_BAD_REQUEST
            resp.data = {
                'data': [], 
                'message': 'request failed' 
            }
        
        return resp





class upload_reels(CreateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = reelsUploadSerializer
    def post(self, request, format=None, *args, **kwargs):
            print(request.FILES.get('file   '))
        # try:
            file = request.FILES
            res = Response()
            if file:
                if request.FILES.get('file').content_type == 'video/mp4':
                    upload = Reels_Upload_Form(request.POST, request.FILES)
                    if upload.is_valid():
                        upload.save()
                        
                        res.status_code = status.HTTP_200_OK
                        res.data = {
                            'status': status.HTTP_200_OK,
                            'message': 'reel upload successfully',
                            'data': []
                        }                        
                    else:
                        res.status_code = status.HTTP_400_BAD_REQUEST
                        res.data = {
                            'status': status.HTTP_400_BAD_REQUEST,
                            'message': 'request failed',
                            'data': []
                        }
                else:
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'file format not supported',
                        'data': []
                    }
                return res
            


class delete_reels(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Reels_Upload_Form
    def delete(self, request, id, format=None, *args, **kwargs):
        res = Response()
        if request.user.is_admin:
            del_INST = Reels.objects.filter(id = id)
            if del_INST.exists():
                file_location = del_INST.first()
                print('file_location.file',file_location.file)
                if os.path.exists('media/'+str(file_location.file)):
                        os.remove('media/'+str(file_location.file))
                        del_INST.delete()
                        res.status_code = status.HTTP_200_OK
                        res.data = {
                            'status': status.HTTP_200_OK,
                            'data': [],
                            'message': 'deleted successfully'
                            }   
                else:
                    res.status_code = status.HTTP_404_NOT_FOUND
                    res.data = {
                        'status': status.HTTP_404_NOT_FOUND,
                        'data': [],
                        'message': 'file not found'
                        }
            else:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'data': [],
                    'message': 'request failed'
                    }
        else:
            res.status_code = status.HTTP_401_UNAUTHORIZED
            res.data = {
                'status': status.HTTP_401_UNAUTHORIZED,
                'data': [],
                'message': 'you are not authorized to delete this data'
            }
        return res
                

                
            # if upload:
        # except:
        #     print('not uploaded')
        


class upload_pre_wedding(CreateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = Pre_Wedding_Upload_Form_VIDEOFILE
    def post(self, request, format=None, *args, **kwargs):
        # try:
            file = request.FILES
            res = Response()
            if file:
                if request.FILES.get('video_link'):
                    if not 'video' in request.FILES.get('video_link').content_type:
                        res.status_code = status.HTTP_400_BAD_REQUEST
                        res.data = {
                            'status': status.HTTP_400_BAD_REQUEST,
                            'message': 'video format not supported',
                            'data': []
                        }
                        return res
                    
                
                if 'image' in request.FILES.get('cover_picture').content_type:
                    if request.POST.get('is_youtube_video') == 'true':
                        upload = Pre_Wedding_Upload_Form_YOUTUBE_LINK(request.POST, request.FILES)
                    else:
                        upload = Pre_Wedding_Upload_Form_VIDEOFILE(request.POST, request.FILES)

                    if upload.is_valid():
                        upload.save()
                        
                        res.status_code = status.HTTP_200_OK
                        res.data = {
                            'status': status.HTTP_200_OK,
                            'message': 'pre wedding upload successfully',
                            'data': []
                        }                        
                    else:
                        res.status_code = status.HTTP_400_BAD_REQUEST
                        res.data = {
                            'status': status.HTTP_400_BAD_REQUEST,
                            'message': 'request failed',
                            'data': []
                        }
                else:
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'file format not supported',
                        'data': []
                    }
                return res
            

class get_pre_wedding_indv(GenericAPIView):
    serializer_class = PreWeddingSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, id, format=None, *args, **kwargs):
        pre_wedding = Pre_Wedding.objects.filter(id = id)
        res = Response()
        if pre_wedding.exists():

            data = {}
            for k,v in pre_wedding.values().first().items():
                if v =='' or v == None:
                    data[k] = '-'
                else:
                    data[k] = v
            
            serializer = PreWeddingSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            res.status_code = status.HTTP_200_OK
            res.data = {
                'status': status.HTTP_200_OK,
                'message': 'request successful',
                'data': serializer.data,
            }

        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'no pre wedding found with this id',
                'data': [],
            }

        return res
    

class edit_pre_wedding_indv(GenericAPIView):
    serializer_class = Pre_Wedding_Upload_Form_VIDEOFILE
    permission_classes = [IsAuthenticated]
    def put(self, request, id, format=None, *args, **kwargs):

        file = request.FILES
        res = Response()
        pre_wedding = Pre_Wedding.objects.get(id = id)
        if file:
            if request.FILES.get('video_link'):
                if not 'video' in request.FILES.get('video_link').content_type:
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'video format not supported',
                        'data': []
                    }
                    return res
            
            if request.FILES.get('cover_picture'):
                if not 'image' in request.FILES.get('cover_picture').content_type:
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'file format not supported',
                        'data': []
                    }
                    return res

            if request.POST.get('is_youtube_video') == 'true':
                upload = Pre_Wedding_Upload_Form_YOUTUBE_LINK(request.POST, request.FILES, instance=pre_wedding)
            else:
                upload = Pre_Wedding_Upload_Form_VIDEOFILE(request.POST, request.FILES, instance=pre_wedding)

            # else:

        elif not file:
            if request.POST.get('is_youtube_video') == 'true':
                print('if working')
                upload = Pre_Wedding_Upload_Form_YOUTUBE_LINK(request.POST, instance=pre_wedding)
                print('upload',upload)
            else:
                upload = Pre_Wedding_Upload_Form_VIDEOFILE(request.POST, instance=pre_wedding)


        if upload.is_valid():
            upload.save()
            
            res.status_code = status.HTTP_200_OK
            res.data = {
                'status': status.HTTP_200_OK,
                'message': 'pre wedding upload successfully',
                'data': []
            }                        
        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'request failed',
                'data': []
            }

        return res
            

            

class delete_pre_wedding(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Pre_Wedding_Upload_Form_VIDEOFILE
    def delete(self, request, id, format=None, *args, **kwargs):
        res = Response()
        if request.user.is_admin:
            del_INST = Pre_Wedding.objects.filter(id = id)

            print('del_INSTdel_INST',)
            if del_INST.exists():
                file_location = del_INST.first()


                print('file_location.cover_picture',file_location.cover_picture)
                print('file_location.video_link',file_location.video_link)
                if os.path.exists('media/'+str(file_location.cover_picture)):
                    os.remove('media/'+str(file_location.cover_picture))
                    if del_INST.first().is_youtube_video == False:
                        if os.path.exists('media/'+str(file_location.video_link)):
                            os.remove('media/'+str(file_location.video_link))
                        

                    del_INST.delete()
                    res.status_code = status.HTTP_200_OK
                    res.data = {
                        'status': status.HTTP_200_OK,
                        'data': [],
                        'message': 'deleted successfully'
                        }   
                else:
                    res.status_code = status.HTTP_404_NOT_FOUND
                    res.data = {
                        'status': status.HTTP_404_NOT_FOUND,
                        'data': [],
                        'message': 'file not found'
                        }
            else:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'data': [],
                    'message': 'request failed'
                    }
        else:
            res.status_code = status.HTTP_401_UNAUTHORIZED
            res.data = {
                'status': status.HTTP_401_UNAUTHORIZED,
                'data': [],
                'message': 'you are not authorized to delete this data'
            }
        return res

            

class upload_wedding(CreateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = Wedding_Upload_Form_VIDEOFILE
    def post(self, request, format=None, *args, **kwargs):
        # try:
            file = request.FILES
            res = Response()
            if file:
                if request.FILES.get('video_link'):
                    if not 'video' in request.FILES.get('video_link').content_type:
                        res.status_code = status.HTTP_400_BAD_REQUEST
                        res.data = {
                            'status': status.HTTP_400_BAD_REQUEST,
                            'message': 'video format not supported',
                            'data': []
                        }
                        return res


                if 'image' in request.FILES.get('cover_picture').content_type:
                    if request.POST.get('is_youtube_video') == 'true':
                        upload = Wedding_Upload_Form_YOUTUBE_LINK(request.POST, request.FILES)
                    else:
                        upload = Wedding_Upload_Form_VIDEOFILE(request.POST, request.FILES)
                    
                    
                    if upload.is_valid():
                        upload.save()
                        
                        res.status_code = status.HTTP_200_OK
                        res.data = {
                            'status': status.HTTP_200_OK,
                            'message': 'wedding upload successfully',
                            'data': []
                        }                        
                    else:
                        res.status_code = status.HTTP_400_BAD_REQUEST
                        res.data = {
                            'status': status.HTTP_400_BAD_REQUEST,
                            'message': 'request failed',
                            'data': []
                        }
                else:
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'file format not supported',
                        'data': []
                    }
                return res
            

class get_wedding_indv(GenericAPIView):
    serializer_class = WeddingSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, id, format=None, *args, **kwargs):
        wedding = Wedding.objects.filter(id = id)
        res = Response()
        if wedding.exists():

            data = {}
            for k,v in wedding.values().first().items():
                if v =='' or v == None:
                    data[k] = '-'
                else:
                    data[k] = v
            
            serializer = WeddingSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            res.status_code = status.HTTP_200_OK
            res.data = {
                'status': status.HTTP_200_OK,
                'message': 'request successful',
                'data': serializer.data,
            }
        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'no wedding found with this id',
                'data': [],
            }

        return res
    

class edit_wedding_indv(GenericAPIView):
    serializer_class = Wedding_Upload_Form_VIDEOFILE
    permission_classes = [IsAuthenticated]
    def put(self, request, id, format=None, *args, **kwargs):

        file = request.FILES
        res = Response()
        wedding = Wedding.objects.get(id = id)
        if file:
            if request.FILES.get('video_link'):
                if not 'video' in request.FILES.get('video_link').content_type:
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'video format not supported',
                        'data': []
                    }
                    return res
            
            if request.FILES.get('cover_picture'):
                if not 'image' in request.FILES.get('cover_picture').content_type:
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'file format not supported',
                        'data': []
                    }
                    return res
            
            if request.POST.get('is_youtube_video') == 'true':
                upload = Wedding_Upload_Form_YOUTUBE_LINK(request.POST, request.FILES, instance=wedding)
            else:
                upload = Wedding_Upload_Form_VIDEOFILE(request.POST, request.FILES, instance=wedding)

            # else:


        elif not file:
            if request.POST.get('is_youtube_video') == 'true':
                print('if working')
                upload = Wedding_Upload_Form_YOUTUBE_LINK(request.POST, instance=wedding)
                print('upload',upload)
            else:
                upload = Wedding_Upload_Form_VIDEOFILE(request.POST, instance=wedding)
                print(upload)


        if upload.is_valid():
            upload.save()
            
            res.status_code = status.HTTP_200_OK
            res.data = {
                'status': status.HTTP_200_OK,
                'message': 'pre wedding upload successfully',
                'data': []
            }                        
        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'request failed',
                'data': []
            }

        return res

            

class delete_wedding(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Wedding_Upload_Form_VIDEOFILE
    def delete(self, request, id, format=None, *args, **kwargs):
        print("request", request)
        res = Response()
        if request.user.is_admin:
            del_INST = Wedding.objects.filter(id = id)
            if del_INST.exists():
                file_location = del_INST.first()

                print('file_location.cover_picture',file_location.cover_picture)
                if os.path.exists('media/'+str(file_location.cover_picture)):
                    os.remove('media/'+str(file_location.cover_picture))
                    if del_INST.first().is_youtube_video == False:
                        if os.path.exists('media/'+str(file_location.video_link)):
                            os.remove('media/'+str(file_location.video_link))


                # print('file_location.file',file_location.file)
                # if os.path.exists('media/'+str(file_location.file)):
                #         os.remove('media/'+str(file_location.file))
                    del_INST.delete()
                    res.status_code = status.HTTP_200_OK
                    res.data = {
                        'status': status.HTTP_200_OK,
                        'data': [],
                        'message': 'deleted successfully'
                        }   
                else:
                    res.status_code = status.HTTP_404_NOT_FOUND
                    res.data = {
                        'status': status.HTTP_404_NOT_FOUND,
                        'data': [],
                        'message': 'file not found'
                        }
            else:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'data': [],
                    'message': 'request failed'
                    }
        else:
            res.status_code = status.HTTP_401_UNAUTHORIZED
            res.data = {
                'status': status.HTTP_401_UNAUTHORIZED,
                'data': [],
                'message': 'you are not authorized to delete this data'
            }
        return res




            

class upload_events(CreateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = Events_Upload_Form_VIDEOFILE
    def post(self, request, format=None, *args, **kwargs):
        # try:
            file = request.FILES
            res = Response()
            if file:
                if request.FILES.get('video_link'):
                    if not 'video' in request.FILES.get('video_link').content_type:
                        res.status_code = status.HTTP_400_BAD_REQUEST
                        res.data = {
                            'status': status.HTTP_400_BAD_REQUEST,
                            'message': 'video format not supported',
                            'data': []
                        }
                        return res  
                    
                print(request.POST)
                    
                if 'image' in request.FILES.get('cover_picture').content_type:
                    if request.POST.get('is_youtube_video') == 'true':
                        upload = Events_Upload_Form_YOUTUBE_LINK(request.POST, request.FILES)
                    else:
                        upload = Events_Upload_Form_VIDEOFILE(request.POST, request.FILES)

                    if upload.is_valid():
                        upload.save()
                        
                        res.status_code = status.HTTP_200_OK
                        res.data = {
                            'status': status.HTTP_200_OK,
                            'message': 'event upload successfully',
                            'data': []
                        }                        
                    else:
                        res.status_code = status.HTTP_400_BAD_REQUEST
                        res.data = {
                            'status': status.HTTP_400_BAD_REQUEST,
                            'message': 'request failed',
                            'data': []
                        }
                else:
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'file format not supported',
                        'data': []
                    }
                return res
            


class get_events_indv(GenericAPIView):
    serializer_class = EventsSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, id, format=None, *args, **kwargs):
        events = Events.objects.filter(id = id)
        res = Response()
        if events.exists():

            data = {}
            for k,v in events.values().first().items():
                if v =='' or v == None:
                    data[k] = '-'
                else:
                    data[k] = v
            
            serializer = EventsSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            res.status_code = status.HTTP_200_OK
            res.data = {
                'status': status.HTTP_200_OK,
                'message': 'request successful',
                'data': serializer.data,
            }
        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'no events found with this id',
                'data': [],
            }

        return res
    


class edit_events_indv(GenericAPIView):
    serializer_class = Events_Upload_Form_VIDEOFILE
    permission_classes = [IsAuthenticated]
    def put(self, request, id, format=None, *args, **kwargs):

        file = request.FILES
        res = Response()
        events = Events.objects.get(id = id)
        if file:
            if request.FILES.get('video_link'):
                if not 'video' in request.FILES.get('video_link').content_type:
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'video format not supported',
                        'data': []
                    }
                    return res
            
            if request.FILES.get('cover_picture'):
                if 'image' in request.FILES.get('cover_picture').content_type:
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'file format not supported',
                        'data': []
                    }
                    return res                

                
            if request.POST.get('is_youtube_video') == 'true':
                upload = Events_Upload_Form_YOUTUBE_LINK(request.POST, request.FILES, instance=events)
            else:
                upload = Events_Upload_Form_VIDEOFILE(request.POST, request.FILES, instance=events)



        elif not file:
            if request.POST.get('is_youtube_video') == 'true':
                print('if working')
                upload = Events_Upload_Form_YOUTUBE_LINK(request.POST, instance=events)
                print('upload',upload)
            else:
                upload = Events_Upload_Form_VIDEOFILE(request.POST, instance=events)
                print(upload)


        if upload.is_valid():
            upload.save()
            
            res.status_code = status.HTTP_200_OK
            res.data = {
                'status': status.HTTP_200_OK,
                'message': 'pre events upload successfully',
                'data': []
            }                        
        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'request failed',
                'data': []
            }

        return res
            



class delete_events(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Events_Upload_Form_VIDEOFILE
    def delete(self, request, id, format=None, *args, **kwargs):
        print("request", request)
        res = Response()
        if request.user.is_admin:
            del_INST = Events.objects.filter(id = id)
            if del_INST.exists():
                file_location = del_INST.first()

                print('file_location.cover_picture',file_location.cover_picture)
                if os.path.exists('media/'+str(file_location.cover_picture)):
                    os.remove('media/'+str(file_location.cover_picture))
                    if del_INST.first().is_youtube_video == False:
                        if os.path.exists('media/'+str(file_location.video_link)):
                            os.remove('media/'+str(file_location.video_link))

                # print('file_location.file',file_location.file)
                # if os.path.exists('media/'+str(file_location.file)):
                #    os.remove('media/'+str(file_location.file))
                    del_INST.delete()
                    res.status_code = status.HTTP_200_OK
                    res.data = {
                        'status': status.HTTP_200_OK,
                        'data': [],
                        'message': 'deleted successfully'
                        }   
                else:
                    res.status_code = status.HTTP_404_NOT_FOUND
                    res.data = {
                        'status': status.HTTP_404_NOT_FOUND,
                        'data': [],
                        'message': 'file not found'
                        }
            else:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'data': [],
                    'message': 'request failed'
                    }
        else:
            res.status_code = status.HTTP_401_UNAUTHORIZED
            res.data = {
                'status': status.HTTP_401_UNAUTHORIZED,
                'data': [],
                'message': 'you are not authorized to delete this data'
            }
        return res
    

# class vp(GenericAPIView):
#     authentication_classes = [IgnoreBearerTokenAuthentication]
#     # permission_classes =  [IsAuthenticated]
#     def post(self, request, format=None):
#         print('headers', request.headers)
#         print('request', request.data)



class AddClient(CreateAPIView):
    serializer_class = AddClientForm
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None, *args, **kwargs):

        def generate_random_code(length=25):
            alphabet = string.ascii_letters + string.digits
            random_code = ''.join(secrets.choice(alphabet) for _ in range(length))
            return random_code
        
        res = Response()
        data = {}
        data['name'] = request.POST['name']
        data['contact_number'] = request.POST['contact_number']
        data['email_id'] = request.POST['email_id']
        data['source'] = ClientSource.objects.get(title = 'console')
        data['client_token'] = generate_random_code()
        upload = AddClientForm(data)
        if upload.is_valid():
            instance = upload.save()

            print('upload.data',instance.id)

            message = canned_email.objects.get(email_type = 'welcome_email')
            message = message.email
            message = str(message).replace("{{{link}}}", f'<a href="http://127.0.0.1:8000/client-info/{instance.id}/{instance.client_token}">fill more details</a>')

            email_id = upload.cleaned_data['email_id']

            subject = 'Welcome to Jrs Studios!'
            from_email = 'akshatnigamcfl@gmail.com'
            recipient_list = [email_id]
            text = 'email sent from MyDjango'

            # if send_mail(subject, message, from_email, recipient_list):

            email = EmailMultiAlternatives(subject, text, from_email, recipient_list)
            email.attach_alternative(message, 'text/html')
            # email.attach_file('files/uploadFile_0dTGU7A.csv', 'text/csv')
            email.send()

            
            res.status_code = status.HTTP_200_OK
            res.data = {
                'status': status.HTTP_200_OK,
                'message': 'client added successfully',
                'data': []
            }                        
        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'request failed',
                'data': []
            }
        return res
        

class EditClient(CreateAPIView):
    serializer_class = EditClientForms
    permission_classes = [IsAuthenticated]
    def put(self, request, id, format=None, *args, **kwargs):
        res = Response()
        client = Client.objects.filter(id = id).first()
        if request.FILES:
            print(request.FILES)
            formData = EditClientForms(request.POST, request.FILES, instance=client,)
        else:
            formData = EditClientForms(request.POST, instance=client,)

        if formData.is_valid():
           formData.save()
           res.status_code = status.HTTP_200_OK
           res.data={
               'status': status.HTTP_200_OK,
               'message': 'user edited successfully',
               'data': []
           }
        else:
           res.status_code = status.HTTP_400_BAD_REQUEST
           res.data={
               'status': status.HTTP_400_BAD_REQUEST,
               'message': formData.errors,
               'data': []
           }
        return res


class EditClientUserEdit(GenericAPIView):
    serializer_class = EditClientForms
    authentication_classes = [IgnoreBearerTokenAuthentication]
    def put(self, request, id, format=None, *args, **kwargs):
        res = Response()
        client = Client.objects.filter(id = id).first()
        if request.FILES:
            print('request.FILES',request.FILES)
            formData = EditClientForms(request.POST, request.FILES, instance=client)
        else:
            formData = EditClientForms(request.POST, instance=client,)

        if formData.is_valid():
           formData.save()
           res.status_code = status.HTTP_200_OK
           res.data={
               'status': status.HTTP_200_OK,
               'message': 'user edited successfully',
               'data': []
           }
        else:
           res.status_code = status.HTTP_400_BAD_REQUEST
           res.data={
               'status': status.HTTP_400_BAD_REQUEST,
               'message': formData.errors,
               'data': []
           }
        return res



class AddBooking(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddBookingSerializer_RW
    def post(self, request, id, format=None, *args, **kwargs):
        # print('request.data 111',request.data)
        shoot_date = request.data.get('shoot_date')
        # shoot_date = datetime.strptime(shoot_date, '%Y-%m-%d').date()
        # print(shoot_date)
        

        res = Response()
        # if request.data.get('event_type') == 'wedding':
        serializer = AddBookingSerializer_RW(data=request.data)
        # elif request.data.get('event_type') == 'pre_wedding':
        #     serializer = AddBookingPreWeddingSerializer_RW(data=request.data)
        # else:
        #     serializers.ValidationError('event type not valid')
        
        serializer.is_valid(raise_exception=True)
        # print('serializer.data',serializer.data)

        try: 
            user = Booking.objects.filter(user = id)
        except:
            user = Booking.objects.filter(pk__in=[])

        print('user',user)

        if user.exists():
            booking = None
            for d in user.first().shoot_date.all():
                if str(d) == str(serializer.data.get('shoot_date')):
                    booking = d


            if not booking == None:
                print('s1')
                # if serializer.data.get('event_type') == 'wedding':
                service_update_serializer = UpdateBookingServiceSerializer(user.first(),  data={ 'date':serializer.data.get('shoot_date'), 'additional_service': serializer.data.get('additional_service')}, partial=True)
                service_update_serializer.is_valid(raise_exception=True)
                # elif serializer.data.get('event_type') == 'pre_wedding':
                #     print('booing',booking)
                #     service_update_serializer = booking
                #     service_update_serializer.event_type = serializer.data.get('event_type')
                #     service_update_serializer.additional_service.clear()


                service_update_serializer.save()
                res.status_code = status.HTTP_200_OK
                res.data = {
                    'data': [],
                    'message': 'booking updated',
                    'status': status.HTTP_200_OK
                }
                return res

            else:
                print('s2')

                # if serializer.data.get('event_type') == 'wedding':
                service_update_serializer = UpdateBookingServiceSerializer(user.first(),  data={ 'date':serializer.data.get('shoot_date'), 'additional_service': serializer.data.get('additional_service')}, partial=True)
                # elif serializer.data.get('event_type') == 'pre_wedding':
                #     print('jooing')
                #     service_update_serializer = UpdateBookingPreWeddingServiceSerializer(user.first(), data={'date':serializer.data.get('shoot_date'), 'event_type': serializer.data.get('event_type')})
                service_update_serializer.is_valid(raise_exception=True)
                service_update_serializer.save()
                res.status_code = status.HTTP_200_OK
                res.data = {
                    'data': [],
                    'message': 'booking updated',
                    'status': status.HTTP_200_OK
                }
                return res


            # shoot_date__date = 



        #     service_update_serializer.is_valid(raise_exception=True)
        #     print('bookings',service_update_serializer.validated_data['additional_service'])

        #     # bookings.first().service.clear()
        #     bookings.first().additional_service.clear()

        #     # bookings.first().service.add(*service_update_serializer.validated_data['service'])
        #     bookings.first().additional_service.add(*service_update_serializer.validated_data['additional_service'])

        #     res.status_code = status.HTTP_200_OK
        #     res.data = {
        #         'status': status.HTTP_200_OK,
        #         'message': 'booking updated',
        #         'data': []
        #     }


        else:
            print('s3')

            # print('else working')

            try:

                if serializer.data.get('event_type') == 'wedding':
                    shoot_date_serializer = BookingDateSerializer(data={'user': id,'date':serializer.data.get('shoot_date'), 'event_type': serializer.data.get('event_type'), 'additional_service': serializer.data.get('additional_service'), 'package': serializer.data.get('package') }, many=False)

                elif serializer.data.get('event_type') == 'pre_wedding':
                    print('working til here')

                    shoot_date_serializer = BookingDatePreWeddingSerializer(data={'user': id,'date':serializer.data.get('shoot_date'), 'package': Package.objects.get(segment__segment = 'pre_wedding').id, 'event_type': serializer.data.get('event_type') }, many=False)

                # print(shoot_date_serializer)


                if shoot_date_serializer.is_valid():
                    shoot_date_serializer.save()
                # print('shoot_date_serializer',shoot_date_serializer)


                # print('shoot_date_serializer.data',shoot_date_serializer)
                # shoot_date_serializer.add
                # shoot_date = Booking_ShootDate.objects.create(**shoot_date_serializer.data)
                # print(UserAccount.objects.get(id = id))

                # print('shoot_date_serializer',shoot_date_serializer)

                # booking_serializer = AddBookingSerializer(data={'user': id, 'shoot_date': shoot_date_serializer.data ,'package': serializer.data.get('package') })
                # print('booking_serializer',booking_serializer.shoot_date)
                # booking_serializer.shoot_date.add(serializer.data.get('shoot_date'))
                # booking_serializer.is_valid(raise_exception=True)
                # print('worig 2')
                # booking_serializer.save()
                # print('worig 3')
                # print(booking_serializer.data, serializer.data.get('shoot_date'))
                # booking_serializer.shoot_date.add(serializer.data.get('shoot_date'))
                # booking_serializer.shoot_date.add(shoot_date)
                    res = resFun(status.HTTP_200_OK, 'booking added', [])
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST, serializer.errors, [])
            except:
                    res = resFun(status.HTTP_400_BAD_REQUEST, 'segment not selected, first select segment and try again', [])


        return res
    




class CancleBooking(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddBookingSerializer
    def delete(self, request, format=None, *args, **kwargs):
        res = Response()
        try:
            booking = Booking.objects.select_related().filter(shoot_date__date = request.data.get('shoot_date')).values('shoot_date')
        except:
            booking - Booking.objects.get(pk__in=[])
        
        if booking:
            shoot_date = Booking_ShootDate.objects.get(id = booking.first().get('shoot_date')) 
            
            shoot_date.delete()
                # if str(request.data.get('shoot_date')) == str(b.date):
                    # print('ba**************************************',b.data)
                # else:
                    # print('else working')
            # booking.service.clear()
            # booking.additional_service.clear()

            # booking.delete()

            res.status_code = status.HTTP_200_OK
            res.data = {
                'status': status.HTTP_200_OK,
                'message': 'booking cancled successfully',
                'data': [],
            }

        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'no booking found with this date',
                'data': [],
            }
        return res
    

class getBookings(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddBookingSerializer
    def get(self, request, date, page, format=None, *args, **kwargs):

        # print('date',date   )

        # current_month = datetime.now()
        today = datetime.today().date()
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        if date == 'today':
            booking = Booking.objects.filter(shoot_date__date=today).distinct()
        elif date == 'this_month':
            booking = Booking.objects.filter(shoot_date__date__month=current_month).distinct()
        elif date == 'this_year':
            booking = Booking.objects.filter(shoot_date__date__year=current_year).distinct()


        # try:
        #     package = Booking.objects.filter(user = id)
        # except:
        #     package = Booking.objects.filter(pk__in=[])

        if booking.exists():
            data=[]
            for b in booking:
                for sd in b.shoot_date.all():
                    # print(b,sd.date)

                    if date == 'today':
                        if sd.date == today:
                            d={
                                'id': b.id,
                                'date': sd.date,
                                'client_name': b.user.name,
                                'additional_service': [ f'{ass.count} - {ass.additional_service.service_name}' for ass in sd.additional_service.all()]
                            }
                            data.append(d)
                            # break


                    elif date == 'this_month':
                        # for sd in b.shoot_date.all():
                            # print(sd, b)
                        if sd.date.month == current_month:
                            d={
                                'id': b.id,
                                'date': sd.date,
                                'client_name': b.user.name,
                                'additional_service': [ f'{ass.count} - {ass.additional_service.service_name}' for ass in sd.additional_service.all()]
                            }
                            data.append(d)
                            # print('d',d)
                            # break
                            
                    elif date == 'this_year':
                        # for sd in b.shoot_date.all():
                            if sd.date.year == current_year:
                                d={
                                    'id': b.id,
                                    'date': sd.date,
                                    'client_name': b.user.name,
                                    'additional_service': [ f'{ass.count} - {ass.additional_service.service_name}' for ass in sd.additional_service.all()]
                                }
                                data.append(d)
                                # break
                # data.append(d)

            serializer = GetBookingSerializer(data=data, many=True)
            if serializer.is_valid():
                res = resFun(status.HTTP_200_OK, 'request successful',serializer.data)
            else:
                # print(serializer.errors)
                res = resFun(status.HTTP_400_BAD_REQUEST, serializer.errors,[])
        else:
            res = resFun(status.HTTP_204_NO_CONTENT, 'no data found',[])
        
        return res
    

class confirmBooking(GenericAPIView):
    authentication_classes = [IgnoreBearerTokenAuthentication]
    serializer_class = AddBookingSerializer
    def put(self, request, id, format=None, *args, **kwargs):
        
        try:
            booking = Booking.objects.filter(user = id)
        except:
            booking = Booking.objects.filter(user = id)

        if booking.exists():

            try:
                # if Drp_booking_status.objects.get(id=request.data.get('booking_status')).title == 'completed':
                message = canned_email.objects.get(email_type = 'booking_confirmation_email')
                message = message.email
                message = message.replace("{{{client}}}", f"{booking.first().user.name}")

                subject = 'Congratulations! you booking with jrs studios has been confirmed'
                from_email = 'akshatnigamcfl@gmail.com'
                recipient_list = [booking.first().user.email_id]
                text = 'email sent from MyDjango'
                email = EmailMultiAlternatives(subject, text, from_email, recipient_list)
                email.attach_alternative(message, 'text/html')
                # email.attach(f'{booking.first().user.name}', buffer.read(), 'application/pdf')
                email.send()
                res = resFun(status.HTTP_200_OK, 'quotation sent via email',[])

                serializer = UpdateBookingStatusSerializer(booking.first(), data={'booking_status': Drp_booking_status.objects.get(title='confirmed').id }, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    # print('serializer.data',serializer.data)
                    res = resFun(status.HTTP_200_OK,'status updated',[])
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST,'request failed',[])

                # booking.first().booking_status = Drp_booking_status.objects.filter(id=request.data.get('booking_status')).first()
                # booking.first().save()
            except:
                    res = resFun(status.HTTP_400_BAD_REQUEST,'request failed',[])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST,'no data found',[])
        return res

    



class SubmitPackage(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddBookingSerializer
    def put(self, request, id, format=None, *args, **kwargs):
        try:
            package = Booking.objects.filter(user = id)
        except:
            package = Booking.objects.filter(pk__in=[])

        if package.exists():
            try:
                package_RW = request.data.get('package')
                package_obj = Package.objects.get(id=int(package_RW))

                booking = PackageUpdateSerializer(package.first(), data=request.data, partial=True)
                booking.is_valid(raise_exception=True)
                booking.save()
                
                res = resFun(status.HTTP_200_OK,'submitted',booking.data)
            except:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'request failed',[])
        else:
            try:
                client = Client.objects.get(id=id)
            except:
                client = Client.objects.filter(pk__in=[])
            
            if client:
                
                booking_instance = Booking.objects.create(user=client)
                # print()
                client.booking = booking_instance
                client.save()
                

                
                package = Booking.objects.filter(user=id)
                if package.exists():

                    try:
                        package_RW = request.data.get('package')
                        package_obj = Package.objects.get(id=int(package_RW))

                        booking = PackageUpdateSerializer(package.first(), data=request.data, partial=True)
                        booking.is_valid(raise_exception=True)
                        booking.save()

                        res = resFun(status.HTTP_200_OK,'submitted',booking.data)
                    except:
                        res = resFun(status.HTTP_400_BAD_REQUEST, 'request failed',[])
                    
                    # res = resFun(status.HTTP_200_OK, 'Booking Created',[])
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST, 'request failed',[])

            else:
                res = resFun(status.HTTP_400_BAD_REQUEST,'user not found',[])
        return res



class   UpdateBookingStatus(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddBookingSerializer
    def post(self, request, id, format=None, *args, **kwargs):


        print('request.data',request.data)
        
        try:
            booking = Booking.objects.filter(user = id)
        except:
            booking = Booking.objects.filter(user = id)

        if booking.exists():

            if Drp_booking_status.objects.get(id=request.data.get('booking_status')).title == 'completed':
                print('send email')
                message = canned_email.objects.get(email_type = 'welcome_email')
                message = message.email

                message = str(message).replace("{{{link}}}", f'<a href="http://127.0.0.1:8000/client-info/{booking.first().user.id}/{booking.first().user.client_token}">fill more details</a>')

                subject = 'Welcome to Jrs Studios!'
                from_email = 'akshatnigamcfl@gmail.com'
                recipient_list = [booking.first().user.email_id]
                text = 'email sent from MyDjango'

                email = EmailMultiAlternatives(subject, text, from_email, recipient_list)
                email.attach_alternative(message, 'text/html')
                # email.attach(f'{booking.first().user.name}', buffer.read(), 'application/pdf')
                email.send()


                res = resFun(status.HTTP_200_OK, 'quotation sent via email',[])


            serializer = UpdateBookingStatusSerializer(booking.first(), data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()



                # print('serializer.data',serializer.data)

                res = resFun(status.HTTP_200_OK,'status updated',[])

            else:
                res = resFun(status.HTTP_400_BAD_REQUEST,'request failed',[])

            # booking.first().booking_status = Drp_booking_status.objects.filter(id=request.data.get('booking_status')).first()
            # booking.first().save()


        else:
            res = resFun(status.HTTP_400_BAD_REQUEST,'no data found',[])

        return res



class GetAdditionalServices(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetServicesSerializer
    def get(self, request, format=None, *args, **kwargs):
        res = Response()
        service = Service.objects.all().values()
        # serializer = GetServicesSerializer(data=list(service), many=True)
        # if not serializer.is_valid(raise_exception=True):
        #     res.status_code = status.HTTP_400_BAD_REQUEST
        #     res.data = {
        #         'status': status.HTTP_400_BAD_REQUEST,
        #         'message': serializer.errors if serializer.errors else 'request failed',
        #         'data': [] 
        #     }
        #     return res

        additional_service = AdditionalService.objects.filter(trash=False)
        data  = [{'service_name': s.service_name, 'price': s.price,'id':s.id}  for s in additional_service]
        serializer_2 = AdditionalServiceSerializer(data=data, many=True)
        if not serializer_2.is_valid(raise_exception=True):
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': serializer_2.errors if serializer_2.errors else 'request failed',
                'data': [] 
            }
            return res
        
        main_serializer = ServiceMainSerializer(data={'additional_service': serializer_2.data})
        if main_serializer.is_valid(raise_exception=True):
            res.status_code = status.HTTP_200_OK
            res.data = {
                'status': status.HTTP_200_OK,
                'message': 'request successful',
                'data': main_serializer.data
            }
        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': main_serializer.errors if main_serializer.errors else 'request failed',
                'data': [] 
            }
        return res
    


class GetPackages(GenericAPIView):
    serializer_class = GetPackageSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, id, format=None, *args, **kwargs):
        # print('request', request)
        package = Package.objects.all()
        res = Response()
        data = []
        if package.exists():
            try:
                user = Booking.objects.filter(user = id)
            except:
                user = Booking.objects.filter(pk__in=[])

            for s in package:
                if s.segment.segment == 'wedding':
                    service = [str(serv) for serv in s.service.all()]
                    dt = {'id': int(s.id) ,'package': str(s), 'price': int(s.price), 'segment': str(s.segment),'service': service}
                    if user.first():
                        dt['booked_package'] = {'package': user.first().package.package, 'id': user.first().package.id}
                    else:
                        dt['booked_package'] = {'package': [], 'id': []}

                    data.append(dt)


            
            serializer = GetPackageSerializer(data=data, many=True)
            if serializer.is_valid():
                res = resFun(status.HTTP_200_OK, 'request successful', serializer.data)
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, serializer.errors, [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'packages not available', [])
        return res





class GetBookedServices(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetBookedServicesSerializer
    def get(self, request, id, format=None, *args, **kwargs):
        res = Response()
        bookings=Booking.objects.filter(user = id)
        if bookings.exists():
            booked_service = []
            for b in bookings:
                for d in b.shoot_date.all():
                    # print(d)
                    booked_service_obj = {}
                    booked_service_obj['shoot_date'] = {'full_date': str(d.date), 'date': d.date.day, 'month': d.date.month, 'year': d.date.year }
                    # booked_service_obj['booked_service'] = [{'service': c.service_name, 'segment': c.segment} for c in  b.service.all()]
                    booked_service_obj['booked_additional_service'] = [{'additional_service': str(c.additional_service), 'count': int(c.count)} for c in  d.additional_service.all()]
                    booked_service.append(booked_service_obj)
            print('booked_service', booked_service)

            serializer = GetBookedServicesSerializer(data=list(booked_service), many=True)
            serializer.is_valid(raise_exception=True)
            res.status_code = status.HTTP_200_OK
            res.data = {
                'status': status.HTTP_200_OK,
                'message': 'request successful',
                'data': serializer.data,
            }
        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'no booking available',
                'data': [],
            }
        return res
    


def getBookingDetails(b, user_id):
    # print('booking',bookings)
    payment_structure = None
    additionals_total_price = 0
    # for b in bookings:
    packages = []
    # for c in b.service.all():
    #     if c.charges_application == 'complete_shoot':
    #             booking_pricing['services']['complete_shoot'].append({'service': c.service_name, 'price': c.price, 'charges_application': c.charges_application.replace('_', ' ')})
    #     elif c.charges_application == 'per_day':
    #             booking_pricing['services']['per_day'].append({'service': c.service_name, 'price': c.price, 'charges_application': c.charges_application.replace('_', ' ')})
    for c in b.shoot_date.all():
        additional_service_RW = []
        for s in c.additional_service.all():
            # print(s.additional_service.service_name)
            # if s:
            additionals_total_price += int(s.additional_service.price) * int(s.count)
            additional_service_RW.append({'additional_service': s.additional_service.service_name, 'price': s.additional_service.price, 'count': s.count, 'service_total_price': int(s.additional_service.price) * int(s.count) })
        
        # if len(additional_service_RW) > 0:
        packages.append({'date': str(c.date), 'event_type': c.event_type, 'service' : additional_service_RW})
    # if len(packages) > 0:
        # print('bbbbbbbbbb',Package.objects.get(id=b.package.id).service.all())
        payment_structure = {
            'package': b.package.package, 
            'package_price': b.package.price,
            'discount': b.discount,
            'additionals_total_price' : additionals_total_price, 
            'total_price': int(b.package.price) + int(additionals_total_price), 
            'service': [s.service_name for s in Package.objects.get(id=b.package.id).service.all()],
            'additionals': packages,
            'remaining_payment': int((int(b.package.price) + int(additionals_total_price)) ) - int(Payments.objects.filter(user=user_id).aggregate(Sum('amount'))['amount__sum'] if Payments.objects.filter(user=user_id).aggregate(Sum('amount'))['amount__sum'] != None else 0 )
            }
    
    # print('payment_structure',payment_structure)
        # if c.charges_application == 'complete_shoot':
        # booking_pricing['additional_services'].append({'service': c.service_name, 'price': c.price, 'charges_application': c.charges_application.replace('_', ' ')})
        # elif c.charges_application == 'per_day':
        #     booking_pricing['additional_services']['per_day'].append({'service': c.service_name, 'price': c.price, 'charges_application': c.charges_application.replace('_', ' ')})
            
    # service_data = {"additional_services": [], 'total_price': 0 }
    # for k in booking_pricing:
        # print(k)
        # if True:
            # for dt in k['additionals']:
        #         pass
                # for key, value in dt.items():
                #     print(key,value)
                # if key == 'complete_shoot':
                #     unique = set()
                #     for val in value:
                #         unique.add(tuple(sorted(val.items())))
                #     unique_list = [dict(t) for t in unique]
                    
                #     for u in unique_list:
                #         u['count'] = 1 
                #     if len(unique_list) > 0:
                #         for u in unique_list:
                #             service_data['services'].append(u)
                #             service_data['total_price'] = service_data['total_price'] + int(u['price'])
                
                # elif key == 'per_day':
                #     unique = set()
                #     for val in value:
                #         unique.add(tuple(sorted(val.items())))
                #     unique_list = [dict(t) for t in unique]
                #     count = Counter(tuple(sorted(v.items())) for v in value)
                #     service_repeat = []
                #     for d, count in count.items():
                #         service_repeat.append({"service": dict(d)['service'], 'count': count})
                #     for u in unique_list:
                #         for s in service_repeat:
                #             if u['service'] == s['service']:
                #                 u['count'] = s['count']
                #                 u['price'] = int(u['price']) * int(s['count']) 
                #     if len(unique_list) > 0:
                #         for u in unique_list:
                #             service_data['services'].append(u)
                #             service_data['total_price'] = service_data['total_price'] + int(u['price'])
                    
        # elif k=='additional_services':
        #     for key, value in v.items():
        #         if key == 'complete_shoot':
        #             unique = set()
        #             for val in value:
        #                 unique.add(tuple(sorted(val.items())))
        #             unique_list = [dict(t) for t in unique]
        #             for u in unique_list:
        #                 u['count'] = 1
        #             if len(unique_list) > 0:
        #                 for u in unique_list:
        #                     service_data['additional_services'].append(u)
        #                     service_data['total_price'] = service_data['total_price'] + int(u['price'])
        #         elif key == 'per_day':
        #             unique = set()
        #             for val in value:
        #                 unique.add(tuple(sorted(val.items())))
        #             unique_list = [dict(t) for t in unique]
        #             count = Counter(tuple(sorted(v.items())) for v in value)
        #             service_repeat = []
        #             for d, count in count.items():
        #                 service_repeat.append({"service": dict(d)['service'], 'count': count})

        #             for u in unique_list:
        #                 for s in service_repeat:
        #                     if u['service'] == s['service']:
        #                         u['count'] = s['count']
        #                         u['price'] = int(u['price']) * int(s['count']) 
        #             if len(unique_list) > 0:
        #                 for u in unique_list:
        #                     service_data['additional_services'].append(u)
        #                     service_data['total_price'] = service_data['total_price'] + int(u['price'])

    return payment_structure
            



class GetServicesInvoice(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetServicesInvoiceSerializer
    def get(self, request, id, format=None, *args, **kwargs):
        bookings = Booking.objects.get(user = id)
        res = Response()
        if bookings:
            service_data = getBookingDetails(bookings, id)
            print('service_data',service_data)
            serializer = GetServicesInvoiceSerializer(data=service_data)
            serializer.is_valid(raise_exception=True)
            res.status_code = status.HTTP_200_OK
            res.data={
                'status': status.HTTP_200_OK,
                'message': 'request successful',
                'data': serializer.data,
            }
        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data={
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'no booking found',
                'data': [],
            }
        return res

        # context = {'data' : service_data, 'client_data': client.first()}
    






class PaymentSubmit(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InvoiceSerializer
    def post(self, request, id, format=None, *args, **kwargs):

        print(request.data)

        # client = Client.objects.filter(id = id)

        # template = get_template('console-layout/invoice.html')
        # context = {
        #     'payment_date': 27/1/2024
        # }
        # html = template.render(context)
        # res = BytesIO()
        # result = pisa.CreatePDF(html, dest=res)
        # if result.err:
        #     return Response({
        #         'status': status.HTTP_400_BAD_REQUEST,
        #         'error': 'error generating pdf',
        #         'data': []
        #         })
        # res.seek(0)
        # return FileResponse(res, content_type='application/pdf', as_attachment=True, filename=f'{client.first().name}.pdf')

        if request.data.get('payment') == 0:
            res = resFun(status.HTTP_400_BAD_REQUEST, "amount should be more than 0", [])
            return res

    
        res = Response()
        client = Client.objects.get(id = id)
        if client:

            # print('request.data',request.data)

            bookings = Booking.objects.get(user = id)
            service_data = getBookingDetails(bookings, id)

            # if int(request.data.get('discount')) >= int(service_data.get('total_price'))/2:
            #     raise serializers.ValidationError('dicount can not be more than half of the total price')

            invoice = Invoice.objects.filter(user = client.id)

            # if invoice.exists():
            #     raise serializers.ValidationError('already submitted')
            # else:
            #     print(client.first().id)

            # print(request.data.get('discount'))

            # booking = BookingDiscountPriceSerializer(bookings, data={'total_price': service_data.get('total_price'),'package': request.data.get('package')}, partial=True)
            # booking.is_valid(raise_exception=True)
            # if booking.save():

            payment = PaymentsSerializer(data={'amount': request.data.get('payment'), 'payment_mode': request.data.get('payment_mode'), 'payment_note': request.data.get('payment_note'),  'user': client.id})
            payment.is_valid(raise_exception=True)  
            if payment.save():
                invoice = InvoiceSerializer(data={ 'user': client.id, 'payment': payment.data['id'] })
                invoice.is_valid(raise_exception=True)
                if invoice.save():
                    pass
                else:
                    serializers.ValidationError('payment not save')
            else:
                serializers.ValidationError('payment not save')
            # else:
            #     serializers.ValidationError('discount and total price not updated')


            res = resFun(status.HTTP_200_OK,'payment submitted',[])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST,'invalid client id',[])
        return res
    


class GenerateInvoice(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GenerateInvoiceSerializer
    parser_classes = [MultiPartParser, FormParser]
    def get(self, request, id, format=None, *args, **kwargs):
        pass
    

        # template_path = 'your_template.html'
        # template = get_template(template_path)
        # context = {'my_variable': 'some value'}
        # html = template.render(context)
        # response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition'] = 'filename="mypdf.pdf"'
        # pisa.CreatePDF(html, dest=response)
        # return response



        client = Client.objects.filter(id = id)
        if client.exists():

            template = get_template('console-layout/invoice.html')
            context = {
                'payment_date': 27/1/2024,
                'font_link': 'https://fonts.googleapis.com/css2?family=Allura&display=swap'
            }
            html = template.render(context)
            res = BytesIO()
            result = pisa.CreatePDF(html, dest=res)
            if result.err:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'error': 'error generating pdf',
                    'data': []
                    })
            res.seek(0)
            return FileResponse(res, content_type='application/pdf', as_attachment=True, filename=f'{client.first().name}.pdf')
        else:
            res = Response()
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'data':[],
                'message':'client id invalid',
            }
            return res
        


def quotationGenerateFun(client, discount, additional_price):
    buffer = BytesIO()

        # response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition'] = f'attachment; filename="{client.first().name}"'
    page_height = 792
    tb_gap = 42
    logo_gap = 50
    content_gap_out = 30
    content_gap_in = 25
    line_gap = 20
    bullets_gap = 15

    def nextPageAuth(pg_height, r,g,b, font_style, font_size):
        if pg_height <= tb_gap:
            pdf_canvas.showPage()
            pg_height = 792 - tb_gap
            pdf_canvas.setFillColorRGB(255/255, 255/255, 255/255)  # Yellow background
            pdf_canvas.rect(0, 0, letter[0], letter[1], fill=True)
            pdf_canvas.setFont(font_style, font_size)
            pdf_canvas.setFillColorRGB(r, g, b)  # Black text color
        else:
            pass
        return pg_height
    
    def draw_list_with_bullets(pdf_canvas, items, x, y, r,g,b,font_style, font_size, bullet_radius=2, bullet_spacing=15, text_offset=15):
        pg_height = y
        new = True
        for item in items:
            pg_height = nextPageAuth(pg_height,r,g,b, font_style, font_size)
            if new:
                new=False
            else:
                pg_height -= text_offset
            pdf_canvas.setFillColorRGB(r, g, b)
            pdf_canvas.circle(x, pg_height+3, bullet_radius, fill=True,stroke=False)
            pdf_canvas.drawString(x + bullet_spacing, pg_height, item)
        return pg_height
    
    pdf_canvas = canvas.Canvas(buffer, pagesize=letter)
    pdf_canvas.setFillColorRGB(255/255, 255/255, 255/255)  # Yellow background
    pdf_canvas.rect(0, 0, letter[0], letter[1], fill=True)
        # # Add image
        # image_path = 'http://localhost:8000/static/assets/images/bg_fix_1.jpg'  # Replace with the actual path
        # pdf_canvas.drawImage(image_path, 100, 500, width=200, height=200)
        # Add text overlay 
    def drawStringsCustom(a):
        x = a['x']
        y = a['y']
        gap = a['gap']
        font_size = a['font_size']
        content = a['content']
        bullets = a['bullets']
        pdf_canvas = a['pdf_canvas']
        r = a['r']
        g = a['g']
        b = a['b']
        font_style = a['font_style']
        nextPageAuth(y,r,g,b, font_style, font_size)
        if not bullets == False:
            y -= gap
            pdf_canvas.setFont(font_style, font_size)
            pdf_canvas.setFillColorRGB(r,g,b)  # Black text color
            page_height = draw_list_with_bullets(pdf_canvas, content, x, y, r,g,b,font_style, font_size)
            return page_height
            # print('this working')
        else:
            # Helvetica
            y -= gap
            pdf_canvas.setFont(font_style, font_size)
            pdf_canvas.setFillColorRGB(r,g,b)  # Black text color
            pdf_canvas.drawString(x, y, content)
            # page_height = draw_list_with_bullets(pdf_canvas, content, x, y)
        return y
        
    try:
        booking = Booking.objects.filter(user=client.id)
        # print('booking',)
        for b in booking.first().shoot_date.all():
            print(b.date)
            print([a.additional_service.service_name for a in b.additional_service.all()])
    except:
        booking = Booking.objects.filter(pk__in=[])
    
    if booking.exists():
        font_path = 'media/font/Julius_Sans_One/JuliusSansOne-Regular.ttf'  # Update with your actual path
        pdfmetrics.registerFont(TTFont('JuliusSansOne', font_path))
        font_path = 'media/font/Judson/Judson-Regular.ttf'  # Update with your actual path
        pdfmetrics.registerFont(TTFont('Judson-Regular', font_path))
        font_path = 'media/font/Judson/Judson-Bold.ttf'  # Update with your actual path
        pdfmetrics.registerFont(TTFont('Judson-Bold', font_path))
        locale.setlocale(locale.LC_NUMERIC, 'en_IN')
        
        formatted_price = locale.format_string("%.2f", int((booking.first().package.price + additional_price ) - discount), grouping=True)
        formatted_price = formatted_price.rstrip("0").rstrip(".")
            
        text_width = pdf_canvas.stringWidth('Jrs Studios', "JuliusSansOne", 20)
        x_center = (pdf_canvas._pagesize[0] - text_width) / 2
            
        page_height = drawStringsCustom({'x':x_center, 'y':page_height, 'gap': tb_gap, 'font_style':"JuliusSansOne", 'font_size': 23, 'content': 'Jrs Studios', 'bullets': False, 'pdf_canvas':pdf_canvas, "r":102/255,'g':102/255,'b':102/255})
        pdf_canvas.setStrokeColorRGB(102/255, 102/255, 0) 
        pdf_canvas.line(x_center-10, page_height-10, x_center + text_width+20, page_height-10) 
            
        page_height = drawStringsCustom({'x':60, 'y':page_height, 'gap': logo_gap, 'font_style':"Judson-Regular", 'font_size': 13, 'content': f'Dear {client.name.capitalize()},', 'bullets': False, 'pdf_canvas':pdf_canvas, "r":102/255,'g':102/255,'b':102/255})
        
        page_height = drawStringsCustom({'x':60, 'y':page_height, 'gap': content_gap_in, 'font_style':"Judson-Regular", 'font_size': 13, 'content': 'As per your requirement for Wedding Event Shoot, I ‘ve shared below the detailed', 'bullets': False, 'pdf_canvas':pdf_canvas, "r":102/255,'g':102/255,'b':102/255})
        page_height = drawStringsCustom({'x':60, 'y':page_height, 'gap': content_gap_in, 'font_style':"Judson-Regular", 'font_size': 13, 'content': 'quotation for the same', 'bullets': False, 'pdf_canvas':pdf_canvas, "r":102/255,'g':102/255,'b':102/255})
        page_height = drawStringsCustom({'x':60, 'y':page_height, 'gap': content_gap_out, 'font_style':"Judson-Bold", 'font_size': 18, 'content': f'Package Cost: {formatted_price}/-', 'bullets': False, 'pdf_canvas':pdf_canvas, "r":102/255,'g':102/255,'b':102/255})
        page_height = drawStringsCustom({'x':60, 'y':page_height, 'gap': content_gap_out, 'font_style':"Judson-Bold", 'font_size': 13, 'content': 'The package is inclusive of:', 'bullets': False, 'pdf_canvas':pdf_canvas, "r":102/255,'g':102/255,'b':102/255})
        for b in booking.first().shoot_date.all():
            page_height = drawStringsCustom({'x':75, 'y':page_height, 'gap': content_gap_in, 'font_style':"Judson-Bold", 'font_size': 13, 'content': f"{b.date}", 'bullets': False,'pdf_canvas':pdf_canvas, "r":102/255,'g':102/255,'b':102/255})
            page_height = drawStringsCustom({'x':90, 'y':page_height, 'gap': bullets_gap, 'font_style':"Judson-Regular", 'font_size': 11, 'content': [f'{a.count} - {a.additional_service.service_name}' for a in b.additional_service.all()], 'bullets': True , 'pdf_canvas':pdf_canvas, "r":102/255,'g':102/255,'b':102/255})
        page_height = drawStringsCustom({'x':60, 'y':page_height, 'gap': content_gap_out, 'font_style':"Judson-Bold", 'font_size': 13, 'content': 'Cameras & Equipments details:', 'bullets': False,'pdf_canvas':pdf_canvas, "r":102/255,'g':102/255,'b':102/255})
        drawStringsCustom({'x':250, 'y':page_height, 'gap': content_gap_in, 'font_style':"Judson-Regular", 'font_size': 11, 'content': ["Drone","Gimble","Lights","Tripods","Monopads"], 'bullets': True , 'pdf_canvas':pdf_canvas, "r":102/255,'g':102/255,'b':102/255})
        page_height = drawStringsCustom({'x':75, 'y':page_height, 'gap': content_gap_in, 'font_style':"Judson-Regular", 'font_size': 11, 'content': ["Sony a7s3","Sony Mark 4","SONY A7R iii","SONY a7c","Sony MARK 3","ALL SONY G MASTER LENSES"], 'bullets': True , 'pdf_canvas':pdf_canvas, "r":102/255,'g':102/255,'b':102/255})
        page_height = drawStringsCustom({'x':60, 'y':page_height, 'gap': content_gap_out, 'font_style':"Judson-Bold", 'font_size': 13, 'content': 'Production Process:', 'bullets': False,'pdf_canvas':pdf_canvas, "r":102/255,'g':102/255,'b':102/255})
        page_height = drawStringsCustom({'x':75, 'y':page_height, 'gap': content_gap_in, 'font_style':"Judson-Regular", 'font_size': 11, 'content': ["Production(Executing Shoot)","Finalization of Video (Post Production)"], 'bullets': True , 'pdf_canvas':pdf_canvas, "r":102/255,'g':102/255,'b':102/255})


        page_height = drawStringsCustom({'x':60, 'y':page_height, 'gap': content_gap_out, 'font_style':"Judson-Bold", 'font_size': 13, 'content': 'What you get:', 'bullets': False,'pdf_canvas':pdf_canvas, "r":102/255,'g':102/255,'b':102/255})
        page_height = drawStringsCustom({'x':75, 'y':page_height, 'gap': content_gap_in, 'font_style':"Judson-Regular", 'font_size': 11, 'content': [ d.title for d in Deliverables.objects.filter(trash=False)], 'bullets': True , 'pdf_canvas':pdf_canvas, "r":102/255,'g':102/255,'b':102/255})


        page_height = drawStringsCustom({'x':60, 'y':page_height, 'gap': content_gap_out, 'font_style':"Judson-Bold", 'font_size': 13, 'content': 'Terms & Condition:', 'bullets': False,'pdf_canvas':pdf_canvas, "r":102/255,'g':102/255,'b':102/255})
        page_height = drawStringsCustom({'x':75, 'y':page_height, 'gap': content_gap_in, 'font_style':"Judson-Regular", 'font_size': 11, 'content': [ d.title for d in Terms_Conditions.objects.filter(trash=False)], 'bullets': True , 'pdf_canvas':pdf_canvas, "r":102/255,'g':102/255,'b':102/255})
        text_width = pdf_canvas.stringWidth('we will be glad to create memories for you too', "JuliusSansOne", 13)
        x_center = (pdf_canvas._pagesize[0] - text_width) / 2

        page_height = drawStringsCustom({'x':x_center, 'y':page_height, 'gap': content_gap_out+content_gap_out+content_gap_out, 'font_style':"JuliusSansOne", 'font_size': 13, 'content': 'we will be glad to create memories for you too:', 'bullets': False,'pdf_canvas':pdf_canvas, "r":102/255,'g':102/255,'b':102/255})
        pdf_canvas.setStrokeColorRGB(102/255, 102/255, 102/255)
        pdf_canvas.line(x_center+75, page_height-10, x_center + text_width-75, page_height-10)
        text_width = pdf_canvas.stringWidth('hope to see you soon', "JuliusSansOne", 13)
        x_center = (pdf_canvas._pagesize[0] - text_width) / 2
        page_height = drawStringsCustom({'x':x_center, 'y':page_height, 'gap': content_gap_out, 'font_style':"JuliusSansOne", 'font_size': 13, 'content': 'hope to see you soon', 'bullets': False,'pdf_canvas':pdf_canvas, "r":102/255,'g':102/255,'b':102/255})
        
        pdf_canvas.save()
        buffer.seek(0)

        return buffer



class GenerateQuotation(GenericAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class = GenerateQuotationSerializer
    # parser_classes = [MultiPartParser, FormParser]
    def post(self, request, id, format=None, *args, **kwargs):

        booking = Booking.objects.filter(user=id)

        # deliverables = request.data.get('deliverables')
        # terms_conditions = request.data.get('terms_conditions')

        # for d in deliverables:
        #     booking.first().deliverables.add(d)

        # for t in terms_conditions:
        #     booking.first().terms_conditions.add(t)

        serializer = UpdateDiscountSerializer(booking.first(), data={'discount': int(request.data.get('discount'))}, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'discount not valid', [])
            return res

        additional_price=0

        for d in booking.first().shoot_date.all():
            for e in d.additional_service.all():
                additional_price += int(e.additional_service.price*e.count)
                # print(int(e.additional_service.price*e.count))
        
        # print('Additional Price',additional_price)

        client = Client.objects.filter(id = id)
        if client.exists():
          buffer = quotationGenerateFun(client.first(), int(request.data.get('discount')),additional_price )
          response = FileResponse(buffer, content_type='application/pdf', as_attachment=True, filename=f'quotation.pdf')
        else:
            response = resFun(status.HTTP_400_BAD_REQUEST,'booking not found',[])
        return response


        # response = quotationGenerateFun(id)
        # buffer = BytesIO()

        # pdf_canvas = canvas.Canvas(buffer, pagesize=letter)
        # pdf_canvas.setFillColorRGB(255/255, 255/255, 230/255)  # Yellow background
        # pdf_canvas.rect(0, 0, letter[0], letter[1], fill=True)

        # # ... (Add more drawing and content to the PDF)

        # # Save the canvas to BytesIO
        # pdf_canvas.save()

        # # Move the BytesIO cursor to the beginning
        # buffer.seek(0)

        # return FileResponse(buffer, content_type='application/pdf', as_attachment=True, filename=f'quotation.pdf')


        # Return the BytesIO object
        # return buffer
        
        # return response
    

class SaveQuotation(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SaveQuotationSerializer
    def post(self, request, id, format=None, *args, **kwargs):
        try:
            client = Client.objects.filter(id=id)
            if client.exists():
                booking = Booking.objects.get(user=client.first().id)

                if not isinstance(request.data.get('discount'), int):
                    res = resFun(status.HTTP_400_BAD_REQUEST, 'discount should be integer value',[])
                    return res
                    
                print('booking',booking)
                booking.discount = request.data.get('discount')
                booking.save()
                res = resFun(status.HTTP_200_OK, 'save successfully',[])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'invalid user', [])
            return res
        except:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'request failed', [])
            return res


class EmailQuotation(GenericAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class = GenerateQuotationSerializer
    def get(self, request, id,discount, format=None, *args, **kwargs):
        client = Client.objects.filter(id=id)
        if client.exists():

            booking = Booking.objects.filter(user=id)

            serializer = UpdateDiscountSerializer(booking.first(), data={'discount': discount}, partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'discount not valid', [])
                return res

            additional_price=0

            for d in booking.first().shoot_date.all():
                for e in d.additional_service.all():
                    additional_price += int(e.additional_service.price*e.count)
                    # print(int(e.additional_service.price*e.count))

            # print('Additional Price',additional_price)

            buffer = quotationGenerateFun(client.first(), discount, additional_price)

            if buffer:

                message = canned_email.objects.get(email_type = 'send_quotation_email')
                message = message.email

                message = str(message).replace("{{{link}}}", f'<a href="http://127.0.0.1:8000/client-info-confirm-booking/{client.first().id}/{client.first().client_token}"><button>Confirm Booking</button></a>')
                message = message.replace("{{{client}}}", f"{booking.first().user.name}")

                subject = 'Quotation for booking with Jrs studios'
                from_email = 'akshatnigamcfl@gmail.com'
                recipient_list = [client.first().email_id]
                text = 'email sent from MyDjango'

                email = EmailMultiAlternatives(subject, text, from_email, recipient_list)
                email.attach_alternative(message, 'text/html')
                email.attach(f'{client.first().name}', buffer.read(), 'application/pdf')
                email.send()

                res = resFun(status.HTTP_200_OK, 'quotation sent via email',[])
            else:
                res = resFun(status.HTTP_200_OK, 'quotation pdf not generated',[])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST,'Email not sent',[])
        return res



class ConsoleDashboard(GenericAPIView):
    permission_classes =[IsAuthenticated]
    serializer_class = ConsoleDashboardSerializer
    def post(self,request,format=None, *args, **kwargs):

        today = datetime.today().date()
        current_month = datetime.now().month
        current_year = datetime.now().year
        shoot_date = Booking_ShootDate.objects.filter(date__gte=today).order_by('date')[0:10]
    
        if shoot_date.exists():
            data = []
            for s in shoot_date:
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

            if request.data.get('date_selector') == 'today':
                booking = Booking.objects.filter(shoot_date__date = today, booking_status__title='confirmed').distinct()
            # print('booking',booking)
                client = Client.objects.filter(created_at=today).count()
                pre_wedding = Pre_Wedding.objects.filter(created_at=today).count()
                wedding = Wedding.objects.filter(created_at=today).count()
                events = Events.objects.filter(created_at=today).count()
                reels = Reels.objects.filter(created_at=today).count()
                
            # elif request.data.get('date_selector') == 'this_week':
            elif request.data.get('date_selector') == 'this_month':
                booking = Booking.objects.filter(shoot_date__date__month=current_month,shoot_date__date__year=current_year, booking_status__title='confirmed').distinct()
            # print('booking',booking)
                client = Client.objects.filter(created_at__month=current_month,created_at__year=current_year).count()
                pre_wedding = Pre_Wedding.objects.filter(created_at__month=current_month,created_at__year=current_year).count()
                wedding = Wedding.objects.filter(created_at__month=current_month,created_at__year=current_year).count()
                events = Events.objects.filter(created_at__month=current_month,created_at__year=current_year).count()
                reels = Reels.objects.filter(created_at__month=current_month,created_at__year=current_year).count()
            elif request.data.get('date_selector') == 'this_year':
                booking = Booking.objects.filter(shoot_date__date__year=current_year, booking_status__title='confirmed').distinct()
            # print('booking',booking)
                client = Client.objects.filter(created_at__year=current_year).count()
                pre_wedding = Pre_Wedding.objects.filter(created_at__year=current_year).count()
                wedding = Wedding.objects.filter(created_at__year=current_year).count()
                events = Events.objects.filter(created_at__year=current_year).count()
                reels = Reels.objects.filter(created_at__year=current_year).count()




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

            print('client',client)
            print('total_payment_list',total_payment_list)
            print('booking',booking)


            res = resFun(status.HTTP_200_OK, 'request successful', {'data': data, 'payment': {'total_payment': total_payment_list, 'booking': booking, 'client': client, 'pre_wedding': pre_wedding, 'wedding': wedding, 'events': events, 'reels': reels}})
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'request successful',[])

        return res


# class GenerateQuotation(GenericAPIView):
#     permission_classes=[IsAuthenticated]
#     serializer_class = GenerateQuotationSerializer
#     parser_classes = [MultiPartParser, FormParser]
#     def get(self, request, id, format=None, *args, **kwargs):
#         # pass

#         client = Client.objects.filter(id = id)
#         if client.exists():

#             template = get_template('console-layout/quotation.html')
#             context = {
#                 'name': 'Akshat Nigam',
#                 'booking': [{'date':'27/09/2024', 'additionals': ['additional service 1', 'additional service 2', 'additional service 3']}, {'date':'28/09/2024', 'additionals': ['additional service 3', 'additional service 4', 'additional service 5']}],
#                 "equipments": ['Sony a7s3', 'Sony Mark 4', 'SONY A7R iii', 'SONY a7c', 'Sony MARK 3', 'ALL SONY G MASTER LENSES',
#                                'DRONE', 'GIMBAL', 'LIGHTS', 'TRIPODS','MONOPODS'],
#                 "production_process": ['Production(Executing Shoot)', 'Finalization of Video (Post Production)'],
#                 "what_you_get": ['3-4 Wedding Reels for social media post.','1 cinematic teaser ( 60-90 seconds )','Wedding Film (5-6 minutes)','All photographs will be delivered in the digital soft copies.','300 Edited photographs','Algo al app for Photo sharing (Kwicpic)','4-5 hours video will be delivered  in MP4 Format with the resolution of Full HD 1920x1080 pixels.'],
#                 "terms_conditions": [
#                     "All digital data of photos including Candid's and traditional photographs will be delivered in one week.", "For finalising the deal, you must pay us 50%  booking amount for the shoot.", "35% when we deliver you the soft copies of the work.", "Rest 15% after the completion of the whole work."]
#             }
#             html = template.render(context)
#             res = BytesIO()
#             result = pisa.CreatePDF(html, dest=res)
#             if result.err:
#                 return Response({
#                     'status': status.HTTP_400_BAD_REQUEST,
#                     'error': 'error generating pdf',
#                     'data': []
#                     })
#             res.seek(0)
#             return FileResponse(res, content_type='application/pdf', as_attachment=True, filename=f'{client.first().name}.pdf')
#         else:
#             res = Response()
#             res.status_code = status.HTTP_400_BAD_REQUEST
#             res.data = {
#                 'status': status.HTTP_400_BAD_REQUEST,
#                 'data':[],
#                 'message':'client id invalid',
#             }
#             return res

#         # try:
#         # dynamic_data = {
#         #     'name': 'Akshat Nigam'
#         #     # 'booking': [{'date':'27/09/2024', 'additionals': ['additional service 1', 'additional service 2', 'additional service 3']}, {'date':'28/09/2024', 'additionals': ['additional service 3', 'additional service 4', 'additional service 5']}]
#         # }
#         # html_content = render_to_string('console-layout/quotation.html', {'dynamic_data': dynamic_data})
#         # config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
#         # pdf_bytes = pdfkit.from_string(html_content, False, configuration=config)
#         # print(pdf_bytes)
#         # # res = resFun(status.HTTP_200_OK,'wrking',[])
#         # # return res
#         # print(html_content)
#         # res = BytesIO()
#         # result = pisa.CreatePDF(html_content, dest=res)
#         # #     if result.err:
#         # #         return Response({
#         # #             'status': status.HTTP_400_BAD_REQUEST,
#         # #             'error': 'error generating pdf',
#         # #             'data': []
#         # #             })
#         # client = Client.objects.filter(id=id)
#         # res.seek(0)
#         # return FileResponse(res, content_type='application/pdf', as_attachment=True, filename=f'{client.first().name}.pdf')

#             # with BytesIO(pdf_bytes) as pdf_io:
            
#             #     pdf_io.seek(0)


#             #     if client.exists():
#             #         if pdf_io:
#             #             res = FileResponse(pdf_io, content_type='application/pdf', as_attachment=True, filename=f'{client.first().name}.pdf')
#             #         else:
#             #             print("Error: pdf_io object is not available")
#             #             res = None

#         # except Exception as e:
#         #     print(f"An error occurred: {e}")
#         #     res = None

#         # finally:
#         #     if pdf_io:
#         #         pdf_io.close()

#         # return res
        
        


class GetSegmentServicesAdmin(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SegmentSerializer
    def get(self, request, format=None, *args, **kwargs):

        res = Response()
        
        try:
            segment = Segment.objects.all()  
        except:
            segment = Segment.objects.filter(pk__in=[])  

        if segment.exists():
            serializer = SegmentSerializer(data=list(segment.values()), many=True)
            serializer.is_valid(raise_exception=True)
            res.status_code = status.HTTP_200_OK
            res.data = {
                'status': status.HTTP_200_OK,
                'message': 'request successful',
                'data': serializer.data
            }
        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'no data found',
                'data': []
            }

        return res


        


class AddServicesAdmin(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddServiceSerializer
    def post(self, request, format=None, *args, **kwargs):

        res = Response()        
        serializer = AddServiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res.status_code = status.HTTP_200_OK
        res.data = {
            'status': status.HTTP_200_OK,
            'message': 'successfully added',
            'data': [],
        }

        return res
    

class TrashServicesAdmin(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddServiceSerializer
    def delete(self, request, id, format=None, *args, **kwargs):

        res = Response()
        try:
            service = Service.objects.filter(id = id, trash=False)
        except:
            service = Service.objects.filter(pk__in=[])

        
        if service.exists():

            serializer = AddServiceSerializer(service.first(), data={'trash':True}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            res.status_code = status.HTTP_200_OK
            res.data = {
                'status': status.HTTP_200_OK,
                'message': 'moved to trash',
                'data': serializer.data,
            }
        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'service not found',
                'data': [],
            }
        
        return res


class GetServicesAdmin(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetServiceSerializer
    def get(self, request, id, format=None, *args, **kwargs ):
        try:
            service = Service.objects.filter(id=id)
        except:
            service = Service.objects.filter(pk__in=[])

        res = Response()
        if service.exists():

            serializer = GetServiceSerializer(data={'service_name': service.first().service_name, 'segment': { 'id': service.first().segment.id, 'segment': service.first().segment.segment}, 'trash': service.first().trash}, many=False)
            serializer.is_valid(raise_exception=True)

            res.status_code = status.HTTP_200_OK
            res.data = {
                'status': status.HTTP_200_OK,
                'message': 'request successful',
                'data': serializer.data,
            }
        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'service not found',
                'data': [],
            }
        return res
    

class UpdateServicesAdmin(GenericAPIView):
    serializer_class = AddServiceSerializer
    permission_classes = [IsAuthenticated]
    def put(self, request, id, format=None, *args, **kwargs):
        # print('working here')
        try:
            service_CH = Service.objects.filter(service_name=request.data.get('service_name'))
            if service_CH.first().id == id:
                service_CH=Service.objects.filter(pk__in=[])
        except:
            service_CH = Service.objects.filter(pk__in=[])

        if not service_CH.exists():
            try:
                service = Service.objects.filter(id=id)
                print(service)
            except:
                service = Service.objects.filter(pk__in=[])
            # print('service', service)
            if service.exists():
                serializer = AddServiceSerializer(service.first(), data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                res = resFun(status.HTTP_200_OK,'updated successfully', serializer.data)
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST,'no service found', [])
            # return res
        
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST,'service name already exist', [])
        
        return res






class AddAdditionalServicesAdmin(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddAdditionalServiceSerializer
    def post(self, request, format=None, *args, **kwargs):
        res = Response()        
        serializer = AddAdditionalServiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res.status_code = status.HTTP_200_OK
        res.data = {
            'status': status.HTTP_200_OK,
            'message': 'successfully added',
            'data': [],
        }

        return res


class GetAdditionalServicesAdmin(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetDeliverablesSerializer
    def get(self, request, id, format=None, *args, **kwargs):
        try:
            service = AdditionalService.objects.filter(id=id)
        except:
            service = AdditionalService.objects.filter(pk__in=[])

        res = Response()
        if service.exists():

            serializer = GetDeliverablesSerializer(data={'service_name': service.first().service_name, 'price': service.first().price,  'segment': { 'id': service.first().segment.id, 'segment': service.first().segment.segment}, 'trash': service.first().trash}, many=False)
            serializer.is_valid(raise_exception=True)

            res.status_code = status.HTTP_200_OK
            res.data = {
                'status': status.HTTP_200_OK,
                'message': 'request successful',
                'data': serializer.data,
            }
        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'service not found',
                'data': [],
            }
        return res


class UpdateAdditionalServicesAdmin(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddAdditionalServiceSerializer
    def put(self, request, id, format=None, *args, **kwargs):
        try:
            service_CH = AdditionalService.objects.filter(service_name=request.data.get('service_name'))
            if service_CH.first().id == id:
                service_CH=AdditionalService.objects.filter(pk__in=[])
        except:
            service_CH = AdditionalService.objects.filter(pk__in=[])

        if not service_CH.exists():
            try:
                service = AdditionalService.objects.filter(id=id)
                print(service)
            except:
                service = AdditionalService.objects.filter(pk__in=[])
            # print('service', service)
            if service.exists():
                serializer = AddAdditionalServiceSerializer(service.first(), data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                res = resFun(status.HTTP_200_OK,'updated successfully', serializer.data)
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST,'no service found', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST,'service name already exist', [])
        
        return res


class TrashAdditionalServicesAdmin(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddAdditionalServiceSerializer
    def delete(self, request, id, format=None, *args, **kwargs):
        try:
            service = AdditionalService.objects.filter(id = id, trash=False)
        except:
            service = AdditionalService.objects.filter(pk__in=[])

        
        if service.exists():
            serializer = AddServiceSerializer(service.first(), data={'trash':True}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            res = resFun(status.HTTP_200_OK, 'moved to trash', serializer.data)

        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'service not found',
                'data': [],
            }
        
        return res
    

class AddPackageAdmin(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddPackageSerializer
    def post(self, request, format=None, *args, **kwargs):
        try:
            package = Package.objects.get(package=request.data.get('package').lower(),segment = request.data.get('segment'))
            if package:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'package name already exists' ,[])
                return res
        except:
            pass

        serializer = AddPackageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res = resFun(status.HTTP_200_OK, 'package created',[])
        return res


class GetPackageAdmin(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetPackageSerializer
    def get(self, request, id, format=None, *args, **kwargs):

        try:
            package = Package.objects.filter(id=id)
        except:
            package = Package.objects.filter(pk__in=[])

        if package.exists():
            serializer = GetPackageSerializer(data={'id': int(package.first().id) ,'package': package.first().package, 'price': int(package.first().price), 'segment': str(package.first().segment),'service': [s.id for s in package.first().service.all()], 'booked_package': {}}, many=False)
            serializer.is_valid(raise_exception=True)
            res = resFun(status.HTTP_200_OK, 'request successful', serializer.data)
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'request failed', [])


        # serializer = GetPackageSerializer(data=)
        return res
    
class GetAllPackageAdmin(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetPackageSerializer
    def get(self, request, id, format=None,*args, **kwargs):
        try:
            package = Package.objects.filter(segment=id,trash=False)
        except:
            package = Package.objects.filter(pk__in=[])

        if package.exists():
            data = []
            for p in package:
                data.append({'id': int(p.id) ,'package': p.package, 'price': int(p.price), 'segment': str(p.segment),'service': [str(s.service_name) for s in p.service.all()], 'booked_package': {}})
            serializer = GetPackageSerializer(data=data, many=True)
            serializer.is_valid(raise_exception=True)
            res = resFun(status.HTTP_200_OK, 'request successful', serializer.data)
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'package not found', [])
        return res
    

class UpdatePackageAdmin(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddPackageSerializer
    def put(self, request, id,format=None, *args, **kwargs):

        # print('request.data',request.data)

        try:
            package = Package.objects.filter(package = request.data.get('package').lower(),segment = request.data.get('segment'))
            if package.exists():
                if not int(package.first().id) == int(id):
                    res = resFun(status.HTTP_400_BAD_REQUEST, 'package name already exists', [])
                    return res
        except:
            pass

        try:
            package = Package.objects.filter(id=id)
        except:
            package = Package.objects.filter(pk__in=[])

        if package.exists():
            serializer = AddPackageSerializer(package.first(), data=request.data, many=False)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            res = resFun(status.HTTP_200_OK, 'package updated successfully', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'package not found', [])
        return res



# class AddHomeBannerVideoAdmin(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = HomeBannerVideoSerializer
#     def post(self, request, format=None, *args, **kwargs):
#         print(request.data)

#         serializer = HomeBannerVideoSerializer(data=request.data, many=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         res = resFun(status.HTTP_200_OK, 'Banner Video Saved', serializer.data)
#         return res
    

class AddHomeBannerVideoAdmin(GenericAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = BannerVideo_form
    def post(self, request, format=None, *args, **kwargs):
            # print(request.POST)
            # print(request.FILES)
        # try:
            file = request.FILES
            res = Response()
            if file:
                if request.FILES.get('file'):
                    if not 'video' in request.FILES.get('file').content_type:
                        res = resFun(status.HTTP_400_BAD_REQUEST, 'video format not supported',[])
                        return res
                    upload = BannerVideo_form(request.POST, request.FILES)
                    if upload.is_valid():
                        upload.save()
                        res = resFun(status.HTTP_200_OK, 'wedding upload successfully',[])
                    else:
                        res = resFun(status.HTTP_400_BAD_REQUEST, 'request failed',[])
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST, 'file format not supported',[])
                return res
            

class DeleteHomeBannerVideoAdmin(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BannerVideo_form
    def delete(self, request, id, format=None, *args, **kwargs):
        res = Response()
        if request.user.is_admin:
            del_INST = Banner_video.objects.filter(id = id)
            if del_INST.exists():
                file_location = del_INST.first()
                print('file_location.file',file_location.file)
                if os.path.exists('media/'+str(file_location.file)):
                        os.remove('media/'+str(file_location.file))
                        del_INST.delete()

                        res = resFun(status.HTTP_200_OK, 'deleted successfully', [])
                else:
                    res = resFun(status.HTTP_404_NOT_FOUND, 'file not found', [])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'request failed', [])
        else:
            res = resFun(status.HTTP_401_UNAUTHORIZED, 'you are not authorized to delete this data', [])
        return res

                
            # if upload:
        # except:
        #     print('not uploaded')
        
    

class AddShowcaseImageAdmin(GenericAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = Showcase_form
    def post(self, request, format=None, *args, **kwargs):
            file = request.FILES
            res = Response()
            if file:
                if request.FILES.get('file'):
                    if not 'image' in request.FILES.get('file').content_type:
                        res = resFun(status.HTTP_400_BAD_REQUEST, 'image format not supported',[])
                        return res
                    upload = Showcase_form(request.POST, request.FILES)
                    if upload.is_valid():
                        upload.save()
                        res = resFun(status.HTTP_200_OK, 'wedding upload successfully',[])
                        print('this workings')
                    else:
                        res = resFun(status.HTTP_400_BAD_REQUEST, 'request failed',[])
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST, 'file format not supported',[])
                return res
            

class DeleteShowcaseImageAdmin(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Showcase_form
    def delete(self, request, id, format=None, *args, **kwargs):
        res = Response()
        if request.user.is_admin:
            del_INST = Showcase_images.objects.filter(id = id)
            if del_INST.exists():
                file_location = del_INST.first()
                print('file_location.file',file_location.file)
                if os.path.exists('media/'+str(file_location.file)):
                        os.remove('media/'+str(file_location.file))
                        del_INST.delete()

                        res = resFun(status.HTTP_200_OK, 'deleted successfully', [])
                else:
                    res = resFun(status.HTTP_404_NOT_FOUND, 'file not found', [])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'request failed', [])
        else:
            res = resFun(status.HTTP_401_UNAUTHORIZED, 'you are not authorized to delete this data', [])
        return res





class AddTeamMemberAdmin(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamMemberSerializer
    def post(self, request, format=None, *args, **kwargs):
        print('POST', request.data)

        form = TeamMemberSerializer(data=request.data,many=False)
        if form.is_valid(raise_exception=True):
            if form.save():
                res = resFun(status.HTTP_200_OK,'member saved successfully', [])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST,'member not saved', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'request failed',[])
        return res



class GetTeamMemberIndvAdmin(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamMemberSerializer
    def get(self, request, id, format=None, *args, **kwargs):
        try:
            member = Team_member.objects.filter(id=id)
        except:
            member = Team_member.objects.filter(pk__in=[])           
            
        if member.exists():
            serializer = TeamMemberSerializer(data=member.values().first(), many=False)
            serializer.is_valid(raise_exception=True)
            res = resFun(status.HTTP_200_OK,'request successful', serializer.data)
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST,'team member not found', [])
        return res


class UpdateTeamMemberIndvAdmin(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamMemberSerializer
    def put(self, request, id, format=None, *args, **kwargs):
        try:
            member = Team_member.objects.filter(id=id)
        except:
            member = Team_member.objects.filter(pk__in=[])

        if member.exists():
            serializer = TeamMemberSerializer(member.first(), data=request.data ,partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            res = resFun(status.HTTP_200_OK,'request successful', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST,'team member not found', [])
        return res


class DeleteTeamMemberIndvAdmin(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamMemberSerializer
    def delete(self,request, id,format=None, *args, **kwargs):
        try:
            member = Team_member.objects.filter(id=id)
        except:
            member = Team_member.objects.filter(pk__in=[])

        if member.exists():
            member = member.first()
            member.trash = True
            member.save()
            res = resFun(status.HTTP_200_OK,'member moved to trash', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST,'team member not found', [])
        return res
        



class GetDeliverablesAdmin(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetDeliverablesSerializer
    def get(self, request, id, format=None, *args, **kwargs):
        try:
            deliverables = Deliverables.objects.filter(id=id)
        except:
            deliverables = Deliverables.objects.filter(pk__in=[])

        res = Response()
        if deliverables.exists():

            serializer = GetDeliverablesSerializer(data={'title': deliverables.first().title, 'trash': deliverables.first().trash}, many=False)
            serializer.is_valid(raise_exception=True)

            res = resFun(status.HTTP_200_OK,'request successful',serializer.data)
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST,'service not found',[])
        return res
    


class UpdateDeliverables(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetDeliverablesSerializer
    def put(self, request, id, format=None, *args, **kwargs):
        try:
            deliverables_CH = Deliverables.objects.filter(deliverables_name=request.data.get('title').lower())
            if deliverables_CH.first().id == id:
                deliverables_CH=Deliverables.objects.filter(pk__in=[])
        except:
            deliverables_CH = Deliverables.objects.filter(pk__in=[])

        if not deliverables_CH.exists():
            try:
                deliverables = Deliverables.objects.filter(id=id)
            except:
                deliverables = Deliverables.objects.filter(pk__in=[])
            # print('deliverables', deliverables)
            if deliverables.exists():
                serializer = GetDeliverablesSerializer(deliverables.first(), data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    res = resFun(status.HTTP_200_OK,'updated successfully', serializer.data)
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST, serializer.errors['title'] if serializer.errors['title'] else serializer.errors , [])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST,'no deliverables found', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST,'deliverables name already exist', [])
        return res



class TrashDeliverablesAdmin(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetDeliverablesSerializer
    def delete(self, request, id, format=None, *args, **kwargs):
        try:
            deliverables = Deliverables.objects.filter(id = id, trash=False)
        except:
            deliverables = Deliverables.objects.filter(pk__in=[])

        
        if deliverables.exists():
            serializer = GetDeliverablesSerializer(deliverables.first(), data={'trash':True}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            res = resFun(status.HTTP_200_OK, 'moved to trash', serializer.data)
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'deliverables not found', [])
        return res
    


class AddDeliverablesAdmin(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetDeliverablesSerializer
    def post(self, request, format=None, *args, **kwargs):
        res = Response()        
        serializer = GetDeliverablesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = resFun(status.HTTP_200_OK, 'successfully added',[])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, serializer.errors,[])
        return res










class GetTermsConditionAdmin(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetTermsConditionSerializer
    def get(self, request, id, format=None, *args, **kwargs):
        try:
            terms_conditions = Terms_Conditions.objects.filter(id=id)
        except:
            terms_conditions = Terms_Conditions.objects.filter(pk__in=[])

        res = Response()
        if terms_conditions.exists():

            serializer = GetTermsConditionSerializer(data={'title': terms_conditions.first().title, 'trash': terms_conditions.first().trash}, many=False)
            serializer.is_valid(raise_exception=True)

            res = resFun(status.HTTP_200_OK,'request successful',serializer.data)
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST,'service not found',[])
        return res
    


class UpdateTermsCondition(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetTermsConditionSerializer
    def put(self, request, id, format=None, *args, **kwargs):
        try:
            terms_conditions_CH = Terms_Conditions.objects.filter(terms_conditions_name=request.data.get('title').lower())
            if terms_conditions_CH.first().id == id:
                terms_conditions_CH=Terms_Conditions.objects.filter(pk__in=[])
        except:
            terms_conditions_CH = Terms_Conditions.objects.filter(pk__in=[])

        if not terms_conditions_CH.exists():
            try:
                terms_conditions = Terms_Conditions.objects.filter(id=id)
            except:
                terms_conditions = Terms_Conditions.objects.filter(pk__in=[])
            # print('terms_conditions', terms_conditions)
            if terms_conditions.exists():
                serializer = GetTermsConditionSerializer(terms_conditions.first(), data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    res = resFun(status.HTTP_200_OK,'updated successfully', serializer.data)
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST, serializer.errors['title'] if serializer.errors['title'] else serializer.errors , [])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST,'no terms_conditions found', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST,'terms conditions name already exist', [])
        return res



class TrashTermsConditionAdmin(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetTermsConditionSerializer
    def delete(self, request, id, format=None, *args, **kwargs):
        try:
            terms_conditions = Terms_Conditions.objects.filter(id = id, trash=False)
        except:
            terms_conditions = Terms_Conditions.objects.filter(pk__in=[])

        
        if terms_conditions.exists():
            serializer = GetTermsConditionSerializer(terms_conditions.first(), data={'trash':True}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            res = resFun(status.HTTP_200_OK, 'moved to trash', serializer.data)
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'terms conditions not found', [])
        return res
    


class AddTermsConditionAdmin(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetTermsConditionSerializer
    def post(self, request, format=None, *args, **kwargs):
        serializer = GetTermsConditionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = resFun(status.HTTP_200_OK, 'successfully added',[])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, serializer.errors,[])
        return res
    

class GetBookingAjax(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetBookingAjaxSerializer
    def post(self, request, format=None, *args, **kwargs):
        try:
            data = request.data.get('booking')
            print('data',data)
            booking = Booking.objects.filter(user__name__icontains=data).order_by('-id')
            # print('booking',booking)
            main_data = [ {"id": b.id, 'date': b.booking_date, 'name': b.user.name} for b in booking]

            serializer = GetBookingAjaxSerializer(data=main_data, many=True)
            if serializer.is_valid():
                res = resFun(status.HTTP_200_OK, 'request successful',serializer.data)
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'request failed',serializer.errors)

            return res
        except:
            return resFun(status.HTTP_400_BAD_REQUEST, 'request failed', [])
            




class teamAddFund(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = teamAddFundSerializer
    def post(self,request, format=None, *args, **kwargs):
        print(request.data)
        try:
            data = {}
            if request.data.get('amount'):
                data['amount'] = int(request.data.get('amount'))
            else:
                return resFun(status.HTTP_400_BAD_REQUEST, 'amount field is required', [])
            
            if request.data.get('booking_id'):
                data['booking'] = request.data.get('booking_id')
            
            if request.data.get('notes'):
                data['note'] = request.data.get('notes')

            if request.data.get('team_mate_id') == None:
                return resFun(status.HTTP_400_BAD_REQUEST, 'team_mate id is required', [])

            serializer = teamAddFundSerializer(data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                
                team = Team_member.objects.get(id=request.data.get('team_mate_id'))
                team.fund.add(serializer.instance)

                res = resFun(status.HTTP_200_OK, 'request successful', [])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'request failed', [])
            return res
        except:
            return resFun(status.HTTP_400_BAD_REQUEST, 'request failed', [])
        

class TeamDeposite(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamDepositeSerializer
    def post(self,request, format=None, *args, **kwargs):
        try:
            data = {}
            if request.data.get('amount'):
                data['amount'] = int(request.data.get('amount'))
            else:
                return resFun(status.HTTP_400_BAD_REQUEST, 'amount field is required', [])
            
            if request.data.get('notes'):
                data['note'] = request.data.get('notes')

            if request.data.get('team_mate_id') == None:
                return resFun(status.HTTP_400_BAD_REQUEST, 'team_mate id is required', [])

            serializer = TeamDepositeSerializer(data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                
                team = Team_member.objects.get(id=request.data.get('team_mate_id'))
                team.payments.add(serializer.instance)
                
                res = resFun(status.HTTP_200_OK, 'request successful', [])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'request failed', [])
            return res
        except:
            return resFun(status.HTTP_400_BAD_REQUEST, 'request failed', [])
        


class CreateWalkinClient(GenericAPIView):
    authentication_classes = [IgnoreBearerTokenAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = CreateWalkinClientSerializer
    def post(self,request, format=None, *args, **kwargs):
        try:

            email = request.data.get('email_id')
            contact_number = request.data.get('contact_number')
            
            if email:
                client = Client.objects.filter(email_id=email)

            if contact_number:
                client = Client.objects.filter(contact_number=contact_number)
            
            if not client.exists():
                serializer = CreateWalkinClientSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    serializer.instance.source = ClientSource.objects.get(title = 'website_walkin')
                    serializer.save()

                    res = resFun(status.HTTP_200_OK, 'request raised, you will get callback soon', [])
                else:
                    print(serializer.errors)
                    res = resFun(status.HTTP_400_BAD_REQUEST, 'something went wrong', [])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'user already registered with this email or contact number', [])

            return res
        except:
            return resFun(status.HTTP_400_BAD_REQUEST, 'request failed', [])
