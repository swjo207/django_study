from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify

from django import forms
from .models import Image

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title','url','description')
        widget={
            'url': forms.HiddenInput,
        }
    # url 입력 필드를 받아서 단순하게 확장자를 추출하여 비교한다.
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg','jpeg']
        extension = url.rsplit('.',1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('the given URL does not match valid image extensions')
        return url
    """
    override save() method keeping parameters required by ModelForm
    1) create a new image instance
    2) get url from cleaned_data dictionary of the form
    3) generate image name by slugifying title
    4) download image file and save it to media directory of the project
    5) only save form to the database when the commit parameter is True
    """
    def save(self, force_insert=False, force_update=False, commit=True):
        image = super(ImageCreateForm,self).save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = '{}.{}'.format(slugify(image.title),image_url.rsplit('.',1)[1].lower())
        # download image from URL
        response = request.urlopen(image_url)
        image.image.save(image_name,ContentFile(response.read()),save=False)
        if commit:
            image.save()
        return image

