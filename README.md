
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


```
API Endpoints
    My Profile Page:
        api/myrecommended --> Recommended people to follow (need to send token with request)
        api/myaccount --> The requesting users account info: email, token ... (need to send token with request)
        api/account/<user_id>/saved --> User's saved events based on their url
        api/account/<user_id>/posted --> User's posted events based on their url
        api/account/<user_id>/followers --> Get a user's followers list
        api/account/<user_id>/following --> Get a user's following list 
        api/account/<user_id>/requesting --> Get a list of users that are requesting to follow the current user (need to send token)
        api/account/<user_id>/requested --> Get a list of users the current user has requested to follow (need to send token with request)
    
    Following a user:
        api/account/<user_id>/follow  (POST) --> Follow a user (need to send token with request)
        api/account/<user_id>/follow (PUT) --> Accept a follow request (need to send token with request)
        api/account/<user_id>/follow (DELETE) --> Delete a follower or a follow request (need to send token with request)
    
    Event Card:
        api/events/<event_id>/save (POST) --> Save an event (need to send token with request)
        api/events/<event_id>/save (DELETE) --> Unsave an event (need to send token with request)
        api/events/<event_id>/people_saving (GET) --> get a list of users saving an event
        
All other API endpoints that don't have any internal/hidden endpoints and are fairly straight forward to use are in the link below
--> http://wpoppin.com/api/   (the links are pretty self explanatory0
```

