from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Hall, Video
from .forms import VideoForm, SearchForm
from django.http import Http404
from django.forms.utils import ErrorList
import urllib
import requests

YOUTUBE_API='AIzaSyCJ8dCJ-vti7vZnxWdBAsrOyAWnrg5uCtg'

# Create your views here.
def home(request):
    return render(request, template_name='hall/home.html')

def dashboard(request):
    return render(request, template_name='hall/dashboard.html')

class SignUp(generic.CreateView):
    form_class=UserCreationForm
    success_url=reverse_lazy('home')
    template_name='registration/signup.html'

    def form_valid(self, form):
        # Automatic login upon signup
        view=super(SignUp, self).form_valid(form) # Getting view from super call
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        user=authenticate(username=username, password=password)
        login(self.request, user)
        return view


class CreateHall(generic.CreateView):
    model=Hall
    fields=['title']
    template_name='hall/create_hall.html'
    success_url=reverse_lazy('home')

    def form_valid(self, form):
        # Assigning self.request.user to form instance user
        form.instance.user=self.request.user
        super(CreateHall, self).form_valid(form) # called super for remaining operation
        return redirect('home')

class DetailHall(generic.DetailView):
    model=Hall
    template_name='hall/detail_hall.html'

class UpdateHall(generic.UpdateView):
    model=Hall
    template_name='hall/update_hall.html'
    fields=['title'] # this is what user is allowed to change
    success_url=reverse_lazy('dashboard')

class DeleteHall(generic.DeleteView):
    model=Hall
    template_name='hall/delete_hall.html'
    success_url=reverse_lazy('dashboard')

def add_video(request, pk):
    form=VideoForm()
    search_form=SearchForm()
    hall=Hall.objects.get(pk=pk)
    if not hall.user==request.user:
       raise Http404

    if request.method=='POST':
        # Create Video object on POST
        filled_form=VideoForm(request.POST)
        if filled_form.is_valid():
            video=Video()
            video.hall=hall
            video.url=filled_form.cleaned_data['url']
            parsed_url=urllib.parse.urlparse(video.url)
            video_id=urllib.parse.parse_qs(parsed_url.query).get('v') # v has the youtube id in the url
            if video_id:
                video.youtube_id=video_id[0]
                response=requests.get(f'https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id={video_id[0]}&key={YOUTUBE_API}')
                json=response.json()
                video.title=json['items'][0]['snippet']['title']
                video.save()
                return redirect('detail_hall', pk)
            else:
                errors=filled_form._errors.setdefault('url',ErrorList())
                errors.append('Need to be a YouTube Url')
    return render(request, template_name='hall/add_video.html',context={
        'form':form, 
        'search_form':search_form,
        'hall':hall
        })