from django.contrib import admin

# Register your models here.

from .models import UserProfile, bookingreq, assistant, serve_req, personalchat

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(bookingreq)


admin.site.register(assistant)
admin.site.register(serve_req)

admin.site.register(personalchat)