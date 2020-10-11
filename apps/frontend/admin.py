from django.contrib import admin

from .models.Candidate import Candidate
from .models.Policy import Policy
from .models.Election_InLine import Election_InLine
from .models.Location import Location
from .models.Election import Election
from .models.Voter import Voter
from .models.Voter_FavElections import Voter_FavElections


# Inlines
class PolicyInLine(admin.TabularInline):
    model = Policy


class ElectionInLine(admin.TabularInline):
    model = Election_InLine


class Voter_FavElections_Inline(admin.TabularInline):
    model = Voter_FavElections


# models
class ElectionAdmin(admin.ModelAdmin):
    inlines = [ElectionInLine, ]
    ordering = ('-date',)
    list_display = ['name', 'status']


class LocationAdmin(admin.ModelAdmin):
    list_display = ['city', 'state']


class CandidateAdmin(admin.ModelAdmin):
    inlines = [PolicyInLine, ]
    list_display = ['user', 'bio', 'is_verified']


class VoterAdmin(admin.ModelAdmin):
    inlines = [Voter_FavElections_Inline, ]
    list_display = ['user']


admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Election, ElectionAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Voter, VoterAdmin)
