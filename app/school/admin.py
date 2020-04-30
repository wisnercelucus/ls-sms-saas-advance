from django.contrib import admin

from school.models import Pupil

@admin.register(Pupil)
class PupilAdmin(admin.ModelAdmin):
    pass
