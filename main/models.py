from django.db import models
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO
import sys


class Newsletter(models.Model):
    email = models.EmailField(blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class LandingPagePictures(models.Model):
    caption = models.CharField(max_length=57)
    image = models.ImageField(upload_to="landing_page_pictures")
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.caption

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.caption)

        img = Image.open(self.image)
        output = BytesIO()
        img = img.resize((900, 600))
        img.save(output, format="JPEG", optimize=True, quality=100)
        output.seek(0)
        self.image = InMemoryUploadedFile(output, "ImageField",
                                          f"{self.slug}.jpg", 'image/jpeg',
                                          sys.getsizeof(output), None)
        super(LandingPagePictures, self).save(*args, **kwargs)

    def image_tag(self):
        return mark_safe("<img src='{}' height='30'/>".format(self.image.url))

    image_tag.short_description = "Image"

    class Meta:
        verbose_name_plural = "Landing Page Pictures"


class InstructorPagePictures(models.Model):
    image = models.ImageField(upload_to="instructor_page_pictures")

    def __str__(self):
        return self.image.path

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        output = BytesIO()
        img = img.resize((900, 600), Image.ANTIALIAS)
        img.save(self.image.path)

    def image_tag(self):
        return mark_safe("<img src='{}' height='30'/>".format(self.image.url))

    image_tag.short_description = "Image"

    class Meta:
        verbose_name_plural = "Instructor Page Pictures"
