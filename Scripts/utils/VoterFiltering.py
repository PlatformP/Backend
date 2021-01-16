from apps.frontend.models.Voter import Voter
from pandas import DataFrame

from Backend.settings import US_GEO_CONFIG
from Scripts.HelperMethods import get_key_from_state


def get_voter_ids_from_city(place, city=False, county=False, state=False):
    df_voter = DataFrame.from_records(Voter.objects.values('id', 'zipcode__zipcode'))
    df_voter.rename(columns={'zipcode__zipcode': 'zipcode'}, inplace=True)

    def get_city_from_zipcode(zipcode):
        if city:
            name = US_GEO_CONFIG.query_postal_code(zipcode).place_name
        elif county:
            name = US_GEO_CONFIG.query_postal_code(zipcode).county_name
        elif state:
            name = get_key_from_state(US_GEO_CONFIG.query_postal_code(zipcode).state_code)
        return name

    df_voter['place'] = df_voter['zipcode'].map(get_city_from_zipcode)
    df_voter.set_index('place', inplace=True)

    return set(df_voter.loc[place, 'id'])