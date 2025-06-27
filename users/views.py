from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm


@login_required  # Ensures only logged-in users can access this view
def profile(request):
    """
    Handles user profile viewing and updating.
    Combines both User model and Profile model updates.
    
    GET: Displays the current user's profile information in editable forms
    POST: Processes profile updates and saves changes to both User and Profile models
    """
    if request.method == 'POST':
        # Initialize forms with submitted data and current user instances
        user_form = UserUpdateForm(
            request.POST, 
            instance=request.user  # Bind to current user
        )
        profile_form = ProfileUpdateForm(
            request.POST,  # Form data
            request.FILES,  # Handle file uploads (profile image)
            instance=request.user.profile  # Bind to current user's profile
        )

        # Validate and save both forms
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()  # Update User model
            profile_form.save()  # Update Profile model
            return redirect('profile')

    else:
        # GET request - populate forms with current user data
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    # Context data for template rendering
    context = {
        'user_form': user_form,  # Form for user data (first/last name, email)
        'profile_form': profile_form  # Form for profile data (bio, image)
    }

    return render(request, 'users/profile.html', context)