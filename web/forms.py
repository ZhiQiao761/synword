import os

from django import forms
from django.utils.functional import cached_property


class UploadForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        cd = self.cleaned_data['file']
        ext = os.path.splitext(cd.name)[1]
        if not ext.lower() in self.supported_exts:
            raise forms.ValidationError(u'Unsupported file extension.')
        return cd

    @cached_property
    def supported_exts(self):
        return ['.docx']
