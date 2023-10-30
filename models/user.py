#!/usr/bin/python3
""" holds class User"""
from models import storage_t
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
import hashlib
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user", cascade="delete")
        reviews = relationship("Review", backref="user", cascade="delete")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        if kwargs:
            pwd = kwargs.pop("password", None)
            if pwd:
                User.__hash_password(self, pwd)
        super().__init__(*args, **kwargs)

    def __hash_password(self, pwd):
        """Constructor for Hash encrypting password attribute to MD5."""
        hash = hashlib.md5()
        hash.update(pwd.encode("utf-8"))
        hashed_password = hash.hexdigest()
        super().__setattr__(self, "password", hashed_password)
