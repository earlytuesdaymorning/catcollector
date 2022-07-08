# Add the following import
# from django.http import HttpResponse # this is for testing the routes
from distutils.log import error
from multiprocessing import context
from nis import cat
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView # this generic import will allow
# us to generate a simple create form based on our model.
from django.views.generic.edit import UpdateView, DeleteView # you can just add them
# all at once by separating by commas
from django.views.generic import ListView # added with Toys
from django.views.generic.detail import DetailView # added with Toys
from django.contrib.auth import login # lines 13/16 ARE included with djgango auth.
# login also creates a session store that's stored in the database, and a session
# cookie that's sent to the browser.
from django.contrib.auth.forms import UserCreationForm # even though there is no
# user creation view or url, which makes it easier to customize, it does give you
# a default user creation form to work with
from django.contrib.auth.decorators import login_required # this will make it so when
# we decorate a view with it, you will not be allowed to see the page unless they are
# logged in
from django.contrib.auth.mixins import LoginRequiredMixin # this will import the
# mixin that we will used to authorize/restrict the CLASS-based views, and which is
# implemented with multiple inheritance
from .models import Cat, Toy, Photo
from .forms import FeedingForm
import uuid  # a python utility that will help us generate random strings
import boto3 # this is the AWS boto3 library

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'tuesdayscatcollector'

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

@login_required # we'll need to place the decorator above the view we want to restrict
def cats_index(request):
    # This reads ALL cats, not just the logged in user's cats. this CAN be useful
    # if we want to have a space for everyone to show their contributions.
    # cats = Cat.objects.all()
    cats = Cat.objects.filter(user=request.user)
    # this^ will filter and dsiplay the requesting user's cats only, or this v
    # cats = request.user.cat_set.all() , which displays all the cats set to the
    # current user.
    return render(request, 'cats/index.html', { 'cats': cats })

# we are going to be using seed data for testing. but the key vaule here references
# the cats that will be in our index, connecting to the DB

@login_required
def cats_details(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    toys_cat_doesnt_have = Toy.objects.exclude(id__in=cat.toys.all().values_list('id'))
    feeding_form = FeedingForm() # instantiating FeedingForm to be rendered
    return render(request, 'cats/details.html', {
        'cat': cat, 'feeding_form': feeding_form, 'toys': toys_cat_doesnt_have
        # including feeding_form along with the cat model, and adding toys
    })

@login_required
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

@login_required
def assoc_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('details', cat_id=cat_id)

@login_required
def assoc_toy_delete(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.remove(toy_id)
    return redirect('details', cat_id=cat_id)

@login_required
def add_photo(request, cat_id):
    # attempting to collect the photo file data
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)

    # conditional logic to determine if file is present...
    if photo_file:
        # ...if it IS then we will create a reference to the boto3 client
        s3 = boto3.client('s3')
        # we'll then need a unique "key" for S3, and an image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
            # what uuid.uuid4() does is create a long, unique string of characters
            # .hex with slice operator [:6] will shorten that unique string to only
            # be 6 characters long.
            # then + the file type that is being uploaded... we are taking the photo
            # file's name[then rfinding the '.': <- and then slicing it right there]
            # basically this will replace 'file_name.png' with 'bd504f.png'

        # if the IF above is successful...
        try:
            # ...upload that photo file to aws s3. any time we upload to s3 it will
            # give us a predictable URL in exchange.
            s3.upload_fileobj(photo_file, BUCKET, key)
            # we will take the exchanged url and save it to the database, URLs
            # exchanged with aws s3 will always be laid out this way
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
                # reminder that we defined S3_BASE_URL and BUCKET at the top and key
                # within this def's if statement
            # this will create a photo instance with the photo model we have and
            # provide the cat_id as as a foreign key value
            photo = Photo(url=url, cat_id=cat_id)
            # save the photo instance
            photo.save()
        # if the IF above is not successful...
        except Exception as error:
            # print an error message along with what caused it as defined above
            print('An error occurred uploading file to S3:', error)
    # finally we will redirect to the details page
    return redirect('details', cat_id=cat_id)

def signup(request):
    error_message = ''
    # IF the request is POST == we need to create a new user, because a form was
    # just submitted. it's implied here that if its not POST, it is GET. and if its
    # GET that means the user just clicked the signup link. doing this just
    # consolidated the signup view function into one, rather than making separate
    # views for get and for post
    if request.method == 'POST':
        form = UserCreationForm(request.POST) # this defines form as a function that
        # will create a 'user' from the post request on the submitted form instance
        if form.is_valid():
        # if ^ form is valid, then v it will save the new user to our database...
            user = form.save()
            login(request, user) # ...then it will log the new user in...
            return redirect('index') # ...and take them to the cat index, by url name
        else:
            error_message = 'Invalid sign up - try again'
    # this v is where it assumes a GET request (implied else) or a bad POST request
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message} # save an error message
    # creating a nested variable called context and passing it below allows us to
    # break our code up a bit and make it easier to look at.
    return render(request, 'registration/signup.html', context)
    # ^ and render an empty form

# we are going to MIX in the mixin here before our imported view, restricting access
# to a user only
class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    # fields = '__all__' -now with toys being added, we are going to change __all__
    # because we no longer want ALL the fields showing up when we add a new cat
    fields = ['name', 'breed', 'description', 'age']

    # The inherited method below is called when a valid cat form is being submitted
    def form_valid(self, form):
        form.instance.user = self.request.user # this assigns the cat to the user
        # that is currently logged in when the cat is created
        return super().form_valid(form) # after that, this line lets CreateView do
        # its normal job

class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    # Let's disallow the renaming of a cat and their breed by excluding those fields!
    fields = ['description', 'age']

class CatDelete(LoginRequiredMixin, DeleteView):
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

class ToyList(LoginRequiredMixin, ListView):
    model = Toy
    template_name = 'toys/index.html'

class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy
    template_name = 'toys/detail.html'

class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = ['name', 'color']

class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
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