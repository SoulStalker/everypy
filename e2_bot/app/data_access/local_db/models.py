from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'

    group_id = Column(String, primary_key=True)
    group_name = Column(Text, nullable=False)

    def __repr__(self):
        return f"<Group(id={self.group_id}, name={self.group_name})>"


class Contact(Base):
    __tablename__ = 'contacts'

    phone_number = Column(String, primary_key=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    telegram_id = Column(String, nullable=True)

    def __repr__(self):
        return f"<Contact(phone={self.phone_number}, name={self.first_name} {self.last_name})>"
