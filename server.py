from flask import Flask

from components.users import routes as user_routes
from settings import config


def get_app():
    app = Flask(__name__)
    app.config.from_object(config)

    user_routes.bind(app)
    config.db.init_app(app)

    return app


if __name__ == '__main__':
    # Run server with toggled on debug mode for visible traceback
    get_app().run(debug=True)
