from django.db import models
from django.contrib.auth.models import User
#from ProfPortal.models import Course,Branch,Evaluation


grades=(('10','A',),
        ('9','A-',),
        ('8','B',),
        ('7','B-',),
        ('6','C',),
        ('5','C-',),
        ('4','D',),
        ('3','E',)
        )
grds={"A":10,"B":8,"A-":9,"B-":7,"C":6,"C-":5,"D":4,"E":3}




# Create your models here.
class Student_Profile(models.Model):
    
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    cgpa=models.DecimalField(default=0.00,max_length=3,max_digits=3,decimal_places=1)
    #branch_choices=((branch.branch_name,branch.branch_name) for branch in Branch.objects.all() )
    branch=models.ForeignKey('ProfPortal.Branch',on_delete=models.CASCADE,null=True)
    email=models.EmailField()
    bits_id=models.CharField(max_length=15)
    expected_cgpa=models.DecimalField(default=0.00,max_length=3,max_digits=3,decimal_places=1)
    

    def __str__(self)  :
        return f'{self.user.username}   {self.branch}   {self.cgpa}'
    @property
    def calc_cgpa(self):
        
       total_units_graded=0
       total_grade=0
       for student_course in Enrolled_Course.objects.filter(enrolled_student=self):
           if student_course.graded==True:
               total_units_graded+=student_course.course_units
               total_grade+=(grds[student_course.student_grade])*student_course.course_units
               if total_units_graded==0:
                return 0
               
       if total_units_graded!=0:
            return total_grade/total_units_graded
    @property
    def calc_ex_cgpa(self):
       total_units_graded=0
       total_grade=0
       for student_course in Enrolled_Course.objects.filter(enrolled_student=self):
               if student_course.expected_grade!='Not selected':
                total_units_graded+=student_course.course_units
                total_grade+=(grds[student_course.expected_grade])*student_course.course_units
                if total_units_graded==0:
                    return 0
               
       if total_units_graded!=0:
            return total_grade/total_units_graded





class Enrolled_Course(models.Model):
    course_name=models.CharField(max_length=15)
    course_units=models.PositiveIntegerField(default=0)
    student_grade=models.TextField(max_length=20,default='Not Awarded')
    graded=models.BooleanField(default=False)
    enrolled_student=models.ForeignKey(Student_Profile,on_delete=models.CASCADE)
    under_course=models.ForeignKey('ProfPortal.Course',on_delete=models.CASCADE,null=True)
    expected_grade=models.TextField(default="Not selected",choices=grades)

    

    def __str__(self)  :
        return f'{self.course_name}   {self.student_grade}   {self.enrolled_student.user.username}'
    
class Course_eval(models.Model):
    of_eval=models.ForeignKey('ProfPortal.Evaluation',on_delete=models.CASCADE)
    of_student=models.ForeignKey(Enrolled_Course,on_delete=models.CASCADE)
    value=models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f'{self.of_eval.eval_name}   {self.of_student.enrolled_student.user.username}   {self.value}'
