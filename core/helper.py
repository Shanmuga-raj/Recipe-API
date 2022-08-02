from django.contrib.auth import get_user_model


def create_user(email="fakeUser@email.com", password="FakePassword", **args):
    return get_user_model().objects.create_user(email, password, **args)


def create_superuser(email="fakeAdmin@email.com", password="FakePassword", **args):
    return get_user_model().objects.create_superuser(email, password, **args)
