from django.contrib import admin
from django.contrib.auth.admin import Group

from .models import (MechTaskAlgorithm, MechTaskStudentSample,
                     MechTaskSurveyEstimate, MechTaskSurveyResponse,
                     MechTaskUserGroup)


class MechTaskAlgorithmAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'average_error')


class MechTaskStudentSampleAdmin(admin.ModelAdmin):
    pass


class MechTaskSurveyEstimateAdmin(admin.ModelAdmin):
    pass


class MechTaskSurveyResponseAdmin(admin.ModelAdmin):
    pass


class MechTaskUserGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'has_deception', 'can_change_algorithm', 'can_change_attributes',
                    'uses_proposed_payment_scheme')


# Remove the admin groups listing from admin
admin.site.unregister(Group)

# Register all the models
admin.site.site_title = 'Survey Admin'
admin.site.register(MechTaskAlgorithm, MechTaskAlgorithmAdmin)
admin.site.register(MechTaskStudentSample, MechTaskStudentSampleAdmin)
admin.site.register(MechTaskSurveyEstimate, MechTaskSurveyEstimateAdmin)
admin.site.register(MechTaskSurveyResponse, MechTaskSurveyResponseAdmin)
admin.site.register(MechTaskUserGroup, MechTaskUserGroupAdmin)
