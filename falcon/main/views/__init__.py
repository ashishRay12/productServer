from main import app
from .things import *

things = ThingsResource()
app.add_route('/things', things)
