import uvicorn

from database import db, models

if __name__ == '__main__':
    db.connect()
    db.create_tables([models.User, models.Profile])
    db.close()
    uvicorn.run("routers.main:app", reload=True)
