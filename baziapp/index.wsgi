import sae
from blazers import wsgi

application = sae.create_wsgi_app(wsgi.application)
