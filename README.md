
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
./manage.py makemigrations (if on a windows system, it's python manage.py)
./manage.py migrate
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
        
    Notifications:
        api/devices (POST) --> Required Parameters:
                           --> registration_id (integer), active(boolean- should be set to true), type (android, ios, or web)
                           --> (need to send token with request)                   
                        
                    --> Add a user's registration_id to our database. Link a user to a device 
                    -->  Needed in order to allow device specific notifications on events like following, commenting...
```

All other API endpoints that don't have any internal/hidden endpoints and are fairly straight forward to use are in the link below
--> http://wpoppin.com/api/   (the links are pretty self explanatory)

CURL Commands for testing REST API (You have to have curl installed before hand - simplest way is to use pip)
```
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token xxxxxxxxxxxxxx" -d '{"key1":"value1", "key2":"value2"}' http://www.wpoppin.com/api/devices/

The 'POST' can change depending on the type of request you want. i.e 'PUT', 'PATCH' ...
```
Reference https://gist.github.com/subfuzion/08c5d85437d5d4f00e58 for more curl commands 

