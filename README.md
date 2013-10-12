Hi, I started to write tmdb from scratch. It's easier that way, and it supports
API v3.

themoviedb.org wrapper for api v3
---------------------------------

- Old wrapper renamed to themoviedb_oldapi:
  https://github.com/doganaydin/themoviedb_oldapi
- Temporarily, only movie search api is implemented.
- Please edit wiki page to add yourself to WhoUses page.

Installation
------------

```bash
$ sudo python setup.py install
$ pip install -r requirements.txt
# Alternatively, for Python 3:
$ sudo python3 setup.py install
```

Usage
-----

First, you need to get an API key from [TMDB](http://www.themoviedb.org/)
(you'll need a user account for that). Then, assuming that `api_key` is a
string containing your API key:

```python
import tmdb
tmdb.configure(api_key)
# Search for movie titles containing "Alien"
movies = tmdb.Movies("Alien")
for movie in movies.iter_results():
    # Pick the movie whose title is exactly "Alien"
    if movie["title"] == "Alien":
        # Create a Movie object, fetching details about it
        movie = tmdb.Movie(movie["id"])
        break
# Access the fetched information about the movie
movie.get_tagline() # or other methods...
```

For a complete list of methods currently available in `Movie` objects, type
`help(tmdb.Movie)` on the Python prompt.

If movie search hangs for too long, use `limit=True`:
`movies = tmdb.Movies("matrix", limit=True)`. Now movie search only returns the
first page of results.

User Authentication
-------------------

In order to modify a movie on [TMDB](http://www.themoviedb.org/), you'll need
to authenticate first:

```python
import tmdb
tmdb.configure(api_key)
auth = tmdb.Core()
rt = auth.request_token()
auth.session_id(rt["request_token"])
# Now you can for instance rate the movie
movie.add_rating(1)
```
Contributors
=============
   Thomas [@tloiret](https://github.com/authmillenon)

   Martin Lenders [@authmillenon](https://github.com/authmillenon)

   lad1337 [@lad1337](https://github.com/lad1337)

   George Dorn    [@georgedorn](https://github.com/georgedorn)
   
   Farrin Reid    [@blakmatrix](https://github.com/blakmatrix)
   
   Benoît Knecht  [@BenoitKnecht](https://github.com/BenoitKnecht)
   
   Alan Justino da Silva    [@alanjds](https://github.com/alanjds)
  
   Dustin Wyatt    [@therms](https://github.com/therms)
