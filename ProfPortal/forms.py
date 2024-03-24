from django import forms
from .models import ProfProfile,Course,Announcement,Study_Material,Branch,Evaluation,Department

class ProfProfile_Form(forms.ModelForm):
    class Meta:
        model=ProfProfile
        fields=[]



class New_Course_Form(forms.ModelForm):
    CDC_to=forms.ModelMultipleChoiceField(Branch.objects.all(),widget=forms.CheckboxSelectMultiple)
   # under_department=forms.ModelChoiceField(Department.objects.all(),widget=forms.Select)
    class Meta:
        model=Course
        fields=['course_name','course_units','course_code','CDC_to','under_department']


class Announcement_Form(forms.ModelForm):
    class Meta:
        model=Announcement
        fields=['title','description','attached_file']

class Content_Form(forms.ModelForm):
    class Meta:
        model=Study_Material
        fields=['title','material']

class Evalv_Form(forms.ModelForm):
    class Meta:
        model=Evaluation
        fields=['eval_name','total_marks']