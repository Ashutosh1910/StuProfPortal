from django import forms 
from .models import Student_Profile,Enrolled_Course
from ProfPortal.models import Course


class StudentProfile_Form(forms.ModelForm):
   
   
   class Meta:
        model=Student_Profile
        fields=['branch']


class ElectiveForm(forms.Form):
    electives_available=forms.ModelMultipleChoiceField(Course.objects.all(),widget=forms.CheckboxSelectMultiple)

class CGPA_CalcForm(forms.ModelForm):
    class Meta:
        model=Enrolled_Course
        fields=['expected_grade']