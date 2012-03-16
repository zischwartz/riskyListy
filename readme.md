# Requirements
 - django
 - django-registration-defaults

First, get `pip` if you don't have it already. It allows you to install python modules super easily. To get it type:
    easy_install pip

And then never, ever use easy_install again.

To install django-registration-defaults:
    pip install django-registration-defaults


Assuming you have django installed, start this by running
    
    python manage.py syncdb 

to set up the sqlite database for development.

Next, to start the dev server, run
    
    python manage.py runserver

and a placeholder should show up at http://127.0.0.1:8000/



