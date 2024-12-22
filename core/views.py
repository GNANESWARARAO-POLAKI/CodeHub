from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .forms import *
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request,'index.html')                                       
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            return redirect('core:login')# Redirect to the login page
        else:
            return render(request, 'register.html', {'form': form, 'message': 'Registration failed. Check your input.'})
    
    form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form, 'message': 'Welcome to the registration page'})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                next_url = request.GET.get('next', '/')
                return redirect(next_url)  # Replace with the name of your home URL pattern
            return render(request, 'login.html', {'form': form, 'message': 'Login failed. Invalid credentials.'})
        else:
            return render(request, 'login.html', {'form': form, 'message': 'Validation failed. Check your input.'})
    
    form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('core:home')



@login_required
def create_contest(request):
    if request.method=='POST':
        form=ContestCreationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return render(request,'index.html')
    else:
        form=ContestCreationForm()
        return render(request,'create_contest.html',{'form':form,'message':''})


@login_required
def edit_contest(request, contest_id):
    contest = get_object_or_404(Contests, id=contest_id) 
    if request.method == 'POST':
        form = ContestCreationForm(request.POST,request.FILES, instance=contest)
        if form.is_valid():
            form.save()  

            return redirect('codelife:contest_details', contest_id=contest.id)
    else:
        form = ContestCreationForm(instance=contest)
    
    return render(request, 'edit_contest.html', {'form': form})


def contests(request):
    upcomming_contests=Contests.objects.filter(is_active=True)
    past_contests=Contests.objects.filter(is_active=False)
    return render(request,'contests.html',{'upcomming_contests':upcomming_contests,'past_contests':past_contests})




def custom_400(request,exception):
    return render(request,'errors/400.html',status=400)
def custom_404(request,exception):
    return render(request,'errors/404.html',status=404)
def custom_500(request):
    return render(request,'errors/500.html',status=500)

