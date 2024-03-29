from django.contrib import admin
from django.contrib.auth.admin import Group

from .models import (MechTaskAlgorithm, MechTaskStudentSample,
                     MechTaskSurveyEstimate, MechTaskSurveyResponse,
                     MechTaskUserGroup, MechTaskCustomModel, MechTaskCustomModelSample)


class MechTaskAlgorithmAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'average_error')


class MechTaskStudentSampleAdmin(admin.ModelAdmin):
    pass


class MechTaskSurveyEstimateAdmin(admin.ModelAdmin):
    pass


class MechTaskSurveyResponseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user_group'
    )


class MechTaskUserGroupAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'use_model_estimates_only',
        'use_freely',
        'only_10_percentile_change',
        'can_change_attributes',
        'can_change_algorithm',
        'has_deception',
        'uses_proposed_payment_scheme',
        'in_production'
    )


class MechTaskCustomModelAdmin(admin.ModelAdmin):
    pass


class MechTaskCustomModelSampleAdmin(admin.ModelAdmin):
    pass


# Remove the admin groups listing from admin
admin.site.unregister(Group)

# Register all the models
admin.site.site_title = 'Survey Admin'
admin.site.register(MechTaskAlgorithm, MechTaskAlgorithmAdmin)
admin.site.register(MechTaskStudentSample, MechTaskStudentSampleAdmin)
admin.site.register(MechTaskSurveyEstimate, MechTaskSurveyEstimateAdmin)
admin.site.register(MechTaskSurveyResponse, MechTaskSurveyResponseAdmin)
admin.site.register(MechTaskUserGroup, MechTaskUserGroupAdmin)
admin.site.register(MechTaskCustomModel, MechTaskCustomModelAdmin)
admin.site.register(MechTaskCustomModelSample, MechTaskCustomModelSampleAdmin)
