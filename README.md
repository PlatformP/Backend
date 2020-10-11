# GrassRootsBackend
This is the backend for grassrootsusa.com
To interact with the frontend it uses REST endpoints

## Setting Up The Project
Set up a python virtual environment using anaconda with the name 'candid-politics' and python=3.8. For anaconda refrence use this [Link](https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf).
then use pip to install the modules from the requirments.txt.

Once you have the project cloned and the python environment set up cd into the project. To create the migrations type in `python manage.py makemigrations` followed by `python manage.py migrate`. This populates the databases and creates the migrations. Then to create a admin user write `python manage.py createsuperuser` and fill out the information.

## Running the Project
to run te project either run it in the IDE of your choice or cd into the project directory and type `python manage.py runserver`. This runs the development server. To access the admin page go to *127.0.0.1:8000/admin*. To access the API page go to *127.0.0.1:8000/API*

## Calling the API
In order to call the API first run the API generation script -> *Scripts/DataMigrations/ApiKeyGeneration.py*. This stores the api-key in a text file called api_key.txt in the base directory. Then when calling the url pass the API Key in a header `API-KEY: ********` where ****** is the API key

## JWT
The token endpoint is `../API/token/` which is a post that accepts user credentials. This returns a token and a refresh token. To refresh a token after it has been deactivated got to `.../API/token/refresh/` and pass the refresh token into the post

## Github Desktop
we will use Github desktop to commit work. there is a guide [here](https://docs.github.com/en/desktop)
We have a dev and a master branch. The master branch will be updated from the dev once we decide to merge changes onto the server
the commit process will go like this:
1. Commit changes
2. "Merge Into Currecnt Branch" (ctr+shift+M) and select dev
3. Push Origin
4. Create pull request

## Django Refrences
starting out with django -> [django tutorial](https://www.djangoproject.com/start/)

- Model Refrence - [model](https://docs.djangoproject.com/en/3.1/topics/db/models/)
- Admin Refrence - [admin](https://docs.djangoproject.com/en/3.1/ref/contrib/admin/)

## Anaconda Refrence
Anaconda is a python package manager

- download link - [download](https://www.anaconda.com/products/individual)
- cheat sheet - [sheet](https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf)

## Running Backend Server
run the following commands `cd CandidPoliticsBackend` then `source venv/bin/activate` then `python manage.py runserver 0.0.0.0:8000`

## DB
We are using a postgres DataBase

![DB](/Docs/images/db_png.png)