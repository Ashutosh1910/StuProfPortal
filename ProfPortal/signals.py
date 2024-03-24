from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Course
from django.shortcuts import redirect
from allauth.socialaccount.models import SocialAccount
from StudentPortal.models import Student_Profile
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Permission

from .models import ProfProfile
from django.urls import reverse
@receiver(post_save,sender=SocialAccount)
def create_profile(sender,created,instance,**kwargs):
    if created:
        if SocialAccount.objects.filter(user=instance.user).exists():
            Student_Profile.objects.create(user=instance.user).save()
            course_content_type = ContentType.objects.get_for_model(Course)

            instance.user.user_permissions.add(Permission.objects.get(content_type=course_content_type,codename='is_student'))
            instance.user.save()
           # return redirect(reverse('createstudentprofile'))

        