from drf_yasg import openapi

response_candidate = {
    '200': openapi.Response(
        description='showing the candidate',
        examples={
            'application/json': {
                'id': 'int',
                'user': {
                    'first_name': 'String',
                    'last_name': 'String',
                },
                'political_party': {
                    'party': 'String',
                    'party_color': 'string'
                },
                'profile_picture': 'String (url)',
                'bio': 'String',
                'popularity': 'double',
                'supporters': 'int',
                'protesters': 'int',
                'protestor_supporter_json': {
                    'date': [],
                    'protesters': [],
                    'supporters': []
                },
                'social_media_json': {},
                'voter_match': {
                    'match_pct': 'double',
                    'favorite': 'boolean',
                    'support': 'boolean',
                    'protest': 'boolean'
                },
                'election': {
                    'id': 'int',
                    'name': 'String',
                    'type': 'int'
                }
            }
        }
    )
}
