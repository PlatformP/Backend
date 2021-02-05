from drf_yasg import openapi

response_get_survey = {
    '200': openapi.Response(
        description='/get_survey',
        examples={
            'application/json': {
                0: {
                    'id': 'int',
                    'name': 'String',
                    'survey_type': 'int (0-4)(general, city, county, state, national)',
                    'questions': [{0: {
                        'answer': 'null or {answer: int}',
                        'id': 'int',
                        'question': 'String'
                    }}]
                }
            }
        }
    )
}

submit_answer_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'survey_id': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER),
                                    description='[int]'),
        'question_id': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER),
                                      description='[int]'),
        'answer': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER),
                                 description='[int]'),
    }
)

submit_answer_response = {
    '201': openapi.Response(
        description='empty reponse',
        examples={
            'application/json': {}
        }
    )
}
