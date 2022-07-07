from django.forms import ModelForm # importing this to be able to write our own CBV
from .models import Feeding

class FeedingForm(ModelForm): # extending the ModelForm class to apply it here as
    # FeedingForm. we can use some of the methods from ModelForm selectively
    class Meta: # a special subclass that allows to set metadata and separate concerns
        model = Feeding
        fields = ['date', 'meal'] # because there are only two items here, i could
        # also use () to make a two tuple as it would be recognized the same way.
        # any more than two though it needs to be a [] list

# the nested class, Meta, declares the Model being used and the fields
# we want inputs generated for. many of Meta's attributes are used for other CBVs
# behind the scenes already. there is django documentation on all the options

# in views we will need to update the cat details route to import the new form and
# allow it to render in the details.html page