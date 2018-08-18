from django.shortcuts import render_to_response
from django.views.generic import FormView

from web.forms import UploadForm
from web.text import extract_text, modify


class HomeView(FormView):
    template_name = 'web/home.html'
    form_class = UploadForm

    def form_valid(self, form):
        text = extract_text(form.cleaned_data['file'].file)
        modified_text = modify(text)
        ctx = self.get_context_data(
            original_text=text,
            modified_text=modified_text
        )
        return render_to_response('web/home.html', ctx)
