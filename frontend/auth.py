import os
import secrets
import requests
import urllib
import datetime
from flask_login import UserMixin
import hashlib
import redis
from flask import (
    redirect, 
    request, 
    url_for,
    Blueprint,
    flash,
    session
)
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user
)

# The login manager from flask-login
_login_manager = LoginManager()
@_login_manager.user_loader
def load_user(user_id):
    """Retrieves a user given the ID"""
    return get_user(user_id)

# The blueprint that holds all login/logout endpoints for OAuth2 
blueprint = Blueprint("auth_blueprint", __name__)

# The logger from app.logger
_logger = None

# The config from app.config
_config = None

# The redis db
_db = None

# The salt used for hashing
_salt = secrets.token_bytes(32)

def init_app(app):
    """
    Initiates this module with the given Flask app
    """
    global _db, _config, _login_manager, _logger
    _login_manager.init_app(app)
    _config = app.config 
    _logger = app.logger
    _db = redis.Redis(
        host=_config["REDIS_ADDR"], 
        port=_config["REDIS_PORT"], 
        db=0, 
        password=None, 
        socket_timeout=None
    )
    admin_list = app.config["ADMIN_LIST"].split(",")
    admin_list_enc = list()
    for entry in admin_list:
        user_id_hash = hashlib.pbkdf2_hmac(
            "sha256", 
            entry.strip().encode("utf-8"), 
            _salt, 
            100000
        ).hex()
        admin_list_enc.append(user_id_hash)
    app.config["ADMIN_LIST"] = admin_list_enc


def build_url(baseurl, path, args_dict):
    """Builds a URI"""
    # Returns a list in the structure of urlparse.ParseResult
    url_parts = list(urllib.parse.urlparse(baseurl))
    url_parts[2] = path
    url_parts[4] = urllib.parse.urlencode(args_dict)
    return urllib.parse.urlunparse(url_parts)


@blueprint.route("/login")
def login():
    """Redirects the user to Discord for OAuth2"""
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    _logger.debug("Preparing oauth2 URI for Discord")
    redirect_uri = url_for("auth_blueprint.login_callback", _external=True)
    state = secrets.token_hex(16)
    data = {
        "response_type": "code",
        "client_id": _config["DISCORD_CLIENT_ID"],
        "scope": "identify",
        "redirect_uri": redirect_uri,
        "state": state,
        "prompt": "none"
    }
    auth_uri = build_url(
        _config["DISCORD_API_BASE"],
        _config["DISCORD_API_AUTHORIZE"],
        data
    )
    resp = redirect(auth_uri)
    resp.set_cookie("state", value=state, max_age=500, httponly=True, samesite="Lax")
    _logger.debug("Redirecting to discord")
    return resp

