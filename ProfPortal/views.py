from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseForbidden
from django.contrib.auth.decorators import login_required,permission_required
from StudentPortal.models import *
from allauth.socialaccount.models import SocialAccount
from .models import *
from django.contrib import messages
from .forms import New_Course_Form,Announcement_Form,Content_Form,Evalv_Form
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
def LoginPage(request):
   if request.user.is_authenticated:
     return redirect('check_user')
    
   return render(request,'base.html')




@login_required
def check_user(request):
    if SocialAccount.objects.filter(user=request.user).exists():
        
        if not request.user.student_profile.branch:
            return redirect('createstudentprofile')
        else:
            return redirect("StudentHome")
    else:
        return redirect("ProfHome")
    
@login_required
@permission_required('ProfPortal.is_prof', raise_exception=True)
def ProfHome(request):
    #get all prof courses
    prof_courses=Course.objects.filter(taught_by=request.user.profprofile)
    return render(request,'prof-home.html',context={'prof_courses':prof_courses})

@login_required
@permission_required('ProfPortal.is_prof', raise_exception=True)
def create_course(request):
    prof_profile=request.user.profprofile
    if request.method=='POST':
        form=New_Course_Form(request.POST)
        if form.is_valid():
            new_course=form.save(commit=False)
            new_course.taught_by=prof_profile
           #new_course.under_department=prof_profile.under_department
            new_course.save()

            new_course.compulsary_to.set(form.cleaned_data.get('CDC_to'))
            new_course.save()
            for branch in new_course.compulsary_to.all():
                for student in branch.student_profile_set.all():
                    Enrolled_Course.objects.create(enrolled_student=student,under_course=new_course,course_name=new_course.course_name,course_units=new_course.course_units).save()
            messages.success(request,f'{new_course.course_name} created you can students to your course')
            return redirect('ProfHome')
        else:
            dept=Department.objects.get(pk=form.data["under_department"])
            new_course=Course.objects.create(taught_by=prof_profile,under_department=dept)
            new_course.course_name=form.data['course_name']
            new_course.course_units=form.data['course_units']
            new_course.course_code=form.data['course_code']

            
            
            new_course.save()
            return redirect('ProfHome')


    else:
        form=New_Course_Form()
        return render(request,'course-form.html',context={'form':form})
@login_required
@permission_required('ProfPortal.is_prof', raise_exception=True)
def course_detail(request,pk):
    try:
         course=Course.objects.get(pk=pk,taught_by=request.user.profprofile)
    except Course.DoesNotExist:
        return HttpResponse('<h1>Course does not exist</h1>')
    else:
        #to find students not enrolled in course
        not_enrolled_courses=Enrolled_Course.objects.exclude(under_course=course)
        not_enrolled_students=set([ec.enrolled_student for ec in not_enrolled_courses  if not  Enrolled_Course.objects.filter(under_course=course,enrolled_student=ec.enrolled_student)])
        return render(request,'course-detail.html',context={"course":course,
                                          "not_enrolled_students":not_enrolled_students})
        
    
@login_required
@permission_required('ProfPortal.is_prof', raise_exception=True)
def create_announcement(request,pk):
    try:
        related_course=Course.objects.get(pk=pk,taught_by=request.user.profprofile)
    except Course.DoesNotExist:
        return HttpResponse("NOT FOUND")
    

    if request.method=='POST':
        form=Announcement_Form(request.POST,request.FILES)
        if form.is_valid():
            announcement=form.save(commit=False)
            announcement.by_prof=request.user.profprofile
            announcement.under_course=related_course
            print(announcement.attached_file)
            announcement.save()
            email_subject=announcement.title
            email_body=f'''  {announcement.description}
            Please check site for attachments
            
            
            from:{related_course.taught_by.user.username}
            {related_course.taught_by.under_department.department_name} Department
           Time: {announcement.posted_at}
           

            
            '''
            sender=settings.EMAIL_HOST_USER
            receiptent_list=[ec.enrolled_student.email for ec in related_course.enrolled_course_set.all()]
            send_mail(email_subject,email_body,sender,receiptent_list)
            return redirect("ProfHome")
        else:
            messages.warning(request,"Error occured Please fill form again")
            return redirect('course-announcement')
    else:
        form=Announcement_Form()
        return render(request,'announcement-form.html',context={'form':form,
                                                                "course":related_course.pk})







@login_required
@permission_required('ProfPortal.is_prof', raise_exception=True)
def add_student_to_course(request,pk,pk2):
    try:
        course=Course.objects.get(pk=pk,taught_by=request.user.profprofile)
    except Course.DoesNotExist:
        return HttpResponse('<h1>Course does not exist</h1>')
        
    else:
        try:

            student_to_add=Student_Profile.objects.get(pk=pk2)
        except Student_Profile.DoesNotExist:
         return HttpResponse('<h1>Student Not found</h1>')
            
        else:
            enrolled_course,created= Enrolled_Course.objects.get_or_create(course_name=course.course_name,course_units=course.course_units,enrolled_student=student_to_add,under_course=course)
            enrolled_course.save()
            if  created:
                messages.success(request,f'{student_to_add.user.first_name} added to {course.course_name}')

            else:
                messages.warning(request,'Student already enrolled in course')
            return redirect('course_detail',pk)
    
    

