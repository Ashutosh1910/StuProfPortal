from django.contrib import admin
from .models import * 
# Register your models here.
admin.site.register([Student_Profile,Enrolled_Course,Course_eval])