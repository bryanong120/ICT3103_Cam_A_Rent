import pytest
from flask import Flask

from app_factory import create_app

@pytest.fixture()
def base_app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    app.config['WTF_CSRF_ENABLED'] = False

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(base_app):
    return base_app.test_client()


@pytest.fixture()
def runner(base_app):
    return base_app.test_cli_runner()