export MYSQL_PASS=
python app.py db init
python app.py db migrate
python app.py db upgrade
python app.py