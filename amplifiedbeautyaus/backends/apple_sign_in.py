import jwt
import requests
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from social_core.backends.oauth import BaseOAuth2
from social_core.utils import handle_http_errors


class AppleOAuth2(BaseOAuth2):
    """apple authentication backend"""

    name = 'apple'
    ACCESS_TOKEN_URL = 'https://appleid.apple.com/auth/token'
    SCOPE_SEPARATOR = ','
    ID_KEY = 'uid'

    @handle_http_errors
    def do_auth(self, access_token, *args, **kwargs):
        """
        Finish the auth process once the access_token was retrieved
        Get the email from ID token received from apple
        """
        response_data = {}
        client_id, client_secret = self.get_key_and_secret()
        print(client_id)
        print(client_secret)

        headers = {'content-type': "application/x-www-form-urlencoded"}
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': access_token,
            'grant_type': 'authorization_code',
            'redirect_uri': 'https://example-app.com/redirect'
        }
        print(data)

        res = requests.post(AppleOAuth2.ACCESS_TOKEN_URL, data=data, headers=headers)
        response_dict = res.json()
        id_token = response_dict.get('id_token', None)

        if id_token:
            decoded = jwt.decode(id_token, '', verify=False)
            print(str(decoded))
            response_data.update({"fullName": decoded['fullName']}) if 'fullName' in decoded else None
            response_data.update({'email': decoded['email']}) if 'email' in decoded else None
            response_data.update({'uid': decoded['sub']}) if 'sub' in decoded else None
        response = kwargs.get('response') or {}
        response.update(response_data)
        response.update({'access_token': access_token}) if 'access_token' not in response else None

        kwargs.update({'response': response, 'backend': self})
        return response_data

    def get_key_and_secret(self):
        headers = {
            'kid': settings.SOCIAL_AUTH_APPLE_KEY_ID
        }

        payload = {
            'iss': settings.SOCIAL_AUTH_APPLE_TEAM_ID,
            'iat': timezone.now(),
            'exp': timezone.now() + timedelta(days=180),
            'aud': 'https://appleid.apple.com',
            'sub': settings.SOCIAL_AUTH_APPLE_CLIENT_KEY,
        }

        client_secret = jwt.encode(
            payload,
            settings.SOCIAL_AUTH_APPLE_PRIVATE_KEY,
            algorithm='ES256',
            headers=headers
        ).decode("utf-8")

        return settings.SOCIAL_AUTH_APPLE_CLIENT_KEY, client_secret
