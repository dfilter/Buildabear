# Buildabear
Capstone RPG Build Guide Website

# Filesystem navigation:
- All files that actually make the RESTful api do what it does are located in the app folder.
- docs contains .xml files of my database structure.
- migrations contains my database migration data.
- test contains a file containing some of the tests i used withing apps/utls.py to test the database IO.
- app.db is my sqlite database.
- config.py contains my flask application configureations.
- main.py is the script run to startup the buildabear RESTful api.
- Pipfile and Pipfile.lock are used by pipenv to create my python virtual envrionment.
- Procfile is used by Heroku to run initialization tasks when deploying my app there.
- README.md is what you're looking at now! :P

# Inside the app Folder:
- static contains the favion for the api.
- templates contains the template that is rendered if for whatever reason you view the api root url.
- __init__.py contains the code neede to start up the app as well as the api endpoints.
- models.py contains the code used to create models of the tables inside of app.db.
- resources.py contains the code that handles the api requests.
- routes.py is what renders the html template if you go to the api's root url.
- utils.py contains all the quries to the app.db database. It used the models in models.py.

# Installation:
1. Install python version 2.7.15
2. ```cd /%pathtoproject%/Buildabear```
3. ```pip install pipenv```
4. ```pipenv install``` this will automatically install requirements from Pipfile and Pipfile.lock
5. ```pipenv shell```
6. ```pipenv run python main.py```
7. Navigate to "localhost:5000" in web browser
8. Enjoy!

# Database Migrations
1. Enter pipenv shell
2. ```set FLASK_APP=main.py```
3. ```flask db init```
4. ```flask db migrate -m "some message"```
5. ```flask db upgrade```
