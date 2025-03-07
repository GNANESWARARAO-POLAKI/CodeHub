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


# url='http://172.30.94.65:9000/run/'  
# ---ml lab gpu 


#--project lab gpu 
# url='http://172.30.100.82:9000/run/'



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
        return JsonResponse({'message': 'Registration successful!','success':True})

    return redirect('codelife:contest_details', contest_id=contest.id)


def contest_details(request,contest_id):
    contest=get_object_or_404(Contests,id=contest_id)
    is_participant=False
    registration_count=Participant.objects.filter(contest=contest).count()
    if request.user.is_authenticated:
        is_participant=Participant.objects.filter(user=request.user,contest=contest).exists()
    # print(localtime(now()).strftime('%Y-%m-%d %H:%M:%S'))
    if request.user.is_staff:
        questions=contest.questions.all()
        return render(request,'contest_details.html',{'questions':questions,'contest':contest,'registration_count':registration_count,'is_participant':is_participant})
    return render(request,'contest_details.html',{'contest':contest,'is_participant':is_participant,'registration_count':registration_count})

@login_required
def codelife_contest(request,contest_id):
    contest=get_object_or_404(Contests,id=contest_id)
    current_time=int((contest.end_date-localtime(now())).total_seconds())
    is_participant=Participant.objects.filter(contest=contest,user=request.user).exists()
    if not is_participant or contest.status=='Upcoming' :
        return redirect('codelife:contest_details', contest_id=contest.id)
    if contest.status=='Past':
        return redirect('codelife:contest_results',contest_id=contest.id)
    # print(localtime(now()),'-',contest.end_date,'=',current_time)
    # print(localtime().strftime('%H%M'))
    participant=get_object_or_404(Participant,user=request.user,contest=contest)
    return render(request,'contest.html',{'contest':contest,'current_time':current_time,'participant':participant})



def verify_passcode(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Read JSON data correctly
            contest_id = data.get('contest_id')
            passcode = data.get('passcode')

            contest = get_object_or_404(Contests, id=contest_id)  # Validate contest

                
            if passcode == localtime().strftime('%MGMRIT%H'):  # Replace with your actual validation logic
                participant = get_object_or_404(Participant, user=request.user, contest=contest)
                participant.is_active = True
                participant.save()

                return JsonResponse({
                    'success': True,
                    'message': 'Passcode verified successfully!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid passcode!'
                })

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data!'}, status=400)
    
    return JsonResponse({'success': False, 'message': 'Invalid request method!'}, status=400)

# @login_required
# def add_question(request, contest_id):
#     contest = get_object_or_404(Contests, id=contest_id)

#     if request.method == 'POST':
#         form = AddQuestionsForm(request.POST)
#         formset = TestcaseFormSet(request.POST)

#         if form.is_valid() and formset.is_valid():
#             # Create a new question
#             question = form.save(commit=False)
#             question.contest = contest
#             question.save()

#             # Save testcases
#             for form in formset:
#                 testcase = form.save(commit=False)
#                 testcase.question = question
#                 testcase.save()

#             return redirect('codelife:contest_details', contest_id=contest.id)
#         else:
#             # If form is invalid, return with errors
#             return render(request, 'add_question.html', {
#                 'form': form,
#                 'formset': formset,
#                 'contest': contest,
#                 'is_edit': False
#             })
#     else:
#         form = AddQuestionsForm()
#         formset = TestcaseFormSet(queryset=Testcase.objects.none())  # No testcases initially

#     return render(request, 'add_question.html', {
#         'form': form,
#         'formset': formset,
#         'contest': contest,
#         'is_edit': False  # Flag to indicate this is for adding
#     })



# # @login_required
# # def edit_question(request,question_id):
# #     question=get_object_or_404(Questions,id=question_id)
# #     if request.method == 'POST':
# #         form = AddQuestionsForm(request.POST, instance=question)
# #         if form.is_valid():
# #             form.save()  
# #             return redirect('codelife:contest_details', contest_id=question.contest.id)
# #     else:
# #         form = AddQuestionsForm(instance=question)
# #     return render(request, 'edit_question.html', {'form': form})


# @login_required
# def edit_question(request, question_id):
#     question = get_object_or_404(Questions, id=question_id)
#     contest = question.contest

#     if request.method == 'POST':
#         form = AddQuestionsForm(request.POST, instance=question)
#         formset = TestcaseFormSet(request.POST, queryset=question.testcases.all())

#         if form.is_valid() and formset.is_valid():
#             # Save the question
#             question = form.save()

#             # Save the testcases
#             testcases = formset.save(commit=False)
#             for testcase in testcases:
#                 testcase.question = question
#                 testcase.save()

#             # Handle deleted testcases
#             for deleted in formset.deleted_objects:
#                 deleted.delete()

#             return redirect('codelife:contest_details', contest_id=contest.id)

#         else:
#             return render(request, 'add_question.html', {
#                 'form': form,
#                 'formset': formset,
#                 'contest': contest,
#                 'is_edit': True,
#             })
#     else:
#         form = AddQuestionsForm(instance=question)
#         formset = TestcaseFormSet(queryset=question.testcases.all())

#     return render(request, 'add_question.html', {
#         'form': form,
#         'formset': formset,
#         'contest': contest,
#         'is_edit': True,
#     })
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Contests

@login_required
def add_or_edit_question(request, contest_id=None, question_id=None):
    if question_id:
        question = get_object_or_404(Questions, id=question_id)
        contest = question.contest
        is_edit = True

    else:
        contest = get_object_or_404(Contests, id=contest_id)
        question = None
        is_edit = False

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        score = request.POST.get('score')
        timelimit = request.POST.get('timelimit')
        lives=request.POST.get('lives')
        if is_edit:
            question.title = title
            question.description = description
            question.score = score
            question.timelimit = timelimit
            question.lives=lives
            question.save()
        else:
            question = Question.objects.create(
                title=title,
                description=description,
                score=score,
                timelimit=timelimit,
                lives=lives,
                # contest=contest
            )

        # Handling test cases
        testcases_count = int(request.POST.get('testcases_count', 0))
        
        for i in range(testcases_count):
            input_data = request.POST.get(f'input_{i}')
            output_data = request.POST.get(f'output_{i}')
            hidden = request.POST.get(f'hidden_{i}') == 'on'  # Convert string to boolean

            if input_data and output_data:
                testcase, created = Testcases.objects.get_or_create(question=question, input_data=input_data)
                testcase.expected_output = output_data
                testcase.hidden = hidden
                testcase.save()

        return redirect('codelife:contest_details', contest_id=contest.id)

    testcases = Testcases.objects.filter(question=question) if is_edit else []
    return render(request, 'add_or_edit_question.html', {'contest': contest, 'question': question, 'testcases': testcases, 'is_edit': is_edit})


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
            'jntuno': participant.user.jntuno,
            'last_activity': participant.last_activity,
            'year':participant.user.year,
        }
        for index,participant in enumerate(participants)
    ]
    # if Participant.objects.filter(contest=contest,user=request.user).exists():
    #     current_rank=get_object_or_404(Participant,user=request.user,contest=contest)
    # else:
    #     contest_rank=-1
    is_staff = False
    if request.user and request.user.is_staff:
        is_staff = True
    data = {
        'is_staff':is_staff,
        'participants': participants_data,
        # 'current_rank':
    }

    return JsonResponse(data)

