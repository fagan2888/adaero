import transaction

from pyramid.httpexceptions import HTTPUnauthorized, HTTPOk
from pyramid.security import (
    NO_PERMISSION_REQUIRED,
    forget,
    remember,
    Allow,
    Authenticated,
)

from logging import getLogger as get_logger
from rest_toolkit import resource

from adaero.constants import ALLOW_PASSWORDLESS_ACCESS_KEY, BUSINESS_UNIT_KEY, HOMEBASE_LOCATION_KEY
from adaero.config import get_config_value
from adaero.models.period import Period
from adaero.security import ANGULAR_2_XSRF_TOKEN_COOKIE_NAME
from adaero.views import Root


log = get_logger(__name__)


def _build_user_data_response(request, username):
    request.response.status_int = 200
    request.response.set_cookie(
        ANGULAR_2_XSRF_TOKEN_COOKIE_NAME, request.session.get_csrf_token()
    )
    unit_name = get_config_value(request.registry.settings, BUSINESS_UNIT_KEY)
    location = get_config_value(
        request.registry.settings, HOMEBASE_LOCATION_KEY
    )
    with transaction.manager:
        current_period = Period.get_current_period(request.dbsession)
    return {
        "success": True,
        "data": {
            "displayName": request.user.display_name,
            "title": request.user.position,
            "principals": request.effective_principals,
            "businessUnit": unit_name,
            "currentPhase": current_period.phase(location),
        },
    }


@resource("/api/v1/login")
class Login(Root):
    def __init__(self, request):  # pylint disable=unused-argument
        pass


@Login.POST(permission=NO_PERMISSION_REQUIRED, require_csrf=False)
def login(request):
    username = request.json_body["username"]
    password = request.json_body["password"]
    if not get_config_value(
        request.registry.settings, ALLOW_PASSWORDLESS_ACCESS_KEY
    ) and not request.ldapsource.auth_user(username, password):
        raise HTTPUnauthorized
    remember(request, username)
    return _build_user_data_response(request, username)


@resource("/api/v1/user-data")
class UserData(Root):

    __acl__ = [(Allow, Authenticated, "read")]

    def __init__(self, request):  # pylint disable=unused-argument
        pass


@UserData.GET(permission="read")
def get_user_data(request):
    username = request.authenticated_userid
    if not username:
        raise HTTPUnauthorized
    return _build_user_data_response(request, username)


@resource("/api/v1/logout")
class Logout(Root):
    def __init__(self, request):  # pylint disable=unused-argument
        pass


@Logout.POST(permission=NO_PERMISSION_REQUIRED, require_csrf=False)
def logout(request):
    headers = forget(request)
    return HTTPOk(headers=headers)
