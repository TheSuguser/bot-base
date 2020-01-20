"""
权限验证装饰器
"""
from functools import wraps
from flask_login import current_user

from flask import abort

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
