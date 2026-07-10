from django.views.generic import DetailView

from .models import About


class AboutView(DetailView):
    context_object_name = "about"
    model = About
    template_name = "about/about.html"

    def get_object(self):
        return About.objects.first()
