from django.db import models
from django.conf.locale import LANG_INFO
from taggit.managers import TaggableManager
from django.conf import settings
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO
import sys
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.template.loader import render_to_string


language_list = [(k, v['name']) for k, v in LANG_INFO.items() if len(v) > 1]
star_list = [('1', 'One star'), ('2', 'Two stars'), ('3', 'Three stars'),
             ('4', 'Four stars'), ('5', 'Five stars')]
course_status = [('draft', 'Draft'), ('published', 'Published')]


class Category(models.Model):
    category_title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ['category_title']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_title


class Course(models.Model):
    instructor = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE,
                                   related_name='course_instructor')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='course_category')
    language = models.CharField(max_length=50, choices=language_list)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    thumbnail_image = models.ImageField(upload_to="course_thumbnails")
    price = models.IntegerField()
    about_the_course = RichTextField()
    date_created = models.DateTimeField(auto_now_add=True)
    keywords = TaggableManager()
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='course_student', blank=True)
    status = models.CharField(max_length=50, choices=course_status)

    class Meta:
        ordering = ['date_created']

    def get_stripe_price(self):
        return int(self.price) * 100

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        img = Image.open(self.thumbnail_image)
        output = BytesIO()
        img = img.resize((300, 200))
        img.save(output, format="JPEG", optimize=True, quality=100)
        output.seek(0)
        self.thumbnail_image = InMemoryUploadedFile(output, "ImageField",
                                                    f"{self.slug}.jpg", 'image/jpeg',
                                                    sys.getsizeof(output), None)
        super(Course, self).save(*args, **kwargs)


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='course_modules')
    module_title = models.CharField(max_length=200)
    module_title_slug = models.SlugField(max_length=200, null=True)

    def __str__(self):
        return self.course.title + " - " + self.module_title

    def save(self, *args, **kwargs):
        if not self.module_title_slug:
            self.module_title_slug = slugify(self.module_title)
        super(Module, self).save(*args, **kwargs)


class Content(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE,
                               related_name='modules_content')
    title = models.CharField(max_length=50)
    content_description = RichTextField()
    content_video = models.FileField(upload_to='content_videos')
    content_image = models.ImageField(
        upload_to='content_images', null=True, blank=True)
    content_file = models.FileField(
        upload_to="content_files", null=True, blank=True)

    def __str__(self):
        return f"{self.module}'s content"


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='course_review')
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stars = models.CharField(max_length=20, choices=star_list)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.student.get_name() + "'s review"
