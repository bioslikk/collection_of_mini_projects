import logging
import os

import connexion as connexion
from flask_cors import CORS
logging.basicConfig(level=logging.INFO)

app = connexion.App(__name__)

app.add_api('swagger.yaml')
application = app.app


if __name__ == '__main__':
    CORS(application)
    # If you want to run this with a WSGI
    # use the command: uwsgi --http :8080 -w application:application -p 16
    # to run mongo do -> docker run --name some-mongo --net=host -d mongo
    app.run(port=4001, server='gevent')
