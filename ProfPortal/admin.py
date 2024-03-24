from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register([ProfProfile,Department,Course,Evaluation,Announcement,Branch,Study_Material])