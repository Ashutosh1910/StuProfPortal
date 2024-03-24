from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
class Department(models.Model):
    department_name=models.CharField(max_length=15)
    def __str__(self):
        return f'{self.department_name}'


class ProfProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    under_department=models.ForeignKey(Department,on_delete=models.SET_NULL,null=True)
    phone_no=models.PositiveBigIntegerField(default=0)
    def __str__(self):
        return f'{self.user.username}'



class Branch(models.Model):
    branch_name=models.CharField(max_length=15)
    branch_code=models.CharField(max_length=3)
    def __str__(self):
        return f'  {self.branch_name}    '


class Course(models.Model):
    course_name=models.CharField(max_length=15)
    course_units=models.PositiveIntegerField(default=0)
    course_code=models.CharField(max_length=9)
    under_department=models.ForeignKey(Department,on_delete=models.CASCADE)
    taught_by=models.ForeignKey(ProfProfile,on_delete=models.CASCADE)
    compulsary_to=models.ManyToManyField(Branch,blank=True)
    def __str__(self):
        return f'{self.course_name}({self.course_code})         Units:{self.course_units}           Taught by:   {self.taught_by.user.username}'
    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"pk": self.pk})
    
    class Meta:
        permissions=[('is_prof','is a prof'),
                     ('is_student','is a student')]


class Announcement(models.Model):
    title=models.CharField(max_length=15)
    description=models.TextField()
    attached_file=models.FileField(upload_to="announcement_files/",null=True,blank=True)
    by_prof=models.ForeignKey(ProfProfile,on_delete=models.CASCADE)
    under_course=models.ForeignKey(Course,on_delete=models.CASCADE)
    posted_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.title}   {self.under_course.course_name} {self.by_prof.user.first_name}'


class Evaluation(models.Model):
    eval_name=models.CharField(max_length=15)
    total_marks=models.PositiveIntegerField(default=0)
    of_course=models.ForeignKey(Course,on_delete=models.CASCADE,)
    def __str__(self):
        return f'{self.eval_name}   {self.of_course.course_name}'
    def get_absolute_url(self):
        return reverse("eval_detail", kwargs={"pk": self.pk})
    

class Study_Material(models.Model):
    title=models.CharField(max_length=15)
    under_course=models.ForeignKey(Course,on_delete=models.CASCADE)
    posted_at=models.DateTimeField(auto_now_add=True)
    material=models.FileField(upload_to="study_material_files/",null=True,blank=True)
    posted_by=models.ForeignKey(ProfProfile,on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.material.url}  {self.under_course.course_name}'

    




