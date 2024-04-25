from django import forms
from console.models import *

class Reels_Upload_Form(forms.ModelForm):
    class Meta:
        model = Reels
        fields = ['title', 'description', 'file']


class Pre_Wedding_Upload_Form_VIDEOFILE(forms.ModelForm):
    class Meta:
        model = Pre_Wedding
        fields = ['title', 'description', 'cover_picture','is_youtube_video','video_link' ]

class Pre_Wedding_Upload_Form_YOUTUBE_LINK(forms.ModelForm):
    class Meta:
        model = Pre_Wedding
        fields = ['title', 'description', 'cover_picture','is_youtube_video','video_youtube_link' ]


class Wedding_Upload_Form_VIDEOFILE(forms.ModelForm):
    class Meta:
        model = Wedding
        fields = ['title', 'description', 'cover_picture' ,'is_youtube_video','video_link']


class Wedding_Upload_Form_YOUTUBE_LINK(forms.ModelForm):
    class Meta:
        model = Wedding
        fields = ['title', 'description', 'cover_picture' ,'is_youtube_video','video_youtube_link']


class BannerVideo_form(forms.ModelForm):
    class Meta:
        model = Banner_video
        fields = '__all__'

class Showcase_form(forms.ModelForm):
    class Meta:
        model = Showcase_images
        fields = '__all__'


class Events_Upload_Form_VIDEOFILE(forms.ModelForm):
    class Meta:
        model = Events
        fields = ['title', 'description', 'cover_picture' ,'is_youtube_video','video_link']

class Events_Upload_Form_YOUTUBE_LINK(forms.ModelForm):
    class Meta:
        model = Events
        fields = ['title', 'description', 'cover_picture', 'is_youtube_video','video_youtube_link']


class AddClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'contact_number', 'email_id', 'client_token','source']


class EditClientForms(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
