from django.shortcuts import render,redirect
from django.http import HttpResponseForbidden,Http404,FileResponse
from django.contrib import messages
from .models import *
from ProfPortal.models import Course,Announcement,Study_Material
from .forms import StudentProfile_Form,ElectiveForm,CGPA_CalcForm
from allauth.account.models import EmailAddress
from django.contrib.auth.decorators import login_required,permission_required

@login_required
@permission_required('ProfPortal.is_student',raise_exception=True)
def create_student_profile(request): 
    if request.method=='POST':
        user_profile=Student_Profile.objects.get(user=request.user)
        form=StudentProfile_Form(request.POST,instance=user_profile)
        if form.is_valid():
            instance=form.save(commit=False)
            user_email=EmailAddress.objects.get(user=request.user).email
            instance.email=user_email
           # instance.user=request.user
            instance.bits_id=user_email[1:5]+instance.branch.branch_code+"PS"+user_email[5:9]+"P"
            instance.save()
            return redirect("StudentHome")
    else:

        form=StudentProfile_Form()
        return render(request,'profile-form.html',{'form':form})



@login_required
def StudentHome(request):
    
    try:
        user_profile=Student_Profile.objects.get(user=request.user)
    except Student_Profile.DoesNotExist:
        return HttpResponseForbidden('ACCESS DENIED')
    else:
        if Enrolled_Course.objects.filter(enrolled_student=user_profile):

            student_courses=Enrolled_Course.objects.filter(enrolled_student=user_profile)
            return render(request,"student-home.html",context={"student_courses":student_courses})
        else:
             student_branch=user_profile.branch
             cdc_courses=student_branch.course_set.all()
             for course in cdc_courses:
                    student_c= Enrolled_Course.objects.create(course_name=course.course_name,course_units=course.course_units,enrolled_student=user_profile,under_course=course)

                    for eval in course.evaluation_set.all():
                        student_eval,created=Course_eval.objects.get_or_create(of_student=student_c,of_eval=eval)
                        if created:
                            student_eval.save()

                    student_c.save()
                    messages.success(request,f'{student_c.course_name} added as it is CDC for your branch')
    
             messages.warning(request,'CDC courses have already been added')
                    
             return redirect('choose-electives')

@login_required
@permission_required('ProfPortal.is_student',raise_exception=True)
def ChooseElectives(request):
   # print('hi')
   
    if request.method=="POST":
        form=ElectiveForm(request.POST)
        if form.is_valid():
            selected_electives=form.cleaned_data.get('electives_available')
            for course in selected_electives:
                student_c,_=Enrolled_Course.objects.get_or_create(course_name=course.course_name,course_units=course.course_units,enrolled_student=request.user.student_profile,under_course=course)
                for eval in course.evaluation_set.all():
                        student_eval,created=Course_eval.objects.get_or_create(of_student=student_c,of_eval=eval)
                        if created:
                            student_eval.save()


                student_c.save()

                
            messages.success(request,'Courses added')
            return redirect('StudentHome')
        else:
            messages.warning(request,"No electives selected")
            return redirect('StudentHome')
        
    else:
        form=ElectiveForm()
    
        return render(request,'electives-form.html',context={'form':form})
            

    
@login_required
@permission_required('ProfPortal.is_student',raise_exception=True)
def course_detail(request,pk):
   try:
        enrolled_course=Enrolled_Course.objects.get(pk=pk,enrolled_student=request.user.student_profile)
   except Enrolled_Course.DoesNotExist:
       return HttpResponseForbidden('COURSE NOT FOUND')
   else:
       
       return render(request,'enrolled-course-detail.html',context={'enrolled_course':enrolled_course})
       
    

    
    
@login_required
@permission_required('ProfPortal.is_student',raise_exception=True)
def download_announcement_resource(request,pk):
   announcement=Announcement.objects.get(pk=pk)
   if not Enrolled_Course.objects.filter(under_course=announcement.under_course,enrolled_student=request.user.student_profile).exists():
       return HttpResponseForbidden('Access Denied')
   
   material=announcement.attached_file
   response=FileResponse(material)
   response['Content-Disposition']=f'attachment;filename:announce{announcement.pk}'
   return response
   
@login_required
@permission_required('ProfPortal.is_student',raise_exception=True)
def download_material_resource(request,pk):
   study_material=Study_Material.objects.get(pk=pk)
   if not Enrolled_Course.objects.filter(under_course=study_material.under_course,enrolled_student=request.user.student_profile).exists():
       return HttpResponseForbidden('Access Denied')
   
   material=study_material.material
   response=FileResponse(material)
   response['Content-Disposition']=f'attachment;'
   return response
  

    
@login_required
@permission_required('ProfPortal.is_student',raise_exception=True)
def cgpa_calc_view(request):
    student_courses=Enrolled_Course.objects.filter(enrolled_student=request.user.student_profile)
    if not student_courses:
        messages.warning(request,'You have not enrolled in any course')
        return redirect("StudentHome")
    if request.method=='POST':
        for sc in student_courses:
            sc.expected_grade=request.POST['ex-grade_id'+str(sc.pk)]
            sc.save()
        return redirect('cgpa-calc')
    else:
        return render(request,'cgpa-calc.html',context={"student_courses":student_courses})