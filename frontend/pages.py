from navbars import *
from auth import is_admin
import requests
from flask import (
    redirect, 
    url_for,
    flash,
    session,
    render_template,
    Blueprint,
    current_app
)
from flask_login import (
    current_user,
    login_required
)

blueprint = Blueprint("pages_blueprint", __name__)

def get_nav_bar():
    """
    Returns the navbar depending on whether the user is logged in or not,
    and whether the user is an admin or not
    """
    navbar = main_nav_bar
    if current_user.is_authenticated:
        if is_admin(current_user.get_id()):
            navbar = admin_nav_bar
        else:
            navbar = user_nav_bar
    return navbar


def get_commands():
    # TODO pull from backend
    return {
        "utilities": {
            "server": "Prints information about the current server the command was sent in. This command only works on servers, not DMs.<br><br>Command usage: <pre>server</pre>",
            "avatar": "Displays the avatar of the bot, or a target user if somebody is @ mentioned.<br><br>Command usage: <pre>avatar [target]</pre>",
            "uptime": "Displays how long the bot has been online. <br><br>Command usage: <pre>uptime</pre>"
        },
        "anime": {
            "anime": "no anime",
            "waifu": "no waifu",
            "headpat": "headpat"
        }
    } 


@blueprint.app_errorhandler(401)
def unauthorized(e):
    """Fired when accessing an unauthorized page"""
    flash("Please login to access that page", "warning")
    return redirect(url_for("index"))


@blueprint.app_errorhandler(403)
def forbidden(e):
    """Fired when a logged in user accesses a page with admin rights"""
    flash("Sorry, you do not have permission to view that page", "warning")
    return redirect(url_for("index"))


@blueprint.app_errorhandler(404)
def resourcenotfound(e):
    """Fired when accessing a non-existant page"""
    flash("Sorry, that page does not exist", "warning")
    return redirect(url_for("index"))


@blueprint.app_errorhandler(500)
def internal_error(e):
    flash("Sorry, an internal error occurred", "danger")
    return redirect(url_for("index"))


@blueprint.route("/user", methods=["GET"])
@login_required
def user():
    return render_template("user.html", nav_bar=get_nav_bar())


@blueprint.route("/admin/manage", methods=["GET"])
@login_required
def manage():
    return render_template("manage.html", nav_bar=get_nav_bar())


@blueprint.route("/status", methods=["GET"])
def status():
    headers = {"Authorization": "Bot " + current_app.config["BOT_TOKEN"]}
    response = requests.get(current_app.config["DISCORD_API_BASE"] + current_app.config["DISCORD_API_USERS_ME"], headers=headers)
    username = ""
    avatar = ""
    client_id = current_app.config["DISCORD_CLIENT_ID"]
    if response: 
        data = response.json()
        avatar = current_app.config["DISCORD_CDN_BASE"] + "avatars/" + client_id + "/" + data["avatar"] + ".png?size=512"
        username = data["username"]
    return render_template("status.html", nav_bar=get_nav_bar(), username=username, avatar=avatar, client_id=client_id)


@blueprint.route("/commands", methods=["GET"])
def commands():
    return render_template(
        "commands.html", 
        nav_bar=get_nav_bar(), 
        commands=get_commands()
    )
