from server import get_app, config


if __name__ == '__main__':
    with get_app().app_context():
        config.db.create_all()
