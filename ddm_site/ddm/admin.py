from django.contrib import admin

from .models import Project, DataEntry, DataEntryPair

admin.site.register(Project)
admin.site.register(DataEntry)
admin.site.register(DataEntryPair)
