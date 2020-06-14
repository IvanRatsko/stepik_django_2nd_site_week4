from django.urls import path

from accounts.views import MyLoginView
from accounts.views import MyLogoutView
from accounts.views import RegisterView

urlpatterns = [
    path('login/', MyLoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('logout/', MyLogoutView.as_view()),

]
