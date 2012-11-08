#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author:doganaydin
#project:themoviedb
#repository:http://github.com/doganaydin/themoviedb
#license: LGPLv3 http://www.gnu.org/licenses/lgpl.html
"""An interface to the themoviedb.org API"""

__author__ = "doganaydin"
__version__ = "0.1"

try:
    import simplejson
except:
    import json as simplejson

import requests

config = {}

def configure(api_key):
    config['apikey'] = api_key
    config['urls'] = {}
    config['urls']['movie.search'] = "https://api.themoviedb.org/3/search/movie?query=%%s&api_key=%(apikey)s&page=%%s" % (config)
    config['urls']['movie.info'] = "https://api.themoviedb.org/3/movie/%%s?api_key=%(apikey)s" % (config)
    config['urls']['people.search'] = "https://api.themoviedb.org/3/search/person?query=%%s&api_key=%(apikey)s&page=%%s" % (config)
    config['urls']['collection.info'] = "https://api.themoviedb.org/3/collection/%%s&api_key=%(apikey)s" % (config)
    config['urls']['movie.alternativetitles'] = "https://api.themoviedb.org/3/movie/%%s/alternative_titles?api_key=%(apikey)s" % (config)
    config['urls']['movie.casts'] = "https://api.themoviedb.org/3/movie/%%s/casts?api_key=%(apikey)s" % (config)
    config['urls']['movie.images'] = "https://api.themoviedb.org/3/movie/%%s/images?api_key=%(apikey)s" % (config)
    config['urls']['movie.keywords'] = "https://api.themoviedb.org/3/movie/%%s/keywords?api_key=%(apikey)s" % (config)
    config['urls']['movie.releases'] = "https://api.themoviedb.org/3/movie/%%s/releases?api_key=%(apikey)s" % (config)
    config['urls']['movie.trailers'] = "https://api.themoviedb.org/3/movie/%%s/trailers?api_key=%(apikey)s" % (config)
    config['urls']['movie.translations'] = "https://api.themoviedb.org/3/movie/%%s/translations?api_key=%(apikey)s" % (config)
    config['urls']['person.info'] = "https://api.themoviedb.org/3/person/%%s&api_key=%(apikey)s" % (config)
    config['urls']['person.credits'] = "https://api.themoviedb.org/3/person/%%s/credits?api_key=%(apikey)s" % (config)
    config['urls']['person.images'] = "https://api.themoviedb.org/3/person/%%s/images?api_key=%(apikey)s" % (config)
    config['urls']['latestmovie'] = "https://api.themoviedb.org/3/latest/movie?api_key=%(apikey)s" % (config)
    config['urls']['config'] = "https://api.themoviedb.org/3/configuration?api_key=%(apikey)s" % (config)
    config['urls']['request.token'] = "https://api.themoviedb.org/3/authentication/token/new?api_key=%(apikey)s" % (config)
    config['urls']['session.id'] = "https://api.themoviedb.org/3/authentication/session/new?api_key=%(apikey)s&request_token=%%s" % (config)
    config['urls']['movie.add.rating'] = "https://api.themoviedb.org/3/movie/%%s/rating?session_id=%%s&api_key=%(apikey)s" % (config)
    config['api'] = {}
    config['api']['backdrop.sizes'] = ""
    config['api']['base.url'] = ""
    config['api']['poster.sizes'] = ""
    config['api']['profile.sizes'] = ""
    config['api']['session.id'] = ""


class Core(object):
    def getJSON(self,url):
        page = requests.get(url).content
        try:
            return simplejson.loads(page)
        except:
            return simplejson.loads(page.decode('utf-8'))

    def escape(self,text):
        if len(text) > 0:
            return requests.utils.quote(text)
        return False

    def update_configuration(self):
        c = self.getJSON(config['urls']['config'])
        config['api']['backdrop.sizes'] = c['images']['backdrop_sizes']
        config['api']['base.url'] = c['images']['base_url']
        config['api']['poster.sizes'] = c['images']['poster_sizes']
        config['api']['profile.sizes'] = c['images']['profile_sizes']
        return "ok"

    def backdrop_sizes(self,img_size):
        size_list = {'s':'w300','m':'w780','l':'w1280','o':'original'}
        return size_list[img_size]

    def poster_sizes(self,img_size):
        size_list = {'s':'w92','m':'185','l':'w500','o':'original'}
        return size_list[img_size]

    def profile_sizes(self,img_size):
        size_list = {'s':'w45','m':'185','l':'w632','o':'original'}
        return size_list[img_size]

    def request_token(self):
        req = self.getJSON(config['urls']['request.token'])
        r = req["request_token"]
        return {"url":"http://themoviedb.org/authenticate/%s" % r,"request_token":r}

    def session_id(self,token):
        sess = self.getJSON(config['urls']['session.id'] % token)
        config['api']['session.id'] = sess["session_id"]
        return sess["session_id"]

