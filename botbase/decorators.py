"""
权限验证装饰器
"""
from functools import wraps
from flask_login import current_user

from flask import abort

from botbase.models import Project

# def permission_required(permission_name):
#     def decorator(func):
#         @wraps(func)
#         def decorated_function(*args, **kwargs):
#             if not current_user.can(permission_name):
#                 abort(403)
#             return func(*args, **kwargs)
#     return decorator

# def admin_required(func):
#     return permission_required('Administer')(func)

def permission_required(permission_name):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission_name):
                abort(403)
            return func(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(func):
    return permission_required('ADMINISTER')(func)

def confirm_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.confirmed:
            message = Markup(
                'Please confirm your account first.'
                'Not receive the email?'
                '<a class="alert-link" href="%s">Resend Confirm Email</a>' %
                url_for('auth.resend_confirm_email'))
            flash(message, 'warning')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)
    return decorated_function

def only_onwer_can(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        print(kwargs)
        if not Project().match(project_id=kwargs.get("project_id"), user_id=current_user.id):
            abort(403)
        
        return func(*args, **kwargs)
    return decorated_function