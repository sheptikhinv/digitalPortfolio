import uvicorn

from database import db, models
from helpers.config import get_value

if __name__ == '__main__':
    db.connect()
    db.create_tables([models.User, models.Profile, models.Project, models.Comment, models.ProjectImage, models.Like])
    db.close()
    if get_value("is_development").lower() == "reload":
        uvicorn.run("routers.main:app", reload=True)
    else:
        uvicorn.run("routers.main:app", host="127.0.0.1", port=5000, root_path="/api")
