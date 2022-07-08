# after creating this file, add a few lines to catcollector/urls.py
# in order to import the views it requires a few dependences we need:
from django.urls import path
from . import views

# we will define all app-level urls
urlpatterns = [
    # empty string, no space, for root route
    path('', views.home, name='home'),
    # trailing backslash, not starting. this makes it like this: url.com/about
    path('about/', views.about, name='about'),
    path('cats/', views.cats_index, name='index'),
    path('cats/<int:cat_id>/', views.cats_details, name='details'),
    # The int:part is called a converter and it's used to match and convert the
    # captured value from a string into, in this case, an integer. If the info in
    # the segment does not look like an integer, then it will not be matched
    path('cats/create/', views.CatCreate.as_view(), name='cats_create'),
    # notice that create does not need to be before the details/view page. this is
    # because python can recognize that the views is looking for something that looks
    # like an interger, therefore 'create' is not taken as a view
    # to finish create path, need to add reverse to models
    path('cats/<int:pk>/update/', views.CatUpdate.as_view(), name='cat_update'),
    path('cats/<int:pk>/delete/', views.CatDelete.as_view(), name='cat_delete'),
    # By default, CBVs that work with individual model instances will expect to
    # find a named parameter of pk. This is why we didn't use cat_id as we did in
    # the detail entry. in short, its just how django works. remember to add the
    # views and the html
    path('cats/<int:cat_id>/add_feeding/', views.add_feeding, name='add_feeding'),
    path('toys/', views.ToyList.as_view(), name='toys_index'),
    path('toys/<int:pk>/', views.ToyDetail.as_view(), name='detail'),
    path('toys/create/', views.ToyCreate.as_view(), name='toys_create'),
    path('toys/<int:pk>/update/', views.ToyUpdate.as_view(), name='toys_update'),
    path('toys/<int:pk>/delete/', views.ToyDelete.as_view(), name='toys_delete'),
    path('cats/<int:cat_id>/add_feeding/', views.add_feeding, name='add_feeding'),
    # associate a toy with a cat (M:M) ^
    path('cats/<int:cat_id>/add_photo/', views.add_photo, name='add_photo'),
    path('cats/<int:cat_id>/assoc_toy/<int:toy_id>/', views.assoc_toy, name='assoc_toy'),
    path('cats/<int:cat_id>/assoc_toy/<int:toy_id>/delete/', views.assoc_toy_delete, name='assoc_toy_delete'),
    # toys paths added with model ^
    path('accounts/signup', views.signup, name='signup'),
    # we are staying consistent ^ with Django's prebuilt auth-based URLS, and laying
    # groundwork to build our own signup view.
]

"""
That name argument within each path is used to obtain the correct URL in templates
using DTL's url template tag, this makes it so we dont need to hardcode the path
in the templates
"""