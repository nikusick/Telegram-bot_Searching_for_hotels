from database.utils.CRUD import CRUDInteface
from database.common.models import db, User, Query

db.connect()
db.create_tables([User, Query])

crud = CRUDInteface()

if __name__ == "main":
    crud()
