# from django.shortcuts import render
from django.views.generic import TemplateView

# def index(request):
#     """A view for the home page."""
#     return render(request, "home/index.html")


class IndexView(TemplateView):
    template_name = "home/index.html"
