from django.shortcuts import render,redirect,Http404,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import *
from .forms import *
from django.contrib import messages
import json
import requests
from django.utils.timezone import localdate,localtime,now

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
    # print(localtime(now()).strftime('%Y-%m-%d %H:%M:%S'))
    if request.user.is_staff:
        questions=Questions.objects.filter(contest=contest)
        return render(request,'contest_details.html',{'questions':questions,'contest':contest,'registration_count':registration_count,'is_participant':is_participant})
    return render(request,'contest_details.html',{'contest':contest,'is_participant':is_participant,'registration_count':registration_count})


@login_required
def codelife_contest(request,contest_id):
    contest=get_object_or_404(Contests,id=contest_id)
    current_time=int((contest.end_date-localtime(now())).total_seconds())
    is_participant=Participant.objects.filter(contest=contest,user=request.user).exists()
    if not is_participant or contest.status=='Upcoming' :
        return redirect('codelife:contest_details', contest_id=contest.id)
    # print(localtime(now()),'-',contest.end_date,'=',current_time)
    return render(request,'contest.html',{'contest':contest,'current_time':current_time})

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

            return redirect('codelife:contest_details', contest_id=contest.id)
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
        formset = TestcaseFormSet(request.POST, queryset=question.testcases.all())

        if form.is_valid() and formset.is_valid():
            # Save the question
            question = form.save()

            # Save the testcases
            testcases = formset.save(commit=False)
            for testcase in testcases:
                testcase.question = question
                testcase.save()

            # Handle deleted testcases
            for deleted in formset.deleted_objects:
                deleted.delete()

            return redirect('codelife:contest_details', contest_id=contest.id)

        else:
            return render(request, 'add_question.html', {
                'form': form,
                'formset': formset,
                'contest': contest,
                'is_edit': True,
            })
    else:
        form = AddQuestionsForm(instance=question)
        formset = TestcaseFormSet(queryset=question.testcases.all())

    return render(request, 'add_question.html', {
        'form': form,
        'formset': formset,
        'contest': contest,
        'is_edit': True,
    })


def leaderboard(request, contest_id):
    contest = get_object_or_404(Contests, id=contest_id)
    participants = (
        Participant.objects.filter(contest=contest)
        .order_by('-score', 'joined_at') 
    )
    participants_data = [
        {
            'rank': index + 1,
            'username': participant.user.username,
            'score': participant.score,
            'joined_at': participant.joined_at,
        }
        for index,participant in enumerate(participants)
    ]
    data = {
        'participants': participants_data,
    }

    return JsonResponse(data)

@csrf_exempt
def questions(request, contest_id):
    user = get_object_or_404(User, id=request.user.id)
    contest = get_object_or_404(Contests, id=contest_id)
    questions = Questions.objects.filter(contest=contest)
    participant=get_object_or_404(Participant,user=user,contest=contest)
    if not questions.first():
        return JsonResponse({'error':'questions not availble in this contest.'},status=400)
    first_question = questions.first().id
    question_id = request.GET.get('question_id',first_question)
    if not question_id:
        return JsonResponse({'error': 'question_id is required'}, status=400)
    current_question = get_object_or_404(Questions, id=question_id, contest=contest)
    status = is_solved(current_question, user)
    lost_submissions=0 
    testcase_data=False
    if Submission.objects.filter(participant__user=user,question=current_question).exists():
        lost_submissions = Submission.objects.filter(participant__user=user,question=current_question).count()-Submission.objects.filter(participant__user=user,question=current_question,output=1,).count()
        testcase_data=Submission.objects.filter(participant__user=user,question=current_question).latest('created_at').json_data
        # print(testcase_data)
    # sample_testcase=Testcases.objects.filter(question=current_question).first()
    solved_status = [
        {'question_id': q.id, 'solved': is_solved(q, user)}
        for q in questions
    ]

    # temp_codes=get_object_or_404(Tempcode,participant__user=user,question=current_question)
    if Tempcode.objects.filter(participant__user=user,question=current_question).exists():
        temp_codes=get_object_or_404(Tempcode,participant__user=user,question=current_question)
    else:
        temp_codes=Tempcode.objects.create(participant=participant,question=current_question)
    response = {
        'current_question': current_question.serialize() | {
            'lost_submissions': lost_submissions, 
            'status': status,
            # 'sample_testcase':sample_testcase.serialize(),
        }, 
        'contest': {
            'id': contest.id,
            'title': contest.title,
        },
        'total_questions': questions.count(),
        'solved_status': solved_status,
        'testcase_data':testcase_data,
        'scripts':temp_codes.serialize()
    }
    return JsonResponse(response)