@csrf_exempt
def questions(request, contest_id):
    user = get_object_or_404(User, id=request.user.id)
    contest = get_object_or_404(Contests, id=contest_id)
    questions = contest.questions.all().order_by('id')
    participant=get_object_or_404(Participant,user=user,contest=contest)
    
    if not questions.exists():
        return JsonResponse({'error': 'Questions not available in this contest.'}, status=400)
    first_question = questions.first().id
    question_id = request.GET.get('question_id',first_question)
    if not question_id:
        return JsonResponse({'error': 'question_id is required'}, status=400)
    current_question = get_object_or_404(Question, id=question_id)
    status = is_solved(current_question, user)
    lost_submissions=0
    testcase_data=False
    submissions = Submission.objects.filter(participant__user=user, question=current_question)
    lost_submissions = submissions.count() - submissions.filter(output=1).count() if submissions.exists() else 0
    testcase_data = submissions.latest('created_at').json_data if submissions.exists() else False
        # print(testcase_data)
    # sample_testcase=Testcase.objects.filter(question=current_question).first()
    current_score=0
    solved_status=[]
    for q in questions:
        solved = is_solved(q, user)
        solved_status.append({'question_id': q.id, 'solved': solved})
        if solved:
            current_score += q.score
            
    # temp_codes=get_object_or_404(Tempcode,participant__user=user,question=current_question)
    temp_codes, created = Tempcode.objects.get_or_create(participant=participant, question=current_question)

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
        'total_score' :sum(questions.values_list('score', flat=True)) or 0,
        'current_score':participant.score,
        'solved_status': solved_status,
        'testcase_data':testcase_data,
        'scripts':temp_codes.serialize()
    }
    # print(response) 
    return JsonResponse(response)


