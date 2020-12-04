from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Hall, Video
from .forms import VideoForm, SearchForm

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

    if request.method=='POST':
        # Create Video object on POST
        filled_form=VideoForm(request.POST)
        if filled_form.is_valid():
            video=Video()
            video.title=filled_form.cleaned_data['title']
            video.url=filled_form.cleaned_data['url']
            video.youtube_id=filled_form.cleaned_data['youtube_id']
            video.hall=Hall.objects.get(pk=pk)
            video.save()
    return render(request, template_name='hall/add_video.html',context={'form':form, 'search_form':search_form})