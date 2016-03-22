import falcon
from helpers import generate_formdata
app = falcon.API(before=[generate_formdata])

from main.views import *