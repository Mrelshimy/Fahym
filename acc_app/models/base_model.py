from acc_app import db
from datetime import datetime
import uuid


class BaseModel(db.Model):
    """
    Base model class for all models
    """
    __abstract__ = True  # Ensure this class is not used to create any tables
    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4())
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def save(self):
        """
        Save the object to the database
        """
        self.updated_at = datetime.now()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Delete the object from the database
        """
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        """
        Convert the object to a dictionary
        """
        new_dict = self.__dict__.copy()
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        return new_dict
