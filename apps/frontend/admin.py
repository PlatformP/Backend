from django.contrib import admin

from .models.Candidate import Candidate
from .models.Policy import Policy
from .models.ElectionInLine import ElectionInLine
from .models.Location import Location
from .models.Election import Election
from .models.Voter import Voter
from .models.VoterFavElections import VoterFavElections
from .models.VoterCandidateMatch import VoterCandidateMatch
from .models.PoliticalParty import PoliticalParty
from .models.ZipCode import ZipCode
from .models.SurveyQuestion import SurveyQuestion
from .models.SurveyQuestionInLine import SurveyQuestionInLine


# Inlines
class PolicyInLine(admin.TabularInline):
    model = Policy


class ElectionInLine(admin.TabularInline):
    model = ElectionInLine


class Voter_FavElections_Inline(admin.TabularInline):
    model = VoterFavElections


class VoterCandidateMatchInLine(admin.TabularInline):
    model = VoterCandidateMatch


class SurveyQuestionInLine(admin.TabularInline):
    model = SurveyQuestionInLine


# models
class ElectionAdmin(admin.ModelAdmin):
    inlines = [ElectionInLine, ]
    ordering = ('-date',)
    list_display = ['name', 'type', 'location']


class LocationAdmin(admin.ModelAdmin):
    list_display = ['city', 'state']


class CandidateAdmin(admin.ModelAdmin):
    inlines = [PolicyInLine, SurveyQuestionInLine]
    list_display = ['user', '__str__', 'bio', 'popularity', 'supporters']


class VoterAdmin(admin.ModelAdmin):
    inlines = (Voter_FavElections_Inline, VoterCandidateMatchInLine, SurveyQuestionInLine)
    list_display = ['user', '__str__']


class Political_PartyAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo']


class ZipCodeAdmin(admin.ModelAdmin):
    list_display = ['zipcode', 'place_name', 'state_name']
    readonly_fields = ['country_code', 'place_name', 'state_name', 'state_name', 'state_code',
                       'state_key', 'county_name', 'county_code']


class SurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ['__str__']


admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Election, ElectionAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Voter, VoterAdmin)
admin.site.register(PoliticalParty, Political_PartyAdmin)
admin.site.register(ZipCode, ZipCodeAdmin)
admin.site.register(SurveyQuestion, SurveyQuestionAdmin)
