from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.views.generic import FormView

from web.forms import UploadForm
from web.text import extract_text, modify


class HomeView(FormView):
    template_name = 'web/home.html'
    form_class = UploadForm

    def form_valid(self, form):
        try:
            text = extract_text(form.cleaned_data['file'])
            modified_text = modify(text)
        except Exception as e:
            text = f'Cannot parse file ({e}).'
            modified_text = None
        ctx = self.get_context_data(
            original_text=text,
            modified_text=modified_text
        )
        return render(self.request, 'web/home.html', ctx)
