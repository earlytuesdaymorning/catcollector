from django.db import models
from django.urls import reverse # import reverse to allow redirection in create route
from datetime import date

MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner'),
)
# we are representing our meals in a tuple filled with two-tuples. these work as
# key:value pairs. django sees these and will automatically understand that those
# letters in the key location represent the words in the value location.

# Create your models here.

# Toys model added
class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.color} {self.name}'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.id})

class Cat(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    # Add the M:M relationship
    toys = models.ManyToManyField(Toy)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('details', kwargs={'cat_id': self.id})
    
    def fed_for_today(self):
        return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)
    # The fed_for_today method demonstrates the use of filter() to obtain a
    # <QuerySet> for today's feedings, then count() is chained on to the query
    # to return the actual number of objects returned.
"""
The reverse function builds a path string. The above will return the correct
path for the details named route. However, since that route requires a cat_id
route parameter, its value must provided as a shown above.
what it is basically doing is creating a new url and taking you there when you hit
submit. the form works on its own and will add to the database, but you cannot see
it until you reverse and update the list
"""
class Feeding(models.Model):
    date = models.DateField('feeding date') # adding this in the parameter makes what
    # is essentially a label for the date field.
    meal = models.CharField(
        max_length=1,
# Note that we're going to use just a single character to represent what meal
# the feeding is for: Breakfast, Lunch or Dinner.
# we are going to need to use Field.choices and define some two-tuples at the top of
# the file to show a helpful dropdown, so the user is not confused on what to enter
        choices=MEALS, # adding the choices as the tuple we defined above
        default=MEALS[0][0] # default value being the first[0] in the tuple, 'B'
    )
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
    # In a one-to-many relationship, the on_delete = models.CASCADE is required.
    # It ensures that if a Cat record is deleted, all of the child Feedings will be
    # deleted automatically as well, thus avoiding orphan records
    # (seriously, that's what they're called).
    def __str__(self):
        return f"{self.get_meal_display()} on {self.date}"
    # Check out the convenient get_meal_display() method Django autoMAGICally
    # creates from the "meal" field. this gives access to the value of a
    # Field.choice. it is created when we make the choices= argument.
    # Since a Feeding belongs to a Cat, it must hold the id of the cat object it
    # belongs to! so we also added a foreign key.
    class Meta: # we can add meta attributes to our models also
        ordering = ['-date'] # in this case, to change the default sorting, so most
        # recent date first

class Photo(models.Model):
    url = models.CharField(max_length=200)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for cat_id: {self.cat_id} @{self.url}"
# If a Model "belongs to" another Model, it must have a foreign key. If there's more
#  than one "belongs to" relationship - that means more than one foreign key.


# REMEMBER TO makemigrations AND migrate ANY TIME WE ADD TO/CHANGE OUR MODELS
# python manage.py showmigrations to see what you are migrating
# you'll see what you already migrated [x] and what you havent yet [ ]
# it is also a good idea to test the model in the shell
