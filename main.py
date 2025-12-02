import init_django_orm #noqa F401
from db.models import Ticket, Order, CinemaHall, MovieSession
import datetime


from services import user

# user.create_user(username="john",
#                  password="jabkf",
#                  first_name="johua",
#                  last_name="froggy")
#
# user.update_user(5, "eererere",
#                  "hrufhru",
#                  "lolk",
#                  "lolkix",
#                  "hrufhru")