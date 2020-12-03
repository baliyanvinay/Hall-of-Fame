from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Hall

# Create your views here.
def home(request):
    return render(request, template_name='hall/home.html')

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
