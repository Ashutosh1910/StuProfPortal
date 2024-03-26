from django.urls import path
from .views import ChooseElectives,create_student_profile,StudentHome,course_detail,download_announcement_resource,download_material_resource,cgpa_calc_view
urlpatterns = [
    path("create-profile/",create_student_profile,name='createstudentprofile'),
    path("create-profile/select-electives",ChooseElectives,name='choose-electives'),
    path("home/",StudentHome,name='StudentHome'),
    path("home/cgpa-calc",cgpa_calc_view,name='cgpa-calc'),

    
    path("courses/<int:pk>/",course_detail,name='enrolled-course-detail'),

    path("resources/<int:pk>/announcement",download_announcement_resource,name='announcement-download'),
    path("resources/<int:pk>/notes",download_material_resource,name='material-download')





  
]
