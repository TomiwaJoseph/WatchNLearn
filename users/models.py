from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.conf import settings
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from courses.models import Course
from resizeimage import resizeimage


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """User model"""
    username = None
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_instructor = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def get_name(self):
        return super().get_full_name()

    def __str__(self):
        return self.first_name + " " + self.last_name


class Instructor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="user_instructor")
    profile_picture = models.ImageField(upload_to='profile_pics')
    expert_in = models.ForeignKey("courses.Category", on_delete=models.CASCADE, null=True,
                                  related_name="instructor_expertise_area")
    descriptions = TaggableManager()
    about = RichTextField()

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def save(self, *args, **kwargs):
        full_name = self.user.first_name + "_" + self.user.last_name
        with Image.open(self.profile_picture) as image:
            cover = resizeimage.resize_cover(image, [300, 300])
            cover = cover.convert('RGB')
            output = BytesIO()
            cover.save(output, format="JPEG", optimize=True, quality=100)
            output.seek(0)
            self.profile_picture = InMemoryUploadedFile(output, "ImageField",
                                                        f"{full_name}.jpg", 'image/jpeg',
                                                        sys.getsizeof(output), None)

        super(Instructor, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    courses_bought = models.ManyToManyField(to="courses.Course", blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " 's Profile"


class BookmarkList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name="user_bookmarks", null=True)
    folder = models.ManyToManyField(Course, blank=True)

    def __str__(self):
        return "{}'s bookmarks".format(self.user)
