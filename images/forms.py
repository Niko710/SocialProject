import requests
from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify

from images.models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['url', 'title', 'description']
        widgets = {
            'url': forms.HiddenInput
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        extensions = ['png', 'jpeg', 'jpg']
        image_ext = url.rsplit('.', 1)[1].lower()
        if image_ext not in extensions:
            forms.ValidationError('This image extension is not supported')
        return url

    def save(self, force_insert=False,  force_update=False, commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        extension = image_url.rsplit('.')[1].lower()
        name = slugify(image.title)
        image_name = f'{name}.{extension}'
        response = requests.get(image_url)
        image.image.save(image_name, ContentFile(response.content), save=False)

        if commit:
            image.save()

        return image
