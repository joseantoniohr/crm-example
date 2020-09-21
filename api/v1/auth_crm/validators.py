import re

from django.utils.translation import ugettext as _

from rest_framework import serializers


class UsernameUnicodeValidator(object):

    regex = r'^[\w.@+-]+\Z'
    message = _(
        'Enter a valid username. This value may contain only letters, '
        'numbers, and @/./+/-/_ characters.'
    )

    def __call__(self, value):
        result = re.match(self.regex, value)
        if not result:
            raise serializers.ValidationError(self.message)
