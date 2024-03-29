from rest_framework import status
from rest_framework.generics import GenericAPIView

from ..mixins import SaveSerializerMixin
from ..serializers import *  # noqa

__all__ = (
    'LogInAPIView',
    'SignupAPIView',
    'ConfirmPhoneNumberAPIView',
    'ForgotPasswordAPIView',
    'ResetPasswordAPIView',
)


class LogInAPIView(GenericAPIView, SaveSerializerMixin):
    """
    JWT authentication endpoint
    """
    serializer_class = LoginSerializer
    save = False


class SignupAPIView(GenericAPIView, SaveSerializerMixin):
    status_code = status.HTTP_201_CREATED
    serializer_class = SignupSerializer


class ConfirmPhoneNumberAPIView(GenericAPIView, SaveSerializerMixin):
    serializer_class = ConfirmPhoneNumberSerializer


class ForgotPasswordAPIView(GenericAPIView, SaveSerializerMixin):
    serializer_class = ForgotPasswordSerializer


class ResetPasswordAPIView(GenericAPIView, SaveSerializerMixin):
    serializer_class = ResetPasswordSerializer
