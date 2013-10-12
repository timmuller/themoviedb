# -*- coding: utf-8 -*-
import unittest
import tmdb
import mock


class TmdbCoreTest(unittest.TestCase):

    def setUp(self):
        tmdb.configure("API_KEY")
        self.core = tmdb.Core()

    def test_getJSON_returns_message_content_of_request(self):
        with mock.patch('requests.get') as request_mock:
            request_object = mock.Mock()
            request_object.content = '{"args": {"m": "hello"}}'
            request_mock.return_value = request_object
            self.assertEqual(self.core.getJSON("http://someurl")["args"]["m"], "hello")

    def test_getJSON_returns_unicode_message_content_of_request(self):
        with mock.patch('requests.get') as request_mock:
            request_object = mock.Mock()
            request_object.content = '{"args": {"m": "hello √"}}'
            request_mock.return_value = request_object
            self.assertEqual(self.core.getJSON("http://someurl")["args"]["m"], "hello √".decode('utf8'))

    def test_escape_escapes_white_space(self):
        self.assertEqual(self.core.escape("Hello tmdb"), "Hello%20tmdb")

    def test_request_token_retrieves_request_token_out_of_fourthy_chars_of_request_object(self):
        with mock.patch('requests.get') as request_mock:
            request_object = mock.Mock()
            request_object.content = '{"request_token": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"}'
            request_mock.return_value = request_object

            self.assertEqual(self.core.request_token()['request_token'], "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")

    @unittest.skip("not implemented")
    def test_request_token_gives_an_exception_when_token_is_not_fouthy_chars_long(self):
        pass

    def test_session_id_retrieves_session_id_out_of_fourthy_chars_of_request_object(self):
        with mock.patch('requests.get') as request_mock:
            request_object = mock.Mock()
            request_object.content = '{"session_id": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"}'
            request_mock.return_value = request_object

            self.assertEqual(self.core.session_id('A_TOKEN'), "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")

    @unittest.skip("not implemented")
    def test_session_id_gives_an_exception_when_token_is_not_fouthy_chars_long(self):
        pass

