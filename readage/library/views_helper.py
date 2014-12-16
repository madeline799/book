import json

from django.http import HttpResponse, Http404
from django.core.paginator import EmptyPage, PageNotAnInteger

from library.models import PermException, MyUser


def FC(prototype, *args):
    """Fake a object-like variable for templates based on the prototype."""
    return dict(zip(prototype, args))


def render_JSON_OK(data):
    """Shortcut. Render an OK message with data in JSON.

    Argument:
    data -- dict, data to be sent
    """
    data['status'] = 'OK'
    return HttpResponse(json.dumps(data))


def render_JSON_Error(message, data={}):
    """Shortcut. Render an Error message in JSON.

    Argument:
    message -- str, human-readable (but English) error message
    data    -- detailed error data to be sent
    """
    res = {
        'status': 'Error',
        'err': message,
        }
    res.update(data)
    return HttpResponse(json.dumps(res))


def get_page(paginator, page):
    """Shortcut. Get certain page from paginator.

    Argument
    paginator -- paginator to get page from
    page      -- string from GET parameter

    Catch format errors and fall back gracefully.
    """
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)


def POST_required(*field_list):
    """View decorator. Check HTTP method and certain field."""
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.method != 'POST':
                return render_JSON_Error('Only POST method is accepted.')
            for field in field_list:
                if field not in request.POST:
                    return render_JSON_Error('POST data not found: {}.'.format(
                        field,
                        ))
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


def login_required_JSON(admin_type=None):
    """View decorator. Check logged in user."""
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated():
                return render_JSON_Error('Not logged in.')
            try:
                request.user.myuser
            except MyUser.DoesNotExist as err:
                return render_JSON_Error('Root not allowed.')
            if admin_type is not None and \
                    request.user.myuser.get_admin_type() != admin_type:
                return render_JSON_Error('Only {} can access.'.format(
                    admin_type,
                    ))
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


def catch_404_JSON(func):
    """View decorator. Convert Http404 to JSON output."""
    def wrapper(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except Http404 as err:
            return render_JSON_Error('404 raised.', {
                'message': err.args[0],
                })
    return wrapper


def catch_PermException_JSON(func):
    """View decorator. Convert PermException to JSON output."""
    def wrapper(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except PermException as err:
            return render_JSON_Error('Permission denied.', {
                'message': err.args[0],
                })
    return wrapper


def catch_Assertion_JSON(func):
    """View decorator. Convert AssertionError to JSON output."""
    def wrapper(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except AssertionError as err:
            return render_JSON_Error(err.args[0])
    return wrapper
