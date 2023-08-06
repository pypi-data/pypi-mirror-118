from __future__ import unicode_literals  # support both Python2 and 3

import pytest

from mock import patch

import unittest2 as unittest

from pycastiphone_client.resources.login import Login
from pycastiphone_client.resources.cliente import Cliente


class ClienteTests(unittest.TestCase):

    @pytest.mark.vcr()
    def test_create(self):
        login = Login.authenticate()

        data = {
            'razonSocial': 'una razon'
        }

        cliente = Cliente.create(login.token, **data)

        for key, value in data.items():
            self.assertEqual(getattr(cliente, key), value)
