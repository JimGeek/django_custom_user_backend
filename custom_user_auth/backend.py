from django.contrib.auth import get_user_model
from django.conf import settings

class CustomBackend(object):
    """
    Custom User backend defines the authentication system which authenticates with UID from the social login.
    It has two methods
    1. authenticate : which overrides the current authenticate method in the django backend
    2. get_user : This method defines the access to the user model
    """
    def authenticate(self,email,password=None):
        mymodel = get_user_model()

        try:
            user = mymodel.objects.get(email=email)
            return user
        except mymodel.DoesNotExist:
            return None

    def get_user(self, user_id):
        mymodel = get_user_model()
        try:
            return mymodel.objects.get(pk=user_id)
        except mymodel.DoesNotExist:
            return None