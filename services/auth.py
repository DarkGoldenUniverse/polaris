from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.core.cache import cache
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication

from services.crypto import hash_token, create_token_string


def key_name(user_id: str, token: str) -> str:
    auth_token_hash_algorithm = getattr(settings, "AUTH_TOKEN_HASH_ALGORITHM", "sha512")
    return f"{user_id}_session_{hash_token(auth_token_hash_algorithm, token)}"


class CacheTokenAuthentication(TokenAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = "Token"
    model = get_user_model()

    # def get_model(self):
    #     if self.model is not None:
    #         return self.model
    #     from rest_framework.authtoken.models import Token
    #     return Token
    #
    # """
    # A custom token model may be used, but must have the following properties.
    #
    # * key -- The string identifying the token
    # * user -- The user to which the token belongs
    # """
    #
    # def authenticate(self, request):
    #     auth = get_authorization_header(request).split()
    #
    #     if not auth or auth[0].lower() != self.keyword.lower().encode():
    #         return None
    #
    #     if len(auth) == 1:
    #         msg = _('Invalid token header. No credentials provided.')
    #         raise exceptions.AuthenticationFailed(msg)
    #     elif len(auth) > 2:
    #         msg = _('Invalid token header. Token string should not contain spaces.')
    #         raise exceptions.AuthenticationFailed(msg)
    #
    #     try:
    #         token = auth[1].decode()
    #     except UnicodeError:
    #         msg = _('Invalid token header. Token string should not contain invalid characters.')
    #         raise exceptions.AuthenticationFailed(msg)
    #
    #     return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        model = self.get_model()
        try:
            key = cache.keys(key_name("*", token))
            if len(key) != 1:
                raise exceptions.AuthenticationFailed(_("Invalid token."))

            session_key = cache.get(key[0])
            session_hash = cache.get(f"django.contrib.sessions.cache{session_key}")
            user = model.objects.get(id=session_hash["user_id"])
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_("Invalid token."))

        if not user.is_active:
            raise exceptions.AuthenticationFailed(_("User inactive or deleted."))

        return user, None

    # def authenticate_header(self, request):
    #     return self.keyword


class CacheSession:
    def __init__(self):
        self.current_time = timezone.now()
        self.current_timestamp = int(self.current_time.timestamp())
        self.session_key_prefix = "django.contrib.sessions.cache"

        self.auth_token_ttl = getattr(settings, "AUTH_TOKEN_TTL", 3600)
        self.auth_token_character_length = getattr(settings, "AUTH_TOKEN_CHARACTER_LENGTH", 32)

    def add(self, request, user) -> str:
        token = self._get_new_token()

        session_data = {
            "user_id": user.id,
            "user_agent": request.META.get("HTTP_USER_AGENT", ""),
            "current_time": self.current_timestamp,
            "expire_time": self.current_timestamp + self.auth_token_ttl,
        }

        login(request, user)

        request.session.update(session_data)
        cache.set(
            key_name(user.id, token), request.session.session_key, timeout=self.auth_token_ttl
        )

        return token

    def invalidate_all(self, user_id, session_key=None):
        # Get list of active user sessions
        session_keys = cache.keys(f"{user_id}_session_*")

        # If session ID present system should invalidate all session except this session ID
        current_session_key = f"{self.session_key_prefix}{session_key}"

        # Delete user sessions from native session list
        for key in session_keys:
            if key == current_session_key:
                continue

            # Read value from additional redis list
            value = cache.get(key)
            # Delete session from native redis list
            cache.delete(value)
            # Delete session from additional redis list
            cache.delete(key)

    def _get_new_token(self):
        while True:
            token = create_token_string(self.auth_token_character_length)
            if not cache.keys(key_name("*", token)):
                return token
