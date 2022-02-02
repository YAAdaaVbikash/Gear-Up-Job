from django.contrib import admin
from accounts.models import Seeker,Company,Rating


# Register your models here.
admin.site.register(Seeker)
admin.site.register(Company)
admin.site.register(Rating)
