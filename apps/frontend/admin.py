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
from .models.testinline import testinline

# Inlines
class testinline(admin.TabularInline):
    model = testinline


class PolicyInLine(admin.TabularInline):
    model = Policy


class ElectionInLine(admin.TabularInline):
    model = ElectionInLine


class Voter_FavElections_Inline(admin.TabularInline):
    model = VoterFavElections


class VoterCandidateMatchInLine(admin.TabularInline):
    model = VoterCandidateMatch


# models
class ElectionAdmin(admin.ModelAdmin):
    inlines = [ElectionInLine, ]
    ordering = ('-date',)
    list_display = ['name', 'status']


class LocationAdmin(admin.ModelAdmin):
    list_display = ['city', 'state']


class CandidateAdmin(admin.ModelAdmin):
    inlines = [PolicyInLine, ]
    list_display = ['user', 'bio']


class VoterAdmin(admin.ModelAdmin):
    inlines = (Voter_FavElections_Inline, VoterCandidateMatchInLine, testinline)
    list_display = ['user']


class Political_PartyAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo']


admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Election, ElectionAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Voter, VoterAdmin)
admin.site.register(PoliticalParty, Political_PartyAdmin)
