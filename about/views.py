from django.shortcuts import render
from .models import About


def about_view(request):
    """Render the About page."""
    template = "about/about.html"
    context = {"about": About.objects.first()}
    return render(request, template, context)
