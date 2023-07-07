from django import forms
from RImageModel.models import ImageToClassifi


class ImageFaceForm(forms.Form):
    
    image = forms.ImageField()
    
    def save(self):
        imageC = ImageToClassifi()
        imageC.image = self.cleaned_data["image"]
        imageC.save()

        return imageC



