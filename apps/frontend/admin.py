from django.contrib import admin

from .models.Election import Election
from .models.Candidate import Candidate
from .models.Policy import Policy
from .models.ElectionInLine import ElectionInLine
from .models.Location import Location
from .models.Voter import Voter
from .models.VoterFavElections import VoterFavElections
from .models.VoterCandidateMatch import VoterCandidateMatch
from .models.PoliticalParty import PoliticalParty
from .models.ZipCode import ZipCode
from .models.Survey import Survey
from .models.SurveyQuestion import SurveyQuestion
from .models.SurveyQuestionAnswers import SurveyQuestionAnswers


# Inlines
class PolicyInLine(admin.TabularInline):
    model = Policy


class ElectionInLine(admin.TabularInline):
    model = ElectionInLine


class Voter_FavElections_Inline(admin.TabularInline):
    model = VoterFavElections


class VoterCandidateMatchInLine(admin.TabularInline):
    model = VoterCandidateMatch


class SurveyQuestionAnswersInLine(admin.TabularInline):
    model = SurveyQuestionAnswers


class SurveyQuestionInLine(admin.TabularInline):
    model = SurveyQuestion


# models
class ElectionAdmin(admin.ModelAdmin):
    inlines = [ElectionInLine, ]
    ordering = ('-date',)
    list_display = ['name', 'type', 'location']


class LocationAdmin(admin.ModelAdmin):
    list_display = ['city', 'state']


class CandidateAdmin(admin.ModelAdmin):
    inlines = [PolicyInLine, SurveyQuestionAnswersInLine]
    list_display = ['user', '__str__', 'bio', 'popularity', 'supporters', 'protesters']


class VoterAdmin(admin.ModelAdmin):
    inlines = (Voter_FavElections_Inline, VoterCandidateMatchInLine, SurveyQuestionAnswersInLine)
    list_display = ['user', '__str__']


class Political_PartyAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo']


class ZipCodeAdmin(admin.ModelAdmin):
    list_display = ['zipcode', 'place_name', 'state_name']
    readonly_fields = ['country_code', 'place_name', 'state_name', 'state_name', 'state_code',
                       'state_key', 'county_name', 'county_code']


class SurveyAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    inlines = [SurveyQuestionInLine]


admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Election, ElectionAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Voter, VoterAdmin)
admin.site.register(PoliticalParty, Political_PartyAdmin)
admin.site.register(ZipCode, ZipCodeAdmin)
admin.site.register(Survey, SurveyAdmin)
