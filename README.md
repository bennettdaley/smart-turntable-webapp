# smart-turntable-webapp
Web Application for Smart Turntable

https://www.youtube.com/watch?v=zS6DPLAzsAY

Software for Raspberry Pi Listener:
https://github.com/bennettdaley/smart-turntable-pi

Software for arduino:
https://github.com/bennettdaley/smart-turntable-arduino


Uses python3


To run on your machine, do the following in a terminal window:

git clone https://github.com/bennettdaley/smart-turntable-webapp.git

cd to that directory

python3.6 -m venv virtualenv

source virtualenv/bin/activate

pip install -r requirements.txt

if you get errors here, run
pip install --upgrade setuptools

if you still get errors, run
sudo apt-get install python3.6-dev libmysqlclient-dev

if you have the environment variable
script, type in:
source env.sh

otherwise type in:
export FLASK_APP=application.py
export DATABASE_URL='the database url'

Replace 'the database url' with the url of your database.

flask run
