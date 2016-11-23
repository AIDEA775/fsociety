from django.contrib.auth import get_user_model


class UsernameOrEmailBackend(object):

    def authenticate(self, username=None, password=None, **kwargs):
        user_model = get_user_model()
        if username and '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = user_model.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except user_model.DoesNotExist:
            return None

    def get_user(self, username):
        try:
            return get_user_model().objects.get(pk=username)
        except get_user_model().DoesNotExist:
            return None
