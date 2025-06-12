from functools import wraps
from flask import session, redirect, url_for, flash, abort

def roles_required(*required_roles):
    """
    Decorator to protect routes by checking if the logged-in user
    has at least one of the required roles.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            roles = session.get('roles', [])
            print("DEBUG: User roles:", roles)
            print("DEBUG: Required roles:", required_roles)
            print(f"DEBUG roles_required: roles={roles}, required_roles={required_roles}")

            
            if not roles:
                flash("You must be logged in to access this page.", "warning")
                return redirect(url_for('login'))
            
            # Check if any required role matches user roles
            if not any(role in roles for role in required_roles):
                abort(403)# Forbidden
            return f(*args, **kwargs)
        return decorated_function
    return decorator