@blueprint.route("/login/callback")
def login_callback():
    """Return callback for OAuth2 that finishes logging in"""
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    
    # Now get code and state for auth
    _logger.debug("Processing login callback") 
    code = request.args.get("code", None)
    state = request.args.get("state", None)
    state_verif = request.cookies.get("state", None)
    if not code or not state or not state_verif:
        _logger.warn("Rejected callback: missing params")
        flash("Error authenticating. Please try again", "error") # Missing params
        return redirect(url_for("index"))
    if state != state_verif:
        _logger.warn("Rejected callback: mismatched state", "error")
        flash("Error authenticating. Please try again") # Mismatch state
        return redirect(url_for("index"))

    # Now exchange code for token
    data = {
        "client_id": _config["DISCORD_CLIENT_ID"],
        "client_secret": _config["DISCORD_CLIENT_SECRET"],
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": url_for("auth_blueprint.login_callback", _external=True),
        "scope": "identify"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    _logger.debug("Exchanging code for token")
    r = requests.post(
        "{}{}".format(
            _config["DISCORD_API_BASE"], 
            _config["DISCORD_API_TOKEN"]
        ),
        data=data, headers=headers)

    # Now parse token
    if r.status_code != 200:
        _logger.warn(f"Failed to exchange code for token: {r.json()}")
        flash("Error authenticating. Please try again", "error")
        return redirect(url_for("index"))
    tokens = r.json()
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]
    token_type = tokens["token_type"]
    expires_in = tokens["expires_in"]

    # Now get user information
    headers = {"Authorization": f"{token_type} {access_token}"}
    r = requests.get(
        "{}{}".format(
            _config["DISCORD_API_BASE"], 
            _config["DISCORD_API_USERS_ME"]
        ),
        headers=headers
    )
    if r.status_code != 200:
        _logger.warn(f"Failed to fetch user information: {r.json()}")
        flash("Error authenticating. Please try again", "error")
        return redirect(url_for("index"))
    user = r.json()
    user_id = user["id"]
    username = user["username"]
    avatar = user["avatar"]

    # Now immediately revoke tokens
    data = {
        "client_id": _config["DISCORD_CLIENT_ID"],
        "client_secret": _config["DISCORD_CLIENT_SECRET"],
        "token": access_token,
        "token_type_hint": "access_token"
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post(
        "{}{}".format(_config["DISCORD_API_BASE"], _config["DISCORD_API_TOKEN_REVOKE"]),
        data=data, headers=headers)
    if r.status_code != 200:
        _logger.warn(f"Failed to revoke access token: {r.json()}")
    data = {
        "client_id": _config["DISCORD_CLIENT_ID"],
        "client_secret": _config["DISCORD_CLIENT_SECRET"],
        "token": refresh_token,
        "token_type_hint": "refresh_token"
    }
    r = requests.post(
        "{}{}".format(_config["DISCORD_API_BASE"], _config["DISCORD_API_TOKEN_REVOKE"]),
        data=data, headers=headers)
    if r.status_code != 200:
        _logger.warn(f"Failed to revoke refresh token: {r.json()}")
    
    # Now hash ID
    user_id_hash = hashlib.pbkdf2_hmac(
        "sha256", 
        user_id.encode("utf-8"), 
        _salt, 
        100000
    ).hex()

    # Create user and log user in
    expires_in = int(expires_in)
    user = create_user(user_id_hash, username, avatar, expires_in)

    # Begin user session by logging the user in
    if login_user(user, remember=True):
        session.permanent = True

        # Send user back to homepage
        flash(f"Welcome, {username}!", "info")
        return redirect(url_for("index"))
    else:
        _logger.warn("Error logging user in")
        flash("Error authenticating. Please try again", "error")
        return redirect(url_for("index"))

@blueprint.route("/logout")
@login_required
def logout():
    delete_user(current_user.get_id())
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for("index"))


@blueprint.before_app_request
def before_request():
    if hasattr(current_user, "expiration_date"): # isinstance isn't working
        if current_user.expiration_date < datetime.datetime.now():
            # Session expired
            flash("Your session has expired. Please log back in", "warning")
            delete_user(current_user.get_id())
            logout_user()
            redirect(url_for("index"))
        else:
            # Reset session
            update_user_expire(current_user.get_id())

def get_user(user_id):
    user = _db.hgetall(user_id)
    if user is None or b"user_id" not in user:
        return None
    return User(user)


def is_admin(user):
    return str(user) in _config["ADMIN_LIST"]


def create_user(user_id, username, avatar, expires_in):
    """Creates a new User id if it does not exist yet."""
    user = _db.hgetall(user_id)
    if user is None or b"user_id" not in user:
        expires = datetime.datetime.now() + datetime.timedelta(seconds=expires_in)
        user = {
            "user_id": user_id.encode("utf-8"),
            "username": username.encode("utf-8"),
            "avatar": avatar.encode("utf-8"),
            "expires_in": str(expires_in).encode("utf-8"),
            "expiration_date": expires.isoformat().encode("utf-8")
        }
        _db.hmset(user_id, user)
    return get_user(user_id)


def update_user_expire(user_id):
    """Updates a user's expiration date to now"""
    user = get_user(user_id)
    if user is not None:
        expires_in = int(user.expires_in)
        expires = datetime.datetime.now() + datetime.timedelta(seconds=expires_in)
        _db.hset(user_id, "expiration_date", expires.isoformat().encode("utf-8"))


def delete_user(user_id):
    """Deletes the user session corresponding to the user ID"""
    _db.delete(user_id)


class User(UserMixin):
    def __init__(self, mapping):
        """Inits a User object from a byte mapping"""
        self.id = mapping[b"user_id"].decode("utf-8")
        self.username = mapping[b"username"].decode("utf-8")
        self.avatar = mapping[b"avatar"].decode("utf-8")
        self.expires_in = mapping[b"expires_in"].decode("utf-8")
        self.expiration_date = mapping[b"expiration_date"].decode("utf-8")
        self.expiration_date = datetime.datetime.fromisoformat(self.expiration_date)

    def get_id(self):
        return str(self.id)
