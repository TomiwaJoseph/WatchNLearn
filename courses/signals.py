from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Course
from users.models import CustomUser


@receiver(post_save, sender=Course)
def create_students(sender, instance, created, **kwargs):
    if created:
        # Add all superusers as students
        all_superusers = CustomUser.objects.filter(is_superuser=True)
        instance.students.add(*all_superusers)
        
        # Add the course as a bought course for all superusers
        for user in all_superusers:
            user.profile.courses_bought.add(instance)

post_save.connect(create_students, sender=Course)

