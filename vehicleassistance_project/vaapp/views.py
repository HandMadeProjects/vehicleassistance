from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile, bookingreq, assistant, serve_req, personalchat, assreviews, ContactMessage
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib import messages

import folium
import requests

from datetime import datetime

# contact us
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse

# Create your views here.

def home(request):
    # return HttpResponse('Prakriti    |      community index Page')
    return render(request,'user/index.html')

def about(request):
    # return HttpResponse('Prakriti    |      community index Page')
    return render(request,'user/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_text = request.POST.get('message')

        # Create and save a ContactMessage instance
        contact_message = ContactMessage(name=name, email=email, message=message_text)
        contact_message.save()

        '''send_email():
            # # Send an email to your contact address
            # subject = f"Message from {name}"
            # message_body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
            # from_email = settings.DEFAULT_FROM_EMAIL
            # recipient_list = [settings.CONTACT_EMAIL_ADDRESS]  # Replace with your contact email address

            # try:
            #     send_mail(subject, message_body, from_email, recipient_list, fail_silently=False)
            #     return HttpResponse("Thank you for contacting us! We will get back to you shortly.")
            # except Exception as e:
            #     return HttpResponse("An error occurred while sending your message. Please try again later.")
        '''


    # return HttpResponse('Prakriti    |      community index Page')
    import folium

    currentSpot = [19.0236, 72.8499]

    # Create a map centered on the current spot location
    m = folium.Map(location=currentSpot, zoom_start=15)

    # Add a circle around the current spot
    folium.Circle(location=currentSpot, radius=1000, color='blue', fill=True, fill_color='blue').add_to(m)

    # Add a red marker for the current spot
    folium.Marker(currentSpot, icon=folium.Icon(color='red')).add_to(m)

    # Convert the map to HTML and pass it to the template
    map_html = m._repr_html_()
    return render(request, 'user/contact.html', {"map_html": map_html})


# -------------- USER -------------------------------
def bookreqSave(U_id, username, locationlat, locationlong, message, state, status):
    current_date = datetime.now().date()
    current_time = datetime.now()
    current_time = current_time.strftime("%H:%M:%S")
    print(current_time)

    bookingreqDetails = bookingreq(
        U_id=U_id,
        username=username,

        locationlat=locationlat,
        locationlong=locationlong,

        state=state,
        status=status,

        message=message,

        bookdate=current_date,
        booktime=current_time,
    )
    bookingreqDetails.save()

@login_required
def booknow(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        user_profile = UserProfile.objects.filter(username=username).first()

        if user_profile:
            U_id = user_profile.U_id
        else:
            U_id = 0

        locationlat = request.POST.get('locationlat')
        locationlong = request.POST.get('locationlong')

        state = request.POST.get('state')
        state = state.lower()

        status = "new"

        message = request.POST.get('message')

        bookreqSave(U_id, username, locationlat, locationlong, message, state, status)
        return redirect('booknow')
        
    return render(request,'user/booknow.html')

@login_required
def user_profile(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(username=request.user)
        return render(request, 'user/profile.html', {'user_profile': user_profile})
    else:
        return redirect('login')

# -------------- Assistant -------------------------------
# @login_required
def assindex(request):
    logged_in_username = request.user.username

    ass_details = assistant.objects.filter(assname=logged_in_username).first()

    logged_in_username = request.user.username
    ass_details = assistant.objects.filter(assname=logged_in_username).first()

    completedRequest = bookingreq.objects.filter(assistedbyAss_id=ass_details.Ass_id, status="done")

    posReview = assreviews.objects.filter(Ass_id=ass_details.Ass_id, sentiment=0)
    negReview = assreviews.objects.filter(Ass_id=ass_details.Ass_id, sentiment=1)
    neuReview = assreviews.objects.filter(Ass_id=ass_details.Ass_id, sentiment=2)


    parse = { 
        'ass_details' : ass_details, 
        'completedRequest' : len(completedRequest),
        'posReview' : len(posReview),
        'negReview' : len(negReview),
        'neuReview' : len(neuReview),

        }
    return render(request,'assistant/assindex.html', parse)

# Labels: 0 -> Negative; 1 -> Neutral; 2 -> Positive

def sentimentOnReply(post):
    API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
        
    output = query({
        "inputs": post,
    })
    # print(output)

    # Iterate through the data list
    for predictions in output:
        for prediction in predictions:
            label = prediction['label']
            score = prediction['score']
            print(f"Label: {label}, Score: {score}")

    # Alternatively, you can return labels and scores as a list of tuples
    labels_with_scores = [(prediction['label'], prediction['score']) for predictions in output for prediction in predictions]

    # Print the list of labels with scores
    print(labels_with_scores)
    # [('LABEL_2', 0.9782516956329346), ('LABEL_1', 0.018881788477301598), ('LABEL_0', 0.0028664814308285713)]
    return labels_with_scores

# post = "I like you. I love you"
# sentimentOnReply(post)

def showreviews(request):
    logged_in_username = request.user.username
    ass_details = assistant.objects.filter(assname=logged_in_username).first()
    # print("Ass-id : " ,ass_details.Ass_id)

    request_details = assreviews.objects.filter(Ass_id=ass_details.Ass_id)
    parse = { 'reviews_details' : request_details, }

    return render(request,'assistant/reviews.html', parse)


def assRequests(request):
    logged_in_username = request.user.username
    ass_details = assistant.objects.filter(assname=logged_in_username).first()

    request_details = bookingreq.objects.filter(assistedbyAss_id=ass_details.Ass_id, status="active")
    
    return render(request,'assistant/allrequest.html', {'request_details': request_details})


def statusChangeFun(new_status, username, booking_id):
    # new_status = "new"  # Replace with the new value for status
    assistant_details = assistant.objects.filter(assname=username).first()

    if assistant_details:
        Ass_id = assistant_details.Ass_id

    # Use a queryset to update the specific bookingreq object
    bookingreq.objects.filter(Booking_id=booking_id).update(
        assistedbyAss_id=Ass_id,
        status=new_status
    )
    # print("done update")

def assrequestaction(request):
    # action = request.form.get('action')

    if request.method == 'POST':
        # logged_in_username = request.user.username

        username   = request.POST.get('username')
        booking_id = request.POST.get('booking_id')
        action     = request.POST.get('action')
    
        if action == 'decline':
            # print("User clicked the 'Decline' button.")
            new_status = 'new'
            statusChangeFun(new_status, username, booking_id)

        elif action == 'done':
            # print("User clicked the 'Done' button.")
            new_status = 'done'
            statusChangeFun(new_status, username, booking_id)

        # return redirect('booking_request', booking_id=booking_id)        
        return redirect('assRequests')        

        
    
    # return "Button clicked."

@login_required
def assprofile(request):
    if request.user.is_authenticated:
        user_profile = assistant.objects.get(assname=request.user)
        return render(request, 'assistant/assprofile.html', {'user_profile': user_profile})
    else:
        return redirect('login')


def booking_request(request, booking_id):
    # Your view logic here
    print("booking_id: ", booking_id)
    request_details = bookingreq.objects.filter(Booking_id=booking_id).first()

    return render(request, 'assistant/booking_request.html', {'request_details': request_details})

def take_request_view(request):
    if request.method == 'POST':
        logged_in_username = request.user.username

        booking_id = request.POST.get('booking_id')
        print(f"Booking ID: {booking_id}")

        activateReqSave(booking_id, logged_in_username)

    return redirect('assRequests')


def activateReqSave(booking_id_to_update, logged_in_username):
    new_status = "active"  # Replace with the new value for status
    assistant_details = assistant.objects.filter(assname=logged_in_username).first()

    if assistant_details:
        Ass_id = assistant_details.Ass_id

    # Use a queryset to update the specific bookingreq object
    bookingreq.objects.filter(Booking_id=booking_id_to_update).update(
        assistedbyAss_id=Ass_id,
        status=new_status
    )
    print("done update")

# --- Chat -----------------

def chatingRoom(request, booking_id):
    if request.method == 'POST':
        assname = request.POST.get('assname')
        asspassword = request.POST.get('asspassword')
        confirm_password = request.POST.get('confirm_password')
        


    # print("booking_id: ", booking_id)
    chat_details = personalchat.objects.filter(Booking_id=booking_id)
    request_details = bookingreq.objects.filter(Booking_id=booking_id).first()

    parse = {'chat_details': chat_details, 'request_details' : request_details}

    return render(request, 'assistant/chating.html', parse) 
# --------------------

# Define a list of coordinates and corresponding links
# points = [
#     {
#         'coord': [19.016439, 72.829422],
#         'link': '/bookingreq/1',
#     },
#     {
#         'coord': [19.012439, 72.829424],
#         'link': '/bookingreq/2',
#     },
#     {
#         'coord': [19.066439, 72.829422],
#         'link': '/bookingreq/3',
#     },
#     {
#         'coord': [19.016439, 72.929422],
#         'link': '/bookingreq/4',
#     },
# ]

# Define the current spot location
# currentSpot = [19.018438, 72.829122]

@login_required
def plot_active_req_on_map(request):
    logged_in_username = request.user.username

    # Filter assistant objects based on the logged-in user's username
    assistant_details = assistant.objects.filter(assname=logged_in_username).first()

    # Check if an assistant with the logged-in username exists
    if assistant_details:
        # assname = assistant_details.assname
        assstate = assistant_details.assstate
        # Extract the assistant's location
        currentSpot = [float(assistant_details.homelocationlat), float(assistant_details.homelocationlong)]
    else:
        # Handle the case where no assistant with the logged-in username is found
        # assname = "Not Found"
        assstate = "maharashtra"
        currentSpot = [19.018438, 72.829122]


    # return render(request, 'assistant_details.html', {'assname': assname, 'assstate': assstate})

    filtered_bookings = bookingreq.objects.filter(status='new', state=assstate)

    points = [
        {
            'coord': [float(booking.locationlat), float(booking.locationlong)],
            'link': f'/bookingreq/{booking.Booking_id}',
        }
        for booking in filtered_bookings
    ]

    # for point in points:
        # print(f"Coordinates: {point['coord']}, Link: {point['link']}")




    # Create a map centered on the current spot location
    m = folium.Map(location=currentSpot, zoom_start=15)

    # Add a circle around the current spot
    folium.Circle(location=currentSpot, radius=1000, color='blue', fill=True, fill_color='blue').add_to(m)

    # Add a red marker for the current spot
    folium.Marker(currentSpot, icon=folium.Icon(color='red')).add_to(m)

    # Add markers for each coordinate in the list
    for point in points:
        coord = point['coord']
        link = point['link']
        folium.Marker(coord, popup=f'<a href="{link}" target="_blank" >See Details</a>').add_to(m)

    # Convert the map to HTML and pass it to the template
    map_html = m._repr_html_()
    return render(request, 'assistant/map.html', {"map_html":map_html})

    # ------------------------


    # Get the latitude and longitude from the form
    # lat = 19.016439
    # lon = 72.829422

    # # [[19.016439, 72.829422], [19.016439, 72.829424],[19.066439, 72.829422],[19.016439, 72.929422]]

    # # Create a map centered on the provided coordinates
    # m = folium.Map(location=[lat, lon], zoom_start=13)

    # # Add a marker at the provided coordinates
    # folium.Marker([lat, lon]).add_to(m)

    # # Convert the map to HTML and pass it to the template
    # map_html = m._repr_html_()
    # return render(request, 'assistant/map.html', {"map_html":map_html})


def serve_req_Save(U_id, username, locationlat, locationlong, message, state, status):
    current_date = datetime.now().date()
    current_time = datetime.now()

    bookingreqDetails = serve_req(
        U_id=U_id,
        username=username,

        locationlat=locationlat,
        locationlong=locationlong,

        state=state,
        status=status,

        message=message,

        bookdate=current_date,
        booktime=current_time,
    )
    bookingreqDetails.save()



# ======= Assistant ================================================================================
# Register , Login, Profile 


def saveAssisDetails(assname,assfullname, assemail, assage, assdate_of_birth, homelocationlat, homelocationlong, assstate, contact_number):

    current_date = datetime.now().date()

    userRegisterDetails = assistant(
        assname=assname,
        assfullname=assfullname,
        assemail=assemail,
        assage=assage,
        assdate_of_birth=assdate_of_birth,
        homelocationlat=homelocationlat,
        homelocationlong=homelocationlong,
        assstate=assstate,
        contact_number=contact_number,

        registerdOn=current_date,
        ratings = 0 # ratings : total = 5
    )
    userRegisterDetails.save()

    # Ass_id = models.AutoField(primary_key=True)
    # assname = models.CharField(max_length=100, default="")
    # assfullname = models.CharField(max_length=100, default="")
    # assemail = models.EmailField()
    # assage = models.IntegerField()
    # assdate_of_birth = models.DateField()
    # homelocationlat = models.CharField(max_length=100, default="")
    # homelocationlong = models.CharField(max_length=100, default="")
    # contact_number = models.CharField(max_length=15, default="")
    # registerdOn = models.CharField(max_length=100, default="")
    # ratings = models.IntegerField(default=0)



def ass_register(request):
    if request.method == 'POST':
        assname = request.POST.get('assname')
        asspassword = request.POST.get('asspassword')
        confirm_password = request.POST.get('confirm_password')

        # extra info:
        assfullname = request.POST.get('assfullname')
        assemail = request.POST.get('assemail')
        assage = request.POST.get('assage')
        assdate_of_birth = request.POST.get('assdate_of_birth')
        homelocationlat = request.POST.get('homelocationlat')
        homelocationlong = request.POST.get('homelocationlong')
        assstate = request.POST.get('assstate')
        contact_number = request.POST.get('phone')

        # print(assname, asspassword, confirm_password)

        if asspassword == confirm_password:
            if User.objects.filter(username=assname).exists():
                messages.error(request, 'assname already exists.')
                print("assname already exists.")
                return redirect('ass_register')
            else:
                user = User.objects.create_user(username=assname, password=asspassword)
                print("user: ", user)
                messages.success(request, 'Registration successful. You can now log in.')

                user = authenticate(username=assname, password=asspassword)
                login(request, user)
                
                # saveAssisDetails(assname, assfullname, assemail, userage, date_of_birth, locationlat, locationlong, contact_number)
                saveAssisDetails(assname,assfullname, assemail, assage, assdate_of_birth, homelocationlat, homelocationlong, assstate, contact_number)

                saveAssisDetails(assname,assfullname, assemail, assage, assdate_of_birth, homelocationlat, homelocationlong, assstate, contact_number)


                return redirect('assindex')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('assindex')
    
    return render(request, 'assistant/assregister.html')

def ass_login(request):
    if request.method == 'POST':
        assname = request.POST['assname']
        asspassword = request.POST['asspassword']
        user = authenticate(request, username=assname, password=asspassword)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('assindex')  # Redirect to the user profile page
        else:
            messages.error(request, 'Invalid login credentials. Please try again.')
    
    return render(request, 'assistant/asslogin.html')

def ass_logout(request):
    logout(request)
    return redirect('ass_login')  # Redirect to your login page or any other page after logout

# # @login_required
# def user_profile(request):
#     if request.user.is_authenticated:
#         user_profile = UserProfile.objects.get(username=request.user)
#         return render(request, 'community/profile.html', {'user_profile': user_profile})
#     else:
#         return redirect('login')

# ======= User ================================================================================
# Register , Login, Profile 

def saveUserDetails(username,fullname, useremail, userage, date_of_birth, locationlat, locationlong, contact_number):

    current_date = datetime.now().date()

    userRegisterDetails = UserProfile(
        username=username,
        fullname=fullname,
        email=useremail,
        age=userage,
        date_of_birth=date_of_birth,
        locationlat=locationlat,
        locationlong=locationlong,
        contact_number=contact_number,

        registerdOn=current_date,
    )
    userRegisterDetails.save()


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # extra info:
        fullname = request.POST.get('fullname')
        useremail = request.POST.get('email')
        userage = request.POST.get('age')
        date_of_birth = request.POST.get('birthdate')
        locationlat = request.POST.get('locationlat')
        locationlong = request.POST.get('locationlong')
        contact_number = request.POST.get('phone')

        # print(username, password, confirm_password)

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password)
                print("user: ", user)
                messages.success(request, 'Registration successful. You can now log in.')

                user = authenticate(username=username, password=password)
                login(request, user)
                
                saveUserDetails(username, fullname, useremail, userage, date_of_birth, locationlat, locationlong, contact_number)

                return redirect('user_login')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('index')
    
    return render(request, 'user/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('home')  # Redirect to the user profile page
        else:
            messages.error(request, 'Invalid login credentials. Please try again.')
    
    return render(request, 'user/login.html')

def user_logout(request):
    logout(request)
    return redirect('user_login')  # Redirect to your login page or any other page after logout