@csrf_exempt
def submit(request,  question_id):
    user = get_object_or_404(User, id=request.user.id)
    question = get_object_or_404(Questions, id=question_id)
    participant=get_object_or_404(Participant,user=user,contest=question.contest)
    current_score=participant.score
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    passed_data=json.loads(request.body)
    if question.contest.end_date<localtime(now()):
        return JsonResponse({'error': 'Contest has ended'}, status=400)
    code = passed_data['code']
    language =passed_data['language']
    saving_data=save_temp_code(user,passed_data['temp_code_data'])
    testcases=Testcase.objects.filter(question=question)
    testcases_count=testcases.count()
    jsondata={
        'testcases':[ testcase.serialize() for testcase in testcases],
        'testcases_count':testcases_count,
        'code':code,
        'language':language,
        'timelimit':question.timelimit,
    }
    try:
        response = requests.post(
            url,
            json=jsondata
        )
        data = response.json()

        # print(data)
        lang=['','python','c','cpp','java']
        errors=['','runtime_error','compliation_error','wrong_answer','time_limit_exceeded']
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
            participant.score+=question.score
            score=question.score
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
    print(data,score)
    current_score=participant.score
    return JsonResponse(data|{'score':score,'success':success,'current_score':current_score})

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
    

@login_required
def manage_contest(request,contest_id):
    contest = get_object_or_404(Contests,id=contest_id)
    if contest.status=='Past':
        if contest.winners.exists():
            winner_users=list(contest.winners.all())
            winners = Participant.objects.filter(user=winner_users[0], contest=contest)
            for winner in winner_users[1:]:
                winners|=Participant.objects.filter(user=winner_users[1], contest=contest)
            return render(request, 'contest_results.html', {'contest': contest, 'winners': winners})      
        else:
            participants=Participant.objects.filter(contest=contest).order_by('-score', 'last_activity')
            contest.winners.add(participants[0].user.id)
            contest.winners.add(participants[1].user.id)
            # print(participants[0].user.username)
            contest.save() 
    return render(request,'manage_contest.html',{'contest':contest})

from django.db.models import Q

@login_required
def manage_participant(request, contest_id, participant_name):
    contest = get_object_or_404(Contests, id=contest_id)
    participant = get_object_or_404(Participant, user__username=participant_name, contest=contest)

    # Fetch all questions from the contest AND questions the participant has submitted for
    questions = contest.questions.all()

    # Get all submissions of the participant
    submissions = Submission.objects.filter(participant=participant).select_related('question')

    # Organizing submissions by question ID
    question_submissions = {question.id: [] for question in questions}
    lives_lost = {question.id: 0 for question in questions}

    # Process submissions
    for submission in submissions:
        question_id = submission.question.id
        if question_id not in question_submissions:
            question_submissions[question_id] = []  # Ensure the key exists

        question_submissions[question_id].append(submission)
        
        if submission.output != 1:  # Assuming output != 1 means failure
            lives_lost[question_id] += 1

    return render(
        request,
        'manage_participant.html',
        {
            'participant': participant,
            'contest': contest,
            'questions': questions,
            'question_submissions': question_submissions,
            'lives_lost': lives_lost
        }
    )
@login_required
def contest_results(request,contest_id):
    contest = get_object_or_404(Contests,id=contest_id)
    if Participant.objects.filter(contest=contest,user=request.user).exists() and not request.user.is_staff:
        current_user_participant=get_object_or_404(Participant,user=request.user,contest=contest)
        current_user_participant.is_active=False
        current_user_participant.save()
    if contest.status=='Past':
        if contest.winners.exists():
            winner_users=list(contest.winners.all())
            winners = Participant.objects.filter(user=winner_users[0], contest=contest)
            for winner in winner_users[1:]:
                winners|=Participant.objects.filter(user=winner_users[1], contest=contest)
            return render(request, 'contest_results.html', {'contest': contest, 'winners': winners})      
        else:
            participants=Participant.objects.filter(contest=contest).order_by('-score', 'last_activity')
            contest.winners.add(participants[0].user.id)
            contest.winners.add(participants[1].user.id)
            # print(participants[0].user.username)
            contest.save()
    return render(request, 'contest_results.html', {'contest': contest})


def add_life(request):
    if not request.user.is_staff:
        HttpResponseBadRequest("Invalid Request")
    if request.method == "POST":
        participant_id = request.POST.get("participant_id")
        question_id = request.POST.get("question_id")

        # Fetch participant and question
        participant = get_object_or_404(Participant, id=participant_id)
        question = get_object_or_404(Questions, id=question_id)

        # Get all submissions for this participant & question
        submissions = Submission.objects.filter(participant=participant, question=question)

        # Calculate lost submissions
        lost_submissions = submissions.count() - submissions.filter(output=1).count() if submissions.exists() else 0

        if lost_submissions > 0:
            # Delete the last failed submission
            failed_submission = submissions.filter(~Q(output=1)).last()
            if failed_submission:
                failed_submission.delete()

        # Redirect back to manage_participant page
        return redirect('codelife:manage_participant', contest_id=question.contest.id, participant_name=participant.user.username)

    return HttpResponseBadRequest("Invalid Request")


