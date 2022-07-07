# Add the following import
# from django.http import HttpResponse # this is for testing the routes
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView # this generic import will allow
# us to generate a simple create form based on our model.
from django.views.generic.edit import UpdateView, DeleteView # you can just add them
# all at once by separating by commas
from django.views.generic import ListView # added with Toys
from django.views.generic.detail import DetailView # added with Toys
from .models import Cat, Toy
from .forms import FeedingForm

"""
note: to DRY our code, we are including a base.html.
this will create a template inheritance base. a file that includes everything that
will be going to EVERY page. sort of like django's version of partials
"""

# Create your views here.
def home(request):
    """
    this is where we return a response
    in most cases we would render a template
    we will need some data for that template
    """
    # return HttpResponse("<h1>Hello /ᐠ｡‸｡ᐟ\ﾉ</h1>")
    return render(request, 'home.html')

def about(request):
    # we will not use the simple HttpResponse
    # return HttpResponse("<h1>About the CatCollector</h1>")
    return render(request, 'about.html')
    # instead we return a RENDER, and we'll REQUEST from django that they give us
    # the file 'about.html'

"""
we are going to be linking our url to another template with our views.
this time, we will structure it similarly to static, in that we will be creating
a FOLDER called cats first, then then within that we have our template.
"""

def cats_index(request):
    cats = Cat.objects.all()
    return render(request, 'cats/index.html', { 'cats': cats })

# we are going to be using seed data for testing. but the key vaule here references
# the cats that will be in our index, connecting to the DB

def cats_details(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    toys_cat_doesnt_have = Toy.objects.exclude(id__in=cat.toys.all().values_list('id'))
    feeding_form = FeedingForm() # instantiating FeedingForm to be rendered
    return render(request, 'cats/details.html', {
        'cat': cat, 'feeding_form': feeding_form, 'toys': toys_cat_doesnt_have
        # including feeding_form along with the cat model, and adding toys
    })

def add_feeding(request, cat_id):
    # create the ModelForm using the data in request.POST
    form = FeedingForm(request.POST)
    # validate the form
    if form.is_valid():
        # don't save the form to the db until it has the cat_id assigned
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = cat_id
        new_feeding.save()
    return redirect('details', cat_id=cat_id)

def assoc_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('details', cat_id=cat_id)

class CatCreate(CreateView):
    model = Cat
    # fields = '__all__' -now with toys being added, we are going to change __all__
    # because we no longer want ALL the fields showing up when we add a new cat
    fields = ['name', 'breed', 'description', 'age']

class CatUpdate(UpdateView):
    model = Cat
    # Let's disallow the renaming of a cat and their breed by excluding those fields!
    fields = ['description', 'age']

class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats/'

"""
The fields attribute is required and can be used to limit or change the ordering
of the attributes, for example, if we did not want to allow them to change the
name, we would not have included it here.
we could have listed like this: ['name', 'breed', 'description', 'age'], where
changing the order would make it appear that way in the create view

By convention, the CatCreate CBV will look to render a template named
templates/main_app/cat_form.html. All CBVs by default will use a folder inside
of the templates folder with a name the same as the app, in our case main_app.
"""

class ToyList(ListView):
    model = Toy
    template_name = 'toys/index.html'

class ToyDetail(DetailView):
    model = Toy
    template_name = 'toys/detail.html'

class ToyCreate(CreateView):
    model = Toy
    fields = ['name', 'color']

class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'

# This seed data is just here for testing. v

# Add the Cat class & list and view function below the imports
# class Cat:  # Note that parens are optional if not inheriting from another class
#   def __init__(self, name, breed, description, age):
#     self.name = name
#     self.breed = breed
#     self.description = description
#     self.age = age

# cats = [
#     Cat('Lolo', 'tabby', 'foul little demon', 3),
#     Cat('Sachi', 'tortoise shell', 'diluted tortoise shell', 0),
#     Cat('Raven', 'black tripod', '3 legged cat', 4),
#     Cat('Clementine', 'black domestic longhair', 'prissy princess', 6)
# ]