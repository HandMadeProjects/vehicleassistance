
from django.db import models
from django.contrib.auth.models import User

# -------------- USER -------------------------------

class UserProfile(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    U_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, default="")
    fullname = models.CharField(max_length=100, default="")
    email = models.EmailField()
    age = models.IntegerField()
    date_of_birth = models.DateField()
    locationlat = models.CharField(max_length=100, default="")
    locationlong = models.CharField(max_length=100, default="")
    contact_number = models.CharField(max_length=15, default="")
    # user_type = models.CharField(max_length=100, default="")
    registerdOn = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.fullname
    
class bookingreq(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    Booking_id = models.AutoField(primary_key=True)
    U_id = models.IntegerField(default=0)
    username = models.CharField(max_length=100, default="")
    locationlat = models.CharField(max_length=100, default="")
    locationlong = models.CharField(max_length=100, default="")

    state = models.CharField(max_length=100, default="")

    message = models.CharField(max_length=500, default="")
    
    bookdate = models.CharField(max_length=15, default="")
    booktime = models.CharField(max_length=15, default="")

    assistedbyAss_id = models.IntegerField(default=0)

    status = models.CharField(max_length=15, default="") # status = new / active / done

    # slug = models.CharField(max_length=15, default="") # example : /bookingreq/3
    


    def __str__(self):
        return self.username
    
class personalchat(models.Model):
    chat_id = models.AutoField(primary_key=True)

    Booking_id = models.IntegerField(default=0)
    message = models.CharField(max_length=1000, default="")
    username = models.CharField(max_length=100, default="")
    bookdate = models.CharField(max_length=15, default="")
    booktime = models.CharField(max_length=15, default="")

    def __str__(self):
        return self.username
    

# -------------- Assistant -------------------------------

class assistant(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    Ass_id = models.AutoField(primary_key=True)
    assname = models.CharField(max_length=100, default="")
    assfullname = models.CharField(max_length=100, default="")
    assemail = models.EmailField()
    assage = models.IntegerField()
    assdate_of_birth = models.DateField()
    homelocationlat = models.CharField(max_length=100, default="")
    homelocationlong = models.CharField(max_length=100, default="")
    assstate = models.CharField(max_length=100, default="")

    contact_number = models.CharField(max_length=15, default="")
    registerdOn = models.CharField(max_length=100, default="")
    ratings = models.IntegerField(default=0)


    def __str__(self):
        return self.assfullname
    
class serve_req(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    serve_req_id = models.AutoField(primary_key=True)
    Ass_id = models.IntegerField(default=0)

    Booking_id = models.IntegerField(default=0)

    assname = models.CharField(max_length=100, default="")
    status = models.CharField(max_length=15, default="")

    currentlocationlat = models.CharField(max_length=100, default="")
    currentlocationlong = models.CharField(max_length=100, default="")

    state = models.CharField(max_length=100, default="")
  
    serveActivedate = models.CharField(max_length=15, default="")
    serveActivetime = models.CharField(max_length=15, default="")


    def __str__(self):
        return self.assname
    
# class Driver(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # Add additional driver information fields here

# class AssistanceBooking(models.Model):
#     driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
#     # Add fields for assistance booking information (e.g., date, type, location)

# class LocationTracking(models.Model):
#     driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
#     latitude = models.DecimalField(max_digits=9, decimal_places=6)
#     longitude = models.DecimalField(max_digits=9, decimal_places=6)
#     timestamp = models.DateTimeField(auto_now_add=True)