@csrf_exempt
def run_code(request,contest_id,question_id):
    user = get_object_or_404(User, id=request.user.id)
    contest=get_object_or_404(Contests,id=contest_id)
    question = get_object_or_404(Question, id=question_id)
    participant = get_object_or_404(Participant, user=user, contest=contest)
    current_score = participant.score
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    passed_data = json.loads(request.body)
    
    if question.contest.end_date < localtime(now()):
        return JsonResponse({'error': 'Contest has ended'}, status=400)
    
    code = passed_data['code']
    language = passed_data['language']
    saving_data = save_temp_code(user, passed_data['temp_code_data'])
    testcases = Testcase.objects.filter(question=question)
    testcases_count = testcases.count()
    
    jsondata = {
        'testcases': [testcase.serialize() for testcase in testcases],
        'testcases_count': testcases_count,
        'code': code,
        'language': language,
        'timelimit': question.timelimit,
    }
    
    try:
        response = requests.post(
            url,
            json=jsondata
        )
        data = response.json()
        
        lang = ['', 'python', 'c', 'c++', 'java']
        errors = ['', 'runtime_error', 'compilation_error', 'wrong_answer', 'time_limit_exceeded']
        
        sample = data['sample_testcase']
        success = True
        status = ''
        score = 0
        
        for testcase_result in sample:
            if not testcase_result['success']:
                success = False
                status = testcase_result['error']
        
        score = 0  # No scoring in run_code
        
        Submission.objects.create(
            question=question,
            code=code,
            language=lang.index(language),
            output=errors.index(status) + 1,
            score=score,
            participant=participant,
            json_data=data
        )
        
        # Return response without hidden test cases
        return JsonResponse({'sample_testcase': sample, 'score': score, 'success': success, 'current_score': current_score})
    
    except requests.exceptions.HTTPError as errh:
        return JsonResponse({'error': f"HTTP error occurred: {errh}"}, status=505)
    except requests.exceptions.ConnectionError as errc:
        return JsonResponse({'error': f"Error connecting: {errc}"}, status=505)
    except requests.exceptions.Timeout as errt:
        return JsonResponse({'error': f"Timeout error: {errt}"}, status=505)
    except requests.exceptions.RequestException as err:
        return JsonResponse({'error': f"An error occurred: {err}"}, status=505)
@csrf_exempt
def run_code(request, question_id):
    user = get_object_or_404(User, id=request.user.id)
    question = get_object_or_404(Questions, id=question_id)
    participant = get_object_or_404(Participant, user=user, contest=question.contest)
    current_score = participant.score
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    passed_data = json.loads(request.body)
    
    if question.contest.end_date < localtime(now()):
        return JsonResponse({'error': 'Contest has ended'}, status=400)
    
    code = passed_data['code']
    language = passed_data['language']
    saving_data = save_temp_code(user, passed_data['temp_code_data'])
    testcases = Testcase.objects.filter(question=question)
    testcases_count = testcases.count()
    
    jsondata = {
        'testcases': [testcase.serialize() for testcase in testcases],
        'testcases_count': testcases_count,
        'code': code,
        'language': language,
        'timelimit': question.timelimit,
    }
    
    try:
        response = requests.post(
            url,
            json=jsondata
        )
        data = response.json()
        
        lang = ['', 'python', 'c', 'c++', 'java']
        errors = ['', 'runtime_error', 'compilation_error', 'wrong_answer', 'time_limit_exceeded']
        
        sample = data['sample_testcase']
        success = True
        status = ''
        score = 0
        
        for testcase_result in sample:
            if not testcase_result['success']:
                success = False
                status = testcase_result['error']
        
        # score = 0  # No scoring in run_code
        
        # Submission.objects.create(
        #     question=question,
        #     code=code,
        #     language=lang.index(language),
        #     output=errors.index(status) + 1,
        #     score=score,
        #     participant=participant,
        #     json_data=data
        # )
        
        # Return response without hidden test cases
        return JsonResponse({'sample_testcase': sample, 'score': score, 'success': success, 'current_score': current_score})
    
    except requests.exceptions.HTTPError as errh:
        return JsonResponse({'error': f"HTTP error occurred: {errh}"}, status=505)
    except requests.exceptions.ConnectionError as errc:
        return JsonResponse({'error': f"Error connecting: {errc}"}, status=505)
    except requests.exceptions.Timeout as errt:
        return JsonResponse({'error': f"Timeout error: {errt}"}, status=505)
    except requests.exceptions.RequestException as err:
        return JsonResponse({'error': f"An error occurred: {err}"}, status=505)
