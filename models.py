from main_run import db, os
from distinct_types import *


class Slot(db.Model):
    __tablename__ = "slots"
    id = db.Column(db.Text, primary_key=True)
    start = db.Column(db.Text, unique=True, nullable=False)
    end = db.Column(db.Text, unique=True, nullable=False)
    title = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return "<ID: {id} Start: {start} End: {end} Title: {title}>".format(
            id=self.id,
            start=self.start,
            end=self.end,
            title=self.title
        )

    @staticmethod
    def create_slot(slot_data: dict) -> SlotObject:
        s = Slot(**slot_data)

        return s


if "database.sqlite3" not in os.listdir(os.getcwd()):
    db.create_all()
