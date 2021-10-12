# **Participons - backend**

The backend is using Python and Django REST, it serves as API for the frontend part ([branch heroku-frontend](https://github.com/vicsim181/P13/tree/heroku-frontend)).

Two applications composes this API, one managing the authentication process (users and addresses) and one managing everything related to the projects (projects, comments, questions...).

For detailed informations on how to use and settle Django REST, check the [official documentation](https://www.django-rest-framework.org/).

## **How to install the backend?**

Make sure to have a Python version installed greater or equal to the 3.6.

Fork this repository or download the files and install the dependencies with:

On Windows:

```bash
> pip install -r requirements.txt
```

On Linux:

```bash
> pip3 install -r requirements.txt
```

### The authentication application

This application contains the models, views and serializers managing the different actions on the User and Address models as well as the login function.

The main views concerning the User and Address are accessible through urls defined by the Django REST ModelViewSet object. The UserDataView is accessed by a special url defined as "me/", giving the detailed informations about the loggedin user when called.
