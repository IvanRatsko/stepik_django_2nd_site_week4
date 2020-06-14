from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.views.generic.edit import FormView

from accounts.forms import RegistrationUserCreationForm, LoginAuthenticationForm


# Create your views here.


class RegisterView(FormView):
    form_class = RegistrationUserCreationForm
    success_url = '/login/'
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        form.save()
        return super(RegisterView, self).form_valid(form)


class MyLoginView(FormView):
    redirect_authenticated_user = True
    template_name = 'accounts/login.html'
    form_class = LoginAuthenticationForm
    success_url = '/'

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(MyLoginView, self).form_valid(form)


class MyLogoutView(LogoutView):
    redirect_authenticated_user = False
    template_name = 'accounts/login.html'
