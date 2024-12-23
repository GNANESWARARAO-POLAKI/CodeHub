from django.shortcuts import render,redirect,Http404,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import *
from .forms import *
from django.contrib import messages


@csrf_exempt
@login_required
def register(request,contest_id):
    contest = get_object_or_404(Contests, id=contest_id)
    user = request.user
    if request.method == "POST":
        if Participant.objects.filter(user=user, contest=contest).exists():
            messages.warning(request, "You are already registered for this contest.")
        else:
            Participant.objects.create(user=user, contest=contest)
            messages.success(request, "Registration successful!")
        return redirect('codelife:contest_details', contest_id=contest.id)
    return redirect('codelife:contest_details', contest_id=contest.id)


def contest_details(request,contest_id):
    contest=get_object_or_404(Contests,id=contest_id)
    is_participant=False
    registration_count=Participant.objects.filter(contest=contest).count()
    if request.user.is_authenticated:
        is_participant=Participant.objects.filter(user=request.user,contest=contest).exists()
    if request.user.is_staff:
        questions=Questions.objects.filter(contest=contest)
        return render(request,'contest_details.html',{'questions':questions,'contest':contest,'registration_count':registration_count,'is_participant':is_participant})
    return render(request,'contest_details.html',{'contest':contest,'is_participant':is_participant,'registration_count':registration_count})


@login_required
def codelife_contest(request,contest_id):
    return render(request,'contest.html')

@login_required
def add_question(request,contest_id):
    if request.method=='POST':                                
        form=AddQuestionsForm(request.POST)
        if form.is_valid():
            if Contests.objects.filter(id=contest_id).exists():
                contest=get_object_or_404(Contests,id=contest_id)
                question = form.save(commit=False)  # Do not save to the database yet
                question.contest = contest  # Associate the contest with the question
                question.save()
                return render(request,'contest_details.html',{'contest':contest})

            else:
                return 
    form=AddQuestionsForm()
    return render(request,'add_question.html',{'form':form})


@login_required
def edit_question(request,question_id):
    question=get_object_or_404(Questions,id=question_id)
    if request.method == 'POST':
        form = AddQuestionsForm(request.POST, instance=question)
        if form.is_valid():
            form.save()  
            return redirect('codelife:contest_details', contest_id=question.contest.id)
    else:
        form = AddQuestionsForm(instance=question)
    return render(request, 'edit_contest.html', {'form': form})


@csrf_exempt
def question_page(request,contest_id):
    user=get_object_or_404(User,id=request.user.id)
    contest = get_object_or_404(Contests, id=contest_id)
    questions = Questions.objects.filter(contest=contest)
    paginator = Paginator(questions, 1)
    question_number = request.GET.get('page', 1)
    question = paginator.get_page(question_number)
    for idx, q in enumerate(question.object_list, start=(question.number - 1) * paginator.per_page + 1):
        q.display_number = f"{idx} - {'solved' if is_solved(q,user) else 'unsolved'}"
    question_data = {}
    question_data['questions'] = [
        {
            'id': q.id,
            'text': q.title,
            'is_solved': is_solved(q,user),
            'display_number': q.display_number
        } for q in question.object_list
    ]
    return JsonResponse(question_data)


def is_solved(question,user):
    return True
    
