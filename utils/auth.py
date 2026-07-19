"""
Authentication Utilities
Handles user authentication and session management
"""

from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    """
    Decorator to require login for protected routes
    Redirects to login page if user is not authenticated
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def init_auth(app):
    """
    Initialize authentication settings for Flask app
    """
    # Set session configuration
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    
    # Add context processor to make user info available in templates
    @app.context_processor
    def inject_user():
        return dict(
            current_user_id=session.get('user_id'),
            current_user_email=session.get('user_email')
        )

def is_authenticated():
    """
    Check if current user is authenticated
    Returns True if user is logged in, False otherwise
    """
    return 'user_id' in session

def get_current_user_id():
    """
    Get current user ID from session
    Returns user ID if authenticated, None otherwise
    """
    return session.get('user_id')

def get_current_user_email():
    """
    Get current user email from session
    Returns email if authenticated, None otherwise
    """
    return session.get('user_email')