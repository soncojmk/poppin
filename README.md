
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

