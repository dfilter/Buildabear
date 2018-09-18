# Buildabear
Capstone RPG Build Guide Website

# Installation:
1. Install python version 2.7.14
2. Install pipenv via "pip install pipenv"
3. cd to project "cd /%pathtoproject/Buildabear"
4. Run "pipenv install" this will automatically install requirements from Pipfile and Pipfile.lock
5. Run "pipenv shell"
6. Run "pipenv run python main.py"
7. Navigate to "localhost:5000" in web browser
8. Enjoy!

# Database Migrations
1. Enter pipenv shell
2. ```set FLASK_APP=main.py```
3. ```flask db init```
4. ```flask db migrate -m "some message"```
5. ```flask db upgrade```
