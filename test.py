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


class TmdbMoviesTest(unittest.TestCase):

    def setUp(self):
        tmdb.configure("API_KEY")
        self.movies = tmdb.Movies("The Avengers")

    def test_iter(self):
        for i in self.movies:
            self.assertEqual(type(i), tmdb.Movie)
            break

    def test_get_total_results(self):
        self.assertEqual(type(self.movies.get_total_results()), int)
        self.assertGreater(self.movies.get_total_results(), 1)

    def test_iter_results(self):
        for i in self.movies.iter_results():
            self.assertEqual(i["release_date"], "2012-04-26")
            break


class TmdbMovieTest(unittest.TestCase):

    def setUp(self):
        tmdb.configure("3e7807c4a01f18298f64662b257d7059")
        self.movie = tmdb.Movie(24428)

    def test_is_adult(self):
        self.assertIs(self.movie.is_adult(), False)

    def test_get_collection_id(self):
        self.assertEqual(self.movie.get_collection_id(), 86311)

    def test_get_collection_name(self):
        self.assertEqual(self.movie.get_collection_name(), "The Avengers Collection")

    def test_get_collection_backdrop(self):
        self.assertEqual(self.movie.get_collection_backdrop(), "http://cf2.imgobject.com/t/p/original/zuW6fOiusv4X9nnW3paHGfXcSll.jpg")

    def test_get_collection_poster(self):
        self.assertEqual(self.movie.get_collection_poster(), "http://cf2.imgobject.com/t/p/original/fMSxlk2zPpcXBn4R3TK3uqYjOpa.jpg")

    def test_get_budget(self):
        self.assertEqual(self.movie.get_budget(), 220000000)

    def test_get_genres(self):
        self.assertEqual(self.movie.get_genres(), [{'name': 'Action', 'id': 28}, {'name': 'Thriller', 'id': 53}])

    def test_get_homepage(self):
        self.assertEqual(self.movie.get_homepage(), "http://marvel.com/avengers_movie/")

    def test_get_imdb_id(self):
        self.assertEqual(self.movie.get_imdb_id(), "tt0848228")

    def test_get_overview(self):
        self.assertEqual(self.movie.get_overview(), "When an unexpected enemy emerges that threatens global safety and security, Nick Fury, Director of the international peacekeeping agency known as S.H.I.E.L.D., finds himself in need of a team to pull the world back from the brink of disaster. Spanning the globe, a daring recruitment effort begins!")

    def test_get_production_companies(self):
        self.assertEqual(self.movie.get_production_companies(), {'id': 3036, 'name': 'Walt Disney Studios Motion Pictures'})

    def test_get_production_countries(self):
        self.assertEqual(self.movie.get_productions_countries(), [{'name': 'United States of America', 'iso_3166_1': 'US'}])

    def test_get_revenue(self):
        self.assertEqual(self.movie.get_revenue(), 0)

    def test_get_runtime(self):
        self.assertEqual(self.movie.get_runtime(), 143)

    def test_get_spoken_languages(self):
        self.assertEqual(self.movie.get_spoken_languages(), [{'iso_639_1': 'en', 'name': 'English'}])

    def test_get_tagline(self):
        self.assertEqual(self.movie.get_tagline(), "Some assembly required.")

    def test_get_vote_average(self):
        self.assertEqual(self.movie.get_vote_average(), 8.6)

    def test_get_vote_count(self):
        self.assertGreaterEqual(self.movie.get_vote_count(), 153)

    def test_get_id(self):
        self.assertEqual(self.movie.get_id(), 24428)

    def test_get_backdrop(self):
        self.assertEqual(self.movie.get_backdrop(), "http://cf2.imgobject.com/t/p/original/hbn46fQaRmlpBuUrEiFqv0GDL6Y.jpg")

    def test_get_original_title(self):
        self.assertEqual(self.movie.get_original_title(), "The Avengers")

    def test_get_popularity(self):
        self.assertGreater(self.movie.get_popularity(), 800000)

    def test_get_release_date(self):
        self.assertEqual(self.movie.get_release_date(), "2012-04-26")

    def test_get_title(self):
        self.assertEqual(self.movie.get_title(), "The Avengers")

    def test_get_poster(self):
        self.assertEqual(self.movie.get_poster(), "http://cf2.imgobject.com/t/p/original/cezWGskPY5x7GaglTTRN4Fugfb8.jpg")

    def test_add_rating(self):
        add_rating = self.movie.add_rating(5.0)
        self.assertIsNot(add_rating, "ERROR")
        self.assertIsNot(add_rating, False)
        self.assertEqual(add_rating, "PROBLEM_AUTH")
