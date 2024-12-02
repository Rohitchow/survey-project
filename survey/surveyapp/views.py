from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import HttpResponseForbidden
from django.db.models import Count
from .models import Survey, Question, Option, SurveyResponse, QuestionResponse
from django import forms


# Custom Registration Form
class CustomRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True, help_text="Enter your full name")

    class Meta:
        model = UserCreationForm.Meta.model
        fields = UserCreationForm.Meta.fields


# Welcome Page
def welcome(request):
    return render(request, 'welcome.html')


# Register Creator
def register_creator(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('name')
            user.save()
            login(request, user)
            return redirect('survey_dashboard')  
    else:
        form = CustomRegistrationForm()
    return render(request, 'register_creator.html', {'form': form})


# Register User
def register_user(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('name')
            user.save()
            login(request, user)
            return redirect('available_surveys')  
    else:
        form = CustomRegistrationForm()
    return render(request, 'register_user.html', {'form': form})


# Login as Creator
def login_creator(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('survey_dashboard')  
    else:
        form = AuthenticationForm()
    return render(request, 'login_creator.html', {'form': form})


# Login as User
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('available_surveys')  
    else:
        form = AuthenticationForm()
    return render(request, 'login_user.html', {'form': form})


# Survey Dashboard for Creators
@login_required
def survey_dashboard(request):
    surveys = Survey.objects.filter(creator=request.user)
    return render(request, 'survey_dashboard.html', {'surveys': surveys})


# Create Survey
@login_required
def create_survey(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        if not name or not description:
            return render(request, 'create_survey.html', {'error': 'Name and description are required.'})

        survey = Survey.objects.create(name=name, description=description, creator=request.user)
        return redirect('add_questions', survey_id=survey.id)

    return render(request, 'create_survey.html')


# Add Questions to Survey
@login_required
def add_questions(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id, creator=request.user)

    if request.method == 'POST':
        if 'save' in request.POST:
            survey.status = 'draft'
            survey.save()
            return redirect('survey_dashboard')

        if 'publish' in request.POST and survey.questions.count() >= 5:
            survey.status = 'published'
            survey.save()
            return redirect('survey_dashboard')

        if 'close' in request.POST:
            survey.status = 'closed'
            survey.save()
            return redirect('survey_dashboard')

        question_text = request.POST.get('question_text')
        options = [request.POST.get(f'option{i}') for i in range(1, 5)]

        if not question_text or not all(options):
            return render(request, 'add_questions.html', {
                'survey': survey,
                'error': 'All fields are required to add a question.'
            })

        question = Question.objects.create(survey=survey, text=question_text)
        for option_text in options:
            Option.objects.create(question=question, text=option_text)

        return redirect('add_questions', survey_id=survey.id)

    return render(request, 'add_questions.html', {'survey': survey})

@login_required
def republish_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id, creator=request.user, status='closed')
    
    if request.method == 'POST':
        survey.status = 'republished'
        survey.save()
        return redirect('survey_dashboard')

    # Prepare aggregated results
    question_results = []
    for question in survey.questions.all():
        options_data = question.options.annotate(total_responses=Count('selected_responses'))
        total_responses = sum(option.total_responses for option in options_data)

        question_results.append({
            'question': question.text,
            'options': [
                {
                    'text': option.text,
                    'count': option.total_responses,
                    'percentage': (option.total_responses / total_responses * 100) if total_responses > 0 else 0,
                } for option in options_data
            ],
        })

    return render(request, 'republish_survey.html', {
        'survey': survey,
        'question_results': question_results,
    })

# View Survey Results
@login_required
def view_survey_results(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id, creator=request.user)
    question_results = []

    for question in survey.questions.all():
        options_data = question.options.annotate(total_responses=Count('selected_responses'))
        total_responses = sum(option.total_responses for option in options_data)

        question_results.append({
            'question': question.text,
            'options': [
                {
                    'text': option.text,
                    'count': option.total_responses,
                    'percentage': (option.total_responses / total_responses * 100) if total_responses > 0 else 0,
                } for option in options_data
            ],
        })

    total_takers = survey.responses.count()

    return render(request, 'view_survey_results.html', {
        'survey': survey,
        'question_results': question_results,
        'total_takers': total_takers
    })


@login_required
def available_surveys(request):
    # Surveys available to the user (Published state and not yet taken)
    available_surveys = Survey.objects.filter(
        status='published'
    ).exclude(responses__taker=request.user)

    # Surveys already completed by the user (Republished state)
    completed_surveys = Survey.objects.filter(
        responses__taker=request.user,
        status='republished'
    ).distinct()

    return render(request, 'available_surveys.html', {
        'available_surveys': available_surveys,
        'completed_surveys': completed_surveys,
    })

@login_required
def take_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id, status__in=['published', 'republished'])

    existing_response = SurveyResponse.objects.filter(survey=survey, taker=request.user).first()
    question_results = []

    if survey.status == 'republished':
        for question in survey.questions.all():
            options_data = question.options.annotate(total_responses=Count('selected_responses'))
            question_results.append({
                'question': question.text,
                'options': [
                    {
                        'text': option.text,
                        'count': option.total_responses,
                        'percentage': (option.total_responses / total_responses * 100) if total_responses > 0 else 0,
                    } for option in options_data
                ],
            })

    if request.method == 'POST':
        # Check if all questions have a selected option
        missing_responses = []
        for question in survey.questions.all():
            selected_option_id = request.POST.get(f'question_{question.id}')
            if not selected_option_id:
                missing_responses.append(question.text)

        if missing_responses:
            return render(request, 'take_survey.html', {
                'survey': survey,
                'error': "Please select an option for all questions.",
                'question_results': None,
            })

        # Save the responses
        survey_response = SurveyResponse.objects.create(survey=survey, taker=request.user)

        for question in survey.questions.all():
            selected_option_id = request.POST.get(f'question_{question.id}')
            selected_option = get_object_or_404(Option, id=selected_option_id)
            QuestionResponse.objects.create(
                survey_response=survey_response,
                question=question,
                selected_option=selected_option
            )

        return redirect('survey_completed')

    return render(request, 'take_survey.html', {
        'survey': survey,
        'question_results': question_results if existing_response else None,
    })

# Survey Completed
def survey_completed(request):
    return render(request, 'survey_completed.html', {'message': 'Thank you for completing the survey!'})

# Edit Question and Options
@login_required
def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id, survey__creator=request.user)
    options = question.options.all()

    if request.method == 'POST':
        # Update question text
        question_text = request.POST.get('question_text')
        if question_text:
            question.text = question_text
            question.save()

        # Update options
        for idx, option in enumerate(options):
            option_text = request.POST.get(f'option{idx+1}')
            if option_text:
                option.text = option_text
                option.save()

        return redirect('add_questions', survey_id=question.survey.id)

    return render(request, 'edit_question.html', {'question': question, 'options': options})


@login_required
def view_user_results(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id, status='republished')

    if not SurveyResponse.objects.filter(survey=survey, taker=request.user).exists():
        return HttpResponseForbidden("You are not authorized to view these results.")

    # Prepare Wisdom of the Crowd results
    question_results = []
    for question in survey.questions.all():
        options_data = question.options.annotate(total_responses=Count('selected_responses'))
        total_responses = sum(option.total_responses for option in options_data)

        question_results.append({
            'question': question.text,
            'options': [
                {
                    'text': option.text,
                    'count': option.total_responses,
                    'percentage': (option.total_responses / total_responses * 100) if total_responses > 0 else 0,
                } for option in options_data
            ],
        })

    return render(request, 'user_results.html', {
        'survey': survey,
        'question_results': question_results,
    })

from django.contrib.auth import logout

@login_required
def logout_view(request):
    logout(request)  
    return redirect('welcome')  
