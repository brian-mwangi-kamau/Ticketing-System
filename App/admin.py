from django.contrib import admin
from .models import CustomUser, Ticket, Comment, StaffInfo

admin.site.register(CustomUser)
admin.site.register(Ticket)
admin.site.register(Comment)
admin.site.register(StaffInfo)