class Movies(Core):
    def __init__(self, title="", limit=False):
        self.limit = limit
        self.update_configuration()
        title = self.escape(title)
        self.movies = self.getJSON(config['urls']['movie.search'] % (title,str(1)))
        pages = self.movies["total_pages"]
        if not self.limit:
            if int(pages) > 1:                  #
                for i in range(2,int(pages)+1): #  Thanks @tBuLi
                    self.movies["results"].extend(self.getJSON(config['urls']['movie.search'] % (title,str(i)))["results"])

    def get_total_results(self):
        if self.limit:
            return len(self.movies["results"])
        return self.movies["total_results"]

    def iter_movies(self):
        for i in self.movies["results"]:
            yield Movie(i["id"])

    def iter_results(self):
        for i in self.movies["results"]:
            yield i

    def get_id(self,movie_index=0):
        return self.movies["results"][movie_index]["id"]

    # Sizes = s->w300 m->w780 l->w1280 o->original(default)
    def get_backdrop(self,img_size="o",movie_index=0):
        img_path = self.movies["results"][movie_index]["backdrop_path"]
        return config['api']['base.url']+self.backdrop_sizes(img_size)+img_path

    def get_original_title(self,movie_index=0):
        return self.movies["results"][movie_index]["original_title"]

    def get_popularity(self,movie_index=0):
        return self.movies["results"][movie_index]["popularity"]

    def get_release_date(self,movie_index=0):
        return self.movies["results"][movie_index]["release_date"]

    def get_title(self,movie_index=0):
        return self.movies["results"][movie_index]["title"]

    # Sizes = s->w92 m->w185 l->w500 o->original(default)
    def get_poster(self,img_size="o",movie_index=0):
        img_path = self.movies["results"][movie_index]["poster_path"]
        return config['api']['base.url']+self.poster_sizes(img_size)+img_path

class Movie(Core):
    def __init__(self,movie_id):
        self.movie_id = movie_id
        self.update_configuration()
        self.movies = self.getJSON(config['urls']['movie.info'] % self.movie_id)

    def is_adult(self):
        return self.movies['adult']

    def get_collection_id(self):
        return self.movies['belongs_to_collection']["id"]

    def get_collection_name(self):
        return self.movies['belongs_to_collection']["name"]

    # Sizes = s->w300 m->w780 l->w1280 o->original(default)
    def get_collection_backdrop(self,img_size="o"):
        img_path = self.movies["belongs_to_collection"]["backdrop_path"]
        return config['api']['base.url']+self.poster_sizes(img_size)+img_path

    # Sizes = s->w92 m->w185 l->w500 o->original(default)
    def get_collection_poster(self,img_size="o"):
        img_path = self.movies["belongs_to_collection"]["poster_path"]
        return config['api']['base.url']+self.poster_sizes(img_size)+img_path

    def get_budget(self):
        return self.movies['budget']

    def get_genres(self):
        genres = []
        for i in self.movies['genres']:
            genres.append({"id":i["id"],"name":i["name"]})
        return genres

    def get_homepage(self):
        return self.movies['homepage']

    def get_imdb_id(self):
        return self.movies['imdb_id']

    def get_overview(self):
        return self.movies_full['overview']

    def get_production_companies(self):
        for i in self.movies['production_companies']:
            companies = {"id":i["id"],"name":i["name"]}
        return companies

    def get_productions_countries(self):
        for i in self.movies['production_countries']:
            countries = {"iso_3166":i["iso_3166"],"name":i["name"]}
        return countries

    def get_revenue(self):
        return self.movies['revenue']

    def get_runtime(self):
        return self.movies['runtime']

    def get_spoken_languages(self):
        for i in self.movies['spoken_languages']:
            langs = {"iso_639_1":i["iso_639_1"],"name":i["name"]}
        return langs

    def get_tagline(self):
        return self.movies['tagline']

    def get_vote_average(self):
        return self.movies['vote_average']

    def get_vote_count(self):
        return self.movies['vote_count']

    def add_rating(self,value):
        if isinstance(value,float) or isinstance(value,int):
            if config["api"]["session.id"] == "":
                return "PROBLEM_AUTH"
            sess_id = config["api"]["session.id"]
            data = {"value":float(value)}
            req = requests.post(config['urls']['movie.add.rating'] % (self.movie_id,sess_id),data=data)
            res = simplejson.loads(req.content)
            if res['status_message'] == "Success":
                return True
            else:
                return False
        return "ERROR"

class People(Core):
    def __init__(self, people_name, id=-1):
        self.update_configuration()
        people_name = self.escape(people_name)
        self.people = self.getJSON(config['urls']['people.search'] % (people_name,str(1)))
        pages = self.people["total_pages"]
        self.person = ""
        self.images = ""
        for i in range(int(pages)):
            self.people["results"].extend(self.getJSON(config['urls']['people.search'] % (people_name,i))["results"]) 
        if id > -1:
            self.person = self.getJSON(config['urls']['person.info'] % id)
            self.images = self.getJSON(config['urls']['person.images'] % id)

    def full_info(self,person_id):
        self.person = self.getJSON(config['urls']['person.info'] % str(person_id))
        self.images = self.getJSON(config['urls']['person.images'] % str(person_id))

    def get_id(self,people_index=0):
        return self.people["results"][people_index]["id"]

    def is_adult(self,people_index=0):
        return self.people["results"][people_index]["adult"]

    def get_name(self,people_index=0):
        return self.people["results"][people_index]["name"]

    # Sizes = s->w45 m->w185 l->w632 o->original(default)
    def get_profile_image(self,img_size="o",people_index=0):
        img_path = self.people["results"][people_index]["profile_path"]
        return config['api']['base.url']+self.profile_sizes(img_size)+img_path

    def get_biography(self,person_id=0):
        if person_id > 0:
            self.full_info(person_id)
        return self.person['biography']

    def get_birthday(self,person_id=0):
        if person_id > 0:
            self.full_info(person_id)
        return self.person['birthday']

    def get_deathday(self,person_id=0):
        if person_id > 0:
            self.full_info(person_id)
        return self.person['deathday']

    def get_place_of_birth(self,person_id=0):
        if person_id > 0:
            self.full_info(person_id)
        return self.person['place_of_birth']

    def get_homepage(self,person_id=0):
        if person_id > 0:
            self.full_info(person_id)
        return self.person['homepage']

    def get_also_known_as(self,person_id=0):
        if person_id > 0:
            self.full_info(person_id)
        return self.person['also_known_as']

    def get_image_aspect_ratio(self,person_id=0,image_index=0):
        if person_id > 0:
            self.full_info(person_id)
        return self.images['profiles'][image_index]['aspect_ratio']

    def get_image_height(self,person_id=0,image_index=0):
        if person_id > 0:
            self.full_info(person_id)
        return self.images['profiles'][image_index]['height']

    def get_image_width(self,person_id=0,image_index=0):
        if person_id > 0:
            self.full_info(person_id)
        return self.images['profiles'][image_index]['width']

    def get_image_iso_639_1(self,person_id=0,image_index=0):
        if person_id > 0:
            self.full_info(person_id)
        return self.images['profiles'][image_index]['iso_639_1']

    #Sizes = s->w92 m->w185 l->w500 o->original(default)
    def get_image(self,img_size="o",person_id=0,image_index=0):
        if person_id > 0:
            self.full_info(person_id)
        img_path = self.images['profiles'][image_index]['file_path']
        return config['api']['base.url']+self.poster_sizes(img_size)+img_path

class Credits(Core):
    def __init__(self,person_id):
        self.update_configuration()
        self.person = self.getJSON(config['urls']['person.credits'] % person_id)

    def get_cast_id(self,person_index=0):
        return self.person["casts"][person_index]["id"]

    def get_cast_character(self,person_index=0):
        return self.person["casts"][person_index]["character"]

    def get_cast_original_title(self,person_index=0):
        return self.person["casts"][person_index]["original_title"]

    def get_cast_title(self,person_index=0):
        return self.person["casts"][person_index]["title"]

    def get_cast_release_date(self,person_index=0):
        return self.person["casts"][person_index]["release_date"]

    # Sizes = s->w92 m->w185 l->w500 o->original(default)   
    def get_cast_poster(self,img_size="o",person_index=0):
        img_path = self.person["poster_path"]
        return config['api']['base.url']+self.poster_sizes(img_size)+img_path

    def get_crew_id(self,person_index=0):
        return self.person["crew"][person_index]["id"]

    def get_crew_department(self,person_index=0):
        return self.person["crew"][person_index]["department"]

    def get_crew_job(self,person_index=0):
        return self.person["crew"][person_index]["job"]

    def get_crew_original_title(self,person_index=0):
        return self.person["crew"][person_index]["original_title"]

    def get_crew_title(self,person_index=0):
        return self.person["crew"][person_index]["id"]

    def get_crew_release_date(self,person_index=0):
        return self.person["crew"][person_index]["release_date"]

    # Sizes = s->w92 m->w185 l->w500 o->original(default)   
    def get_crew_poster(self,img_size="o",person_index=0):
        img_path = self.person["poster_path"]
        return config['api']['base.url']+self.poster_sizes(img_size)+img_path