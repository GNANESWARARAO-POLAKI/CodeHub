from django.shortcuts import render,redirect,Http404,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import *
from .forms import *
from django.contrib import messages

import requests

# url = 'http://172.30.100.208:8000/run/'
url='http://127.0.0.1:8080/run/'
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
    contest=get_object_or_404(Contests,id=contest_id)
    return render(request,'ai/index.html',{'contest':contest})

@login_required
def add_question(request, contest_id):
    contest = get_object_or_404(Contests, id=contest_id)

    if request.method == 'POST':
        form = AddQuestionsForm(request.POST)
        formset = TestcaseFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            # Create a new question
            question = form.save(commit=False)
            question.contest = contest
            question.save()

            # Save testcases
            for form in formset:
                testcase = form.save(commit=False)
                testcase.question = question
                testcase.save()

            return redirect('contest_details', contest_id=contest.id)
        else:
            # If form is invalid, return with errors
            return render(request, 'add_question.html', {
                'form': form,
                'formset': formset,
                'contest': contest,
                'is_edit': False
            })
    else:
        form = AddQuestionsForm()
        formset = TestcaseFormSet(queryset=Testcases.objects.none())  # No testcases initially

    return render(request, 'add_question.html', {
        'form': form,
        'formset': formset,
        'contest': contest,
        'is_edit': False  # Flag to indicate this is for adding
    })



# @login_required
# def edit_question(request,question_id):
#     question=get_object_or_404(Questions,id=question_id)
#     if request.method == 'POST':
#         form = AddQuestionsForm(request.POST, instance=question)
#         if form.is_valid():
#             form.save()  
#             return redirect('codelife:contest_details', contest_id=question.contest.id)
#     else:
#         form = AddQuestionsForm(instance=question)
#     return render(request, 'edit_question.html', {'form': form})


@login_required
def edit_question(request, question_id):
    question = get_object_or_404(Questions, id=question_id)
    contest = question.contest

    if request.method == 'POST':
        form = AddQuestionsForm(request.POST, instance=question)
        formset = TestcaseFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            # Update existing question
            question = form.save()

            # Save or update testcases
            for form in formset:
                testcase = form.save(commit=False)
                testcase.question = question
                testcase.save()

            return redirect('codelife:contest_details', contest_id=contest.id)
        else:
            # If form or formset is invalid, return with errors
            return render(request, 'add_question.html', {
                'form': form,
                'formset': formset,
                'contest': contest,
                'is_edit': True  # Flag to indicate this is for editing
            })
    else:
        form = AddQuestionsForm(instance=question)
        formset = TestcaseFormSet(queryset=question.testcases.all())  # Pre-fill with existing testcases

    return render(request, 'add_question.html', {
        'form': form,
        'formset': formset,
        'contest': contest,
        'is_edit': True  # Flag to indicate this is for editing
    })


@csrf_exempt
def question_page(request, contest_id):
    user = get_object_or_404(User, id=request.user.id)
    contest = get_object_or_404(Contests, id=contest_id)
    questions = Questions.objects.filter(contest=contest)
    first_question = questions.first().id
    question_id = request.GET.get('question_id',first_question)
    if not question_id:
        return JsonResponse({'error': 'question_id is required'}, status=400)
    current_question = get_object_or_404(Questions, id=question_id, contest=contest)
    status = is_solved(current_question, user)
    lost_submissions = Submission.objects.filter(
        participant__user=user,
        question=current_question,
        output=0
    ).count()
    sample_testcase=Testcases.objects.filter(question=current_question).first()
    solved_status = [
        {'question_id': q.id, 'solved': is_solved(q, user)}
        for q in questions
    ]
    response = {
        'current_question': current_question.serialize() | {
            'lost_submissions': lost_submissions,
            'status': status,
            'sample_testcase':sample_testcase.serialize(),
        },
        'contest': {
            'id': contest.id,
            'title': contest.title,
        },
        'total_questions': questions.count(),
        'solved_status': solved_status,
    }
    return JsonResponse(response)

@csrf_exempt
def submit(request,  question_id):
    user = get_object_or_404(User, id=request.user.id)
    question = get_object_or_404(Questions, id=question_id)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    code = request.POST.get('code')
    language = 'java'
    testcases=Testcases.objects.filter(question=question)
    testcases_count=testcases.count()


    jsondata={
        'testcases':[ testcase.serialize() for testcase in testcases],
        'testcases_count':testcases_count,
        'code':code,
        'language':language,
    }
    output='failed'
    try:
        response = requests.post(
            url,
            json=jsondata
        )
        

        # Parse the API response
        data = response.json()
        if 'output' in data:
            output = data['output']
        else:
            return JsonResponse({'error': 'Invalid response from the code execution API','output':'500'})
    except requests.exceptions.HTTPError as errh:
        return JsonResponse({'error': f"HTTP error occurred: {errh}"})
    except requests.exceptions.ConnectionError as errc:
        return JsonResponse({'error': f"Error connecting: {errc}"})
    except requests.exceptions.Timeout as errt:
        return JsonResponse({'error': f"Timeout error: {errt}"})
    except requests.exceptions.RequestException as err:
        return JsonResponse({'error': f"An error occurred: {err}"})

    # Return the output of the code execution
    return JsonResponse({'status': output})



def is_solved(question,user):
    return Submission.objects.filter(output=1, participant__user=user, question=question).exists()
    

