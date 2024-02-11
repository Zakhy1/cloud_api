import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class UpperCaseLetterContainValidator:
    def __init__(self, count=1):
        self.count = count

    def validate(self, password, user=None):
        if len(re.findall('[A-Z]', password)) < self.count:
            raise ValidationError(
                _(f'The password must contain at least {self.count} uppercase letters, A-Z'), code='password_no_upper')

    def get_help_text(self):
        return _(f'Your password must contain at least %{self.count} uppercase letters')


class LowerCaseLetterContainValidator:
    def __init__(self, count=1):
        self.count = count

    def validate(self, password, user=None):
        if len(re.findall('[a-z]', password)) < self.count:
            raise ValidationError(
                _(f'The password must contain at least {self.count} lowercase letters, a-z'), code='password_no_upper')

    def get_help_text(self):
        return _(f'Your password must contain at least %{self.count} lowercase letters')


class NumberContainValidator:
    def __init__(self, count=1):
        self.count = count

    def validate(self, password, user=None):
        if len(re.findall('\d', password)) < self.count:
            raise ValidationError(
                _(f'The password must contain at least {self.count} numbers, 0-9'), code='password_no_number')

    def get_help_text(self):
        return _(f'Your password must contain at least %{self.count} numbers, 0-9')