from django.db import models
from django.contrib.auth.models import User
#from ProfPortal.models import Course,Branch,Evaluation


grades=(('A','A',),
        ('A-','A-',),
        ('B','B',),
        ('B-','B-',),
        ('C','C',),
        ('C-','C-',),
        ('D','D',),
        ('E','E',)
        ,('NC','NC'))






# Create your models here.
class Student_Profile(models.Model):
    
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    cgpa=models.DecimalField(default=0.00,max_length=3,max_digits=3,decimal_places=1)
    #branch_choices=((branch.branch_name,branch.branch_name) for branch in Branch.objects.all() )
    branch=models.ForeignKey('ProfPortal.Branch',on_delete=models.CASCADE,null=True)
    email=models.EmailField()
    bits_id=models.CharField(max_length=15)

    def __str__(self)  :
        return f'{self.user.username}   {self.branch}   {self.cgpa}'


class Enrolled_Course(models.Model):
    course_name=models.CharField(max_length=15)
    course_units=models.PositiveIntegerField(default=0)
    student_grade=models.TextField(max_length=20,default='Not Awarded')
    graded=models.BooleanField(default=False)
    enrolled_student=models.ForeignKey(Student_Profile,on_delete=models.CASCADE)
    under_course=models.ForeignKey('ProfPortal.Course',on_delete=models.CASCADE,null=True)

    

    def __str__(self)  :
        return f'{self.course_name}   {self.student_grade}   {self.enrolled_student.user.username}'
    
class Course_eval(models.Model):
    of_eval=models.ForeignKey('ProfPortal.Evaluation',on_delete=models.CASCADE)
    of_student=models.ForeignKey(Enrolled_Course,on_delete=models.CASCADE)
    value=models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f'{self.of_eval.eval_name}   {self.of_student.enrolled_student.user.username}   {self.value}'
