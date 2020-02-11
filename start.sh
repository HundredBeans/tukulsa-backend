export BASE_URL=$BASE_URL
export CLIENT_KEY=$CLIENT_KEY
export HOST=$HOST
export IS_PRODUCTION=$IS_PRODUCTION
export MOBILEPULSA_PASSWORD=$MOBILEPULSA_PASSWORD
export MOBILEPULSA_USERNAME=$MOBILEPULSA_USERNAME
export RDS_LINK=$RDS_LINK
export RDS_PASS=$RDS_PASS
export SERVER_KEY=$SERVER_KEY
python app.py db init
python app.py db migrate
python app.py db upgrade
python app.py

