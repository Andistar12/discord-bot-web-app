import logging
import auth
import pages
import flask

# App and user session management
app = flask.Flask(__name__)
app.config.from_pyfile("config.py")
auth.init_app(app)
app.register_blueprint(pages.blueprint)
app.register_blueprint(auth.blueprint)

@app.route("/")
def index():
    return flask.redirect(flask.url_for("pages_blueprint.status"))


if __name__ == '__main__':
    debug = False
    if app.config["LOGGING_LEVEL"] in ["debug", "dev"]:
        app.logger.setLevel(logging.DEBUG)
        debug = True
    app.run(port = app.config["FRONTEND_PORT"], host ="0.0.0.0", debug=debug)
