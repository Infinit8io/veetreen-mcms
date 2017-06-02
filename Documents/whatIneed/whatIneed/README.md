# WhatINeed

On m'a demandé quelques fois « Hey, comment s'appelle ton app pour organiser des soirées ? J'en aurais besoin ! », l'application en question était le projet web : https://github.com/HE-Arc/EventOrganizer.

Du coup comme l'été va bientôt arriver ça sera la saison des grillades au bord du lac, et souvent on doit s'organiser pour savoir qui prend quoi. Bref, tout ça pour dire que je pense que cette application a du potentiel et l'idée me tient à cœur.

Je vous ai ajouté dans le repo tous simplement parce que vous avez bossé dessus avant, ou que vous étiez intéressés par le concept. *J'insiste, je n'oblige personne à bosser sur ce projet, si vous avez envie de vous investir c'est cool ! Sinon pas problème*, et il n'y a pas qu'au niveau du code que vous pouvez contribuer, il y a aussi les aspects design, marketing, etc.

Pour que tout le monde puisse travailler dessus le _stack_ sera le suivant:

* MySQL
* Django
* jQuery & Handlebars.js (Ou un autre template JS)
* Bootstrap4

Donc voilà, dès que j'aurai le temps je ferai des issues et chacun pourra y contribuer comme bon lui semble !



# Installation

1. Install [NPM](https://www.npmjs.com/get-npm) and [YARN](https://yarnpkg.com/lang/en/docs/install/)

    ```console
    $ yarn
    $ npm run production
    ```

2. Create a python3 virtualenv and install python requirements.txt (Pip install .)

    ```console
    $ python3 -m venv
    $ . bin/activate
    (whatineed) $ pip install -r requirements.txt
    ```

    ```
    > conda create -n whatineed python=3
    > activate whatineed
    (whatineed)> pip install -r requirements.txt
    ```

3. Migrate and create a superuser

    ```console
    (whatineed) $ python manage.py migrate
    (whatineed) $ python manage.py createsuperuser
    ```

4. Facebook Auth won't work, you need to configure it, see allauth configuration for that.
   In the meantime, log in using the superuser `/admin`.

# Local Configuration

1. Create the file `local_settings.py`

    ```python
    """Sample local settings for working with docker-compose.yml."""

    from whatineed.settings import *  # noqa

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'django',
            'USER': 'django',
            'PASSWORD': 'django',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'OPTIONS': {
                'charset': 'utf8mb4'
            }
        }
    }

    # Mailhog
    EMAIL_HOST = '127.0.0.1'
    EMAIL_PORT = 1025

    # Redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # Caches
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://{}:{}/1".format(REDIS_HOST, REDIS_PORT),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient"
            }
        }
    }

    # Session
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"
    ```

2. Set the environment variable `DJANGO_SETTINGS_MODULE` accordingly

    ```console
    (whatineed) $ export DJANGO_SETTINGS_MODULE=local_settings
    (whatineed) $ python manage.py migrate
    ```

3. Run the server

    ```console
    (whatineed) $ python manage.py runserver
    ```
