from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .forms import *
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now,localtime
import base64
from django.core.files.base import ContentFile

# Create your views here.

def home(request):
    return render(request,'index.html')   



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



def user_profile(request,username):
    user=get_object_or_404(User,username=username)
    form=UserRegistrationForm(instance=user)
    return render(request,'user_profile.html',{'user':user,'form':form})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, editable=True)
        if form.is_valid():
            user = form.save(commit=False)
            cropped_image_data = request.POST.get('cropped_image')
            if cropped_image_data:
                format, imgstr = cropped_image_data.split(';base64,') 
                ext = format.split('/')[-1] 
                image_data = base64.b64decode(imgstr)  
                image_file = ContentFile(image_data, name=f"{request.POST['username']}.{ext}")
                user.image = image_file 
                user.save()
            else:
                user.save()
            return redirect('core:login')  # Redirect to login page
    else:
        form = UserRegistrationForm(editable=True)
    return render(request, 'register.html', {'form': form, 'is_register': True})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES, instance=request.user, editable=False)
        if form.is_valid():
            user = form.save(commit=False)
            cropped_image_data = request.POST.get('cropped_image')
            if cropped_image_data:
                format, imgstr = cropped_image_data.split(';base64,') 
                ext = format.split('/')[-1] 
                image_data = base64.b64decode(imgstr)  
                image_file = ContentFile(image_data, name=f"{user.username}_image.{ext}")
                user.image = image_file 
                user.save()
            elif 'image-clear' in request.POST: 
                user.image.delete(save=False)  
                user.image = None
                user.save() 
            return redirect('core:home')
    else: 
        form = UserRegistrationForm(instance=request.user, editable=False)
    return render(request, 'register.html', {'form': form, 'is_register': False})

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
        return render(request,'create_contest.html',{'form':form,'message':''})
    else:
        form=ContestCreationForm()
        return render(request,'create_contest.html',{'form':form,'message':''})


@login_required
def edit_contest(request, contest_id):
    contest = get_object_or_404(Contests, id=contest_id) 
    if request.method == 'POST':
        form = ContestCreationForm(request.POST,request.FILES, instance=contest)
        if form.is_valid():
            contest_type=['','codelife','compticode','debugcode']
            
            form.save() 
            return redirect(contest_type[int(form.cleaned_data['contest_type'])]+':contest_details', contest_id=contest.id)
    else:
        form = ContestCreationForm(instance=contest)
    
    return render(request, 'edit_contest.html', {'form': form})


def contests(request):
    upcoming_contests = Contests.objects.upcoming() 
    for contest in upcoming_contests:
        contest.seconds_now=int((contest.start_date-localtime(now())).total_seconds())
    ongoing_contests = Contests.objects.ongoing()    # Get ongoing contests
    for contest in ongoing_contests:
        contest.seconds_now=int((contest.end_date-localtime(now())).total_seconds())
    past_contests = Contests.objects.past()   
    return render(request,'contests.html',{'upcomming_contests':upcoming_contests,'past_contests':past_contests,'ongoing_contests':ongoing_contests})




def custom_400(request,exception):
    return render(request,'errors/400.html',status=400)
def custom_404(request,exception):
    return render(request,'errors/404.html',status=404)
def custom_500(request):
    return render(request,'errors/500.html',status=500)

