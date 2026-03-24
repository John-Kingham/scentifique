from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from profiles.forms import UserProfileForm
from profiles.models import UserProfile


@login_required
def profile(request):
    """Display the user profile page."""

    # Load the form and save if this is a post request.
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
        else:
            messages.error(
                request, "Update failed. Please check that the form is valid."
            )
    else:
        form = UserProfileForm(instance=profile)

    template = "profiles/profile.html"
    context = {
        "form": form,
    }
    return render(request, template, context)
