from __future__ import unicode_literals  # support both Python2 and 3

import pytest

import unittest2 as unittest

from pycastiphone_client.resources.login import Login


class LoginTests(unittest.TestCase):

    @pytest.mark.vcr()
    def test_authenticate(self):
        login = Login.authenticate()

        expected_token = "{} {}".format(login.token_type, login.access_token)

        self.assertEqual(login.token, expected_token)
