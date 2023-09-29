from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # path("about/", views.about, name="AboutUs"),

    path('booknow/', views.booknow, name='booknow'),

    
    path('profile/', views.user_profile, name='user_profile'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),


    path("assindex/", views.assindex, name="assindex"),
    path("assmap/", views.plot_active_req_on_map, name="plot_active_req_on_map"),
    path('assprofile/', views.assprofile, name='assprofile'),
    path('take_request/', views.take_request_view, name='take_request'),
    
    path('all_request/', views.assRequests, name='assRequests'),

    path('bookingreq/<int:booking_id>/', views.booking_request, name='booking_request'),
    
    path('chat/<int:booking_id>/', views.chatingRoom, name='chatingRoom'),

    path('assregister/', views.ass_register, name='ass_register'),
    path('asslogin/', views.ass_login, name='ass_login'),
    path('asslogout/', views.ass_logout, name='ass_logout'),



    # path("business", views.business, name="Business"),
    # path("contact/", views.contact, name="ContactUs"),
    # # path("products/<int:myid>", views.productView, name="ProductView"),
    # path("products/<str:myslug>", views.productView, name="ProductView"),

]