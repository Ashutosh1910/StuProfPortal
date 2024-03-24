from django import forms 
from .models import Student_Profile
from ProfPortal.models import Course


class StudentProfile_Form(forms.ModelForm):
   
   
   class Meta:
        model=Student_Profile
        fields=['branch']


class ElectiveForm(forms.Form):
    electives_available=forms.ModelMultipleChoiceField(Course.objects.all(),widget=forms.CheckboxSelectMultiple)