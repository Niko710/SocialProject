from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy
from django.utils.text import slugify


class Image(models.Model):
    user = models.ForeignKey(User, related_name='images_created', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    url = models.URLField(max_length=2000)
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)
    users_like = models.ManyToManyField(User, related_name='liked_images', blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created'])
        ]
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('images:detail', args=[self.id, self.slug])


