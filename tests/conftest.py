import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mds.server.settings")
os.environ["MDS_JWT_SECRET_KEYS"] = "secret_for_tests"


def pytest_configure():
    django.setup()
