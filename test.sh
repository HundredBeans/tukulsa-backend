clear && clear
export FLASK_ENV=testing
pytest --cov-fail-under=80 --cov=blueprints --cov-report html -s
export FLASK_ENV=development