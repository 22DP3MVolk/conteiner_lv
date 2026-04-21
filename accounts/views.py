from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from .forms import UserRegistrationForm


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # We do not log in automatically, as confirmation is required
            messages.success(
                request, 
                'Thank you for registering! Your account has been created and is pending approval. '
                'You will receive an email notification once an administrator approves your account.'
            )
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    
    def form_invalid(self, form):
        # Checking if the user exists but is not verified
        username = self.request.POST.get('username')
        from .models import User
        try:
            user = User.objects.get(username=username)
            if not user.is_approved:
                return redirect(f'{reverse_lazy("accounts:login")}?next=inactive')
        except User.DoesNotExist:
            pass
        return super().form_invalid(form)