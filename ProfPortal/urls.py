from django.urls import path
from django.contrib.auth import views as auth_views
from .views import ProfHome,create_content,create_course,course_detail,create_announcement,add_student_to_course,grade_student,create_eval,eval_detail,mark_student,remove_student_from_course
urlpatterns = [
   
    path('login/',auth_views.LoginView.as_view(template_name='login.html'), name='LoginPage'),
    path('logout/',auth_views.LogoutView.as_view(template_name='logout.html'), name='LogoutPage'),
    path('home/',ProfHome, name='ProfHome'),


    path('create-course/',create_course, name='create-course'),
    path('courses/<int:pk>/',course_detail,name='course_detail'),
    path('courses/<int:pk>/announce',create_announcement,name='course-announcement'),
    path('courses/<int:pk>/add_student/<int:pk2>/',add_student_to_course,name='add-student'),
    path('courses/<int:pk>/grade_student/<int:pk2>/',grade_student,name='grade-student'),
    path('courses/<int:pk>/create-eval',create_eval,name='create-eval'),
    path('courses/<int:pk>/create-content',create_content,name='create-content'),
    path('courses/<int:pk>/remove-student/<int:pk2>/',remove_student_from_course,name='remove-student'),


    path('evals/<int:pk>/',eval_detail,name='eval_detail'),
    path('evals/<int:pk>/mark/<int:pk2>',mark_student,name='mark-student'),



]