@csrf_exempt
def submit(request,  question_id):
    user = get_object_or_404(User, id=request.user.id)
    question = get_object_or_404(Questions, id=question_id)
    participant=get_object_or_404(Participant,user=user,contest=question.contest)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    passed_data=json.loads(request.body)
    if question.contest.end_date<localtime(now()):
        return JsonResponse({'error': 'Contest has ended'}, status=400)
    code = passed_data['code']
    language =passed_data['language']
    saving_data=save_temp_code(user,passed_data['temp_code_data'])
    testcases=Testcases.objects.filter(question=question)
    testcases_count=testcases.count()
    jsondata={
        'testcases':[ testcase.serialize() for testcase in testcases],
        'testcases_count':testcases_count,
        'code':code,
        'language':language,
    }
    try:
        response = requests.post(
            url,
            json=jsondata
        )
        data = response.json()

        # print(data)
        lang=['','python','c','c++','java']
        errors=['','runtime_error','compliation_error','wrong_answer']
        sample=data['sample_testcase']
        hidden=data['hidden_testcase']
        success=True
        question_score=question.score
        status=''
        score=0
        for testcase_result in sample:
            if testcase_result['success']==False:
                success=False
                status=testcase_result['error']
            else:
                score+=question_score/testcases_count
        for testcase_result in hidden:
            if testcase_result['success']==False:
                success=False
                status=testcase_result['error']
            else:
                score+=question_score/testcases_count
        if success==True and not Submission.objects.filter(question=question,output=1,participant=participant).exists() :
            participant.score+=score
            participant.save()
            # print(participant.score)
        else:
            score=0
        Submission.objects.create(question=question,code=code,language=lang.index(language),output=errors.index(status)+1,score=score,participant=participant,json_data=data)
    except requests.exceptions.HTTPError as errh:
        return JsonResponse({'error': f"HTTP error occurred: {errh}"},status=505)
    except requests.exceptions.ConnectionError as errc:
        return JsonResponse({'error': f"Error connecting: {errc}"},status=505)
    except requests.exceptions.Timeout as errt:
        return JsonResponse({'error': f"Timeout error: {errt}"},status=505) 
    except requests.exceptions.RequestException as err:
        return JsonResponse({'error': f"An error occurred: {err}"},status=505)
    # Return the output of the code execution
    return JsonResponse(data|{'score':score,'success':success})

@csrf_exempt
@login_required
def save_temporary_code(request):
    if request.method!='POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request.'})
    temp_code_data= json.loads(request.body)
    return  save_temp_code(request.user,temp_code_data)

def save_temp_code(user,data=None):
    if data:
        question_id=max(1,int(data['question_id']))
        question=get_object_or_404(Questions,id=question_id)
        participant=get_object_or_404(Participant,user=user,contest=question.contest)
        tempcode=get_object_or_404(Tempcode,question=question,participant=participant)
        tempcode.c=data['c'] 
        tempcode.python=data['python']
        tempcode.cpp=data['cpp']
        tempcode.java=data['java']
        tempcode.save()
        return JsonResponse({'success':True})
    else:
        return JsonResponse({'success':False})

def is_solved(question,user):
    return Submission.objects.filter(output=1, participant__user=user, question=question).exists()
    