@login_required
@permission_required('ProfPortal.is_prof', raise_exception=True)
def create_eval(request,pk):
    try:
        related_course=Course.objects.get(pk=pk,taught_by=request.user.profprofile)
    except Course.DoesNotExist:
        return HttpResponse("Course NOT FOUND")
    
    if request.method=='POST':
        form=Evalv_Form(request.POST)
        if form.is_valid():
            eval=form.save(commit=False)
            eval.of_course=related_course
            eval.save()
            for enrolled_course in related_course.enrolled_course_set.all():
                Course_eval.objects.create(of_student=enrolled_course,of_eval=eval).save()
                
            messages.success(request,f'{eval.eval_name} Created')
            return redirect(eval.get_absolute_url())
        else:
            messages.warning(request,"Error occured Please fill form again")
            return redirect('create-eval')
                


    else:
        form=Evalv_Form()
        return render(request,'create-eval.html',context={"form":form,"pk":related_course.pk})
    


@login_required
@permission_required('ProfPortal.is_prof', raise_exception=True)
def create_content(request,pk):
    try:
        related_course=Course.objects.get(pk=pk,taught_by=request.user.profprofile)
    except Course.DoesNotExist:
        return HttpResponse("Course NOT FOUND")
    
    if request.method=='POST':
        form=Content_Form(request.POST,request.FILES)
        if form.is_valid():
            content=form.save(commit=False)
            content.under_course=related_course
            content.posted_by=request.user.profprofile
            content.save()
            messages.success(request,f'{content.title} posted ')
            
            return redirect('course_detail',pk)
        else:
            messages.warning(request,"Error occured Please fill form again")
            return redirect('create-content')
        
                


    else:
        form=Content_Form()
        return render(request,'create-content.html',context={"form":form,"pk":related_course.pk})
    


@login_required
@permission_required('ProfPortal.is_prof', raise_exception=True)
def eval_detail(request,pk):
    try:
        eval=Evaluation.objects.get(pk=pk)
        if eval.of_course.taught_by!=request.user.profprofile:
            return HttpResponseForbidden("Access Denied")
    except Evaluation.DoesNotExist:
        return HttpResponse("Evaluation not found")
    else:
        return render(request,'eval-detail.html',context={'eval':eval})



@login_required
@permission_required('ProfPortal.is_prof', raise_exception=True)
def mark_student(request,pk,pk2):
    if request.method=='POST':
        try:
            eval=Evaluation.objects.get(pk=pk)
            if eval.of_course.taught_by!=request.user.profprofile:
                return HttpResponse("Access Denied")
        except Evaluation.DoesNotExist:
            return HttpResponse("Evaluation not found")
        else:
            student_eval=Course_eval.objects.get(pk=pk2)
            if int(request.POST["eval_id"+str(pk2)]) <=eval.total_marks:
                student_eval.value=int(request.POST["eval_id"+str(pk2)])
                student_eval.save()
                messages.success(request,f'{student_eval.of_student.enrolled_student.user.first_name} was marked')
                return redirect('eval_detail',pk)
            else:
                messages.warning(request,f'Marks awarded cannot be greater than {eval.total_marks}')
                return redirect('eval_detail',pk)
    else:
        return redirect(request.path)

@login_required
@permission_required('ProfPortal.is_prof', raise_exception=True)
def grade_student(request,pk,pk2):
     if request.method=='POST':
        try:
            related_course=Course.objects.get(pk=pk,taught_by=request.user.profprofile)
           
        except Course.DoesNotExist:
            return HttpResponse("Course not found")
        else:
            try:
                student_course=related_course.enrolled_course_set.filter(pk=pk2).first()
            except Enrolled_Course.DoesNotExist:
              return HttpResponse('Student not registered to course')
            
            student_course.student_grade=(request.POST["grade_id"+str(pk2)])
            print(request.POST["grade_id"+str(pk2)])
            student_course.graded=True
            student_course.save()
            messages.success(request,f'{student_course.enrolled_student.user.first_name} was graded')
            return redirect('course_detail',pk)
     else:
        return redirect(request.path)
     



def remove_student_from_course(request,pk,pk2):
    try:
        related_course=Course.objects.get(pk=pk,taught_by=request.user.profprofile)
    except Course.DoesNotExist:
        return HttpResponse("Course NOT FOUND")
    
    student_to_remove=Student_Profile.objects.get(pk=pk2)
    if Enrolled_Course.objects.filter(enrolled_student=student_to_remove,under_course=related_course):
        ec=Enrolled_Course.objects.get(enrolled_student=student_to_remove,under_course=related_course)
        ec.delete()
    else:
        messages.debug(request,"Student not enrolled in course")

    return redirect(related_course.get_absolute_url())
    

    





