import sqlalchemy
from .db_session import SqlAlchemyBase


class SavedDog(SqlAlchemyBase):
    __tablename__ = "saved_dogs"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
    image_url = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    breed = sqlalchemy.Column(sqlalchemy.String, nullable=True)