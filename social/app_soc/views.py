from django.shortcuts import render, redirect
from .models import Profile
from .forms import DweetForm
from django.contrib.auth.decorators import login_required

def dashboard(request):

    form = DweetForm(request.POST or None)  
    if request.method == "POST":
        form = DweetForm(request.POST)
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.user = request.user
            dweet.save()
            return redirect("app_soc:dashboard.html")
    form = DweetForm()
    return render(request, "app_soc/dashboard.html", {"form": form})

def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "app_soc/profile_list.html", {"profiles": profiles})

@login_required
def profile(request, pk):
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()

    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()    

    return render(request, "app_soc/profile.html", {"profile": profile})
