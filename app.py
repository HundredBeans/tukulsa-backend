import logging
import sys
from blueprints import app, manager
from flask_restful import Api
from logging.handlers import RotatingFileHandler
from werkzeug.contrib.cache import SimpleCache
import line

cache = SimpleCache()

# initiate flask-restful instance
api = Api(app, catch_all_404s=True)

if __name__ == '__main__':
    try:
        if sys.argv[1] == 'db':
            manager.run()
    except Exception as e:
        # define log format and create a rotating log
        formatter = logging.Formatter(
            "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s"
        )
        log_handler = RotatingFileHandler(
            "%s/%s" % (app.root_path, '../storage/log/app.log'), maxBytes=100000, backupCount=10
        )
        logging.getLogger().setLevel(logging.INFO)
        log_handler.setFormatter(formatter)
        app.logger.addHandler(log_handler)
        app.run(debug=False, host='0.0.0.0', port=5000)
