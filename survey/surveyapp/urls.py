from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),  # Welcome page
    path('dashboard/', views.survey_dashboard, name='survey_dashboard'),  # Creator's dashboard
    path('register/creator/', views.register_creator, name='register_creator'),  # Register as creator
    path('register/user/', views.register_user, name='register_user'),  # Register as user (taker)
    path('login/creator/', views.login_creator, name='login_creator'),  # Login as creator
    path('login/user/', views.login_user, name='login_user'),  # Login as user (taker)
    path('create/', views.create_survey, name='create_survey'),  # Create a survey
    path('<int:survey_id>/questions/', views.add_questions, name='add_questions'),  # Add questions to a survey
    path('questions/<int:question_id>/edit/', views.edit_question, name='edit_question'),  # Edit question and options
    path('results/<int:survey_id>/', views.view_survey_results, name='view_survey_results'),  # View survey results
    path('available-surveys/', views.available_surveys, name='available_surveys'),  # View available surveys for takers
    path('take-survey/<int:survey_id>/', views.take_survey, name='take_survey'),  # Take a survey
    path('survey-completed/', views.survey_completed, name='survey_completed'),  # Survey completion confirmation
    path('<int:survey_id>/republish/', views.republish_survey, name='republish_survey'), 
    path('user-results/<int:survey_id>/', views.view_user_results, name='view_user_results'),
    path('logout/', views.logout_view, name='logout'),

]
