from drf_yasg import openapi

response_elections = {
    "200": openapi.Response(
        description='/ballot',
        examples={
            "application/json": {
                0: {
                    'id': 'int',
                    'candidates': [{0: {
                        'id': 'int',
                        'political_party': {
                            'party': 'String',
                            'party_color': 'String'},
                        'popularity': 'int',
                        'profile_picture': 'String (url)',
                        'protesters': 'int',
                        'supporters': 'int',
                        'user': {
                            'first_name': 'String',
                            'last_name': 'String'},
                        'voter_match': {
                            'match_pct': 'int',
                            'favorite': 'boolean',
                            'support': 'boolean',
                            'protest': 'boolean'},
                    }}],
                    'date': 'int (epoch time)',
                    'description': 'String',
                    'favorite': 'boolean',
                    'location': {
                        'city': 'String',
                        'county': 'String',
                        'state': 'int'},
                    'name': 'String',
                    'status': 'int',
                    'type': 'int',
                }
            }
        }
    )
}

response_get_profile = {
    '200':  openapi.Response(
        description='/get_profile',
        examples={
            'application/json': {
                0: {
                    'dob': 'int (epoch time)',
                    'first_name': 'string',
                    'last_name': 'string',
                    'gender': 'int (0-2) (male, female, other)',
                    'id': 'int',
                    'zip_code': 'int'
                }
            }
        }
    )
}
