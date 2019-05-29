from waitress import serve
from manage import app


serve(app, listen='*:80')
