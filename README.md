
# mysite

## Getting Started

In local Decelopment change the database settings in settings.py to be

```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "dev.db",
    }
}
```

Make sure you are using a virtual environment of some sort (e.g. `virtualenv` or
`pyenv`).


```
pip install -r requirements.txt
./manage.py migrate
./manage.py loaddata sites
./manage.py runserver
```

Repo Hierarchy:

'Post': Event app, contains the main event model and views controlling the website
'account': Account app, contains the extended User model that handles user login/signup
'restapi': REST app, app where all models are converted to rest endpoints with GET/POST/DELETE ... endpoints. All rest endpoints end up here.
'blog': Stories app, 
'mysite': main django project file

most of the other apps are external apps that I needed to make changes to. They really don't matter.


