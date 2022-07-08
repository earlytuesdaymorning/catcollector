"""catcollector URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include # add include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')), # add this line
    # include the built-in auth urls for the built-in views
    path('accounts/', include('django.contrib.auth.urls')),
]

"""
including the auth path above imports all of these URL patterns:

accounts/login/ [name='login']
accounts/logout/ [name='logout']
accounts/password_change/ [name='password_change']
accounts/password_change/done/ [name='password_change_done']
accounts/password_reset/ [name='password_reset']
accounts/password_reset/done/ [name='password_reset_done']
accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/reset/done/ [name='password_reset_complete']

but we get to pick and choose which ones to actually use. because auth is included
with django, it is a universal app in our catcollector! so we automatically have a
user variable available in every template

we also will need to create a user signup url in our main_app urls as its not included

now to make a new folder inside of templates, registration/login.html
"""


