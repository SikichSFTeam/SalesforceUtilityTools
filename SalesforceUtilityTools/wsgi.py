from os import environ
from SalesforceUtilityTools import app


def create_app():
    #HOST = environ.get('SERVER_HOST', 'localhost')
    #try:
    #    PORT = int(environ.get('SERVER_PORT', '5555'))
    #except ValueError:
    #    PORT = 5555
    #return app.run(HOST, PORT)
    return app.run()

application = create_app()