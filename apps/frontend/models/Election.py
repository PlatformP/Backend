from django.db import models

from apps.frontend.models.ElectionInLine import ElectionInLine
from apps.frontend.models.Candidate import Candidate
from apps.frontend.models.Location import Location

from pandas import DataFrame

class Election(models.Model):
    STATUS_CHOICE_FIELD = [
        (1, 'Future'),
        (0, 'Past')
    ]

    ELECTION_TYPE_CHOICES = [
        (0, 'City'),
        (1, 'County'),
        (2, 'State'),
        (3, 'National')
    ]

    name = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(max_length=250)
    location = models.ForeignKey('frontend.Location', on_delete=models.SET_NULL, blank=False, null=True)
    type = models.SmallIntegerField(default=0, choices=ELECTION_TYPE_CHOICES)
    status = models.SmallIntegerField(default=1, choices=STATUS_CHOICE_FIELD)

    class Meta:
        verbose_name = 'Election'
        verbose_name_plural = 'Elections'

    def __str__(self):
        return self.name

    def set_status_past(self):
        self.status = 0
        self.save()

    def set_type(self, type):
        self.type = type
        self.save()

    @staticmethod
    def get_df(id, user):
        candidate_ids = set(ElectionInLine.objects.filter(election__pk=id)
                            .values_list('candidate_id', flat=True))
        df_candidates = Candidate.get_multiple_df(candidate_ids, user)

        df_election = DataFrame.from_records(Election.objects.filter(pk=id).values())
        df_location = DataFrame.from_records(Location.objects.filter(id=df_election['location_id']).values())
        df_location.set_index('id', inplace=True)

        df_election['location_id'] = df_election['location_id'].map(df_location.to_dict(orient='index'))

        df_election.rename(columns={'location_id': 'location'}, inplace=True)
        df_candidates.set_index('id', inplace=True, drop=False)

        def candidate_in_election(x):
            return df_candidates.loc[Election.objects.get(pk=x).
                electioninline_set.values_list('candidate_id', flat=True)].to_dict(orient='records')

        df_election['candidates'] = df_election['id'].map(candidate_in_election)

        return df_election