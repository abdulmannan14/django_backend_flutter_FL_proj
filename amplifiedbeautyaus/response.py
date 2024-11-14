from django.conf import settings
from django.db import connection
from django.http import JsonResponse
from rest_framework.response import Response


class AmplifiedBeautyResponse(JsonResponse):
    def __init__(self, data, **kwargs):
        if settings.DEBUG:
            data['debug'] = {
                'num_queries': len(connection.queries)
            }
        super().__init__(data, **kwargs)


class SuccessResponse(AmplifiedBeautyResponse):
    def __init__(self, message, data={}, **kwargs):
        super().__init__({'status': 'true', 'message': message, 'data': data, **kwargs})


class CommonResponse(Response):
    def __init__(self,  success: bool = True, **kwargs):
        kwargs['data'] = {
            'success': success, 'message': kwargs.pop('message', ''), 'data': kwargs.pop('data', None)
        }

        super().__init__(**kwargs)
