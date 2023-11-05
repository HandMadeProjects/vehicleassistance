from django.contrib import admin

# Register your models here.

from .models import UserProfile, bookingreq, assistant, serve_req, personalchat, assreviews, ContactMessage

# Register your models here.

admin.site.register(ContactMessage)

# ------------------------ userg  

admin.site.register(UserProfile)
admin.site.register(bookingreq)

# ------------------------ assistant 

admin.site.register(assistant)
admin.site.register(serve_req)

admin.site.register(personalchat)
admin.site.register(assreviews)