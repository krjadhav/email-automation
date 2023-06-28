from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Email(Base):
    __tablename__ = "emails"

    email_id = Column(String, primary_key=True)
    subject = Column(String)
    sender = Column(String)
    recipient = Column(String)
    received_date = Column(DateTime)

    def __init__(self, email_id, subject, sender, recipient, received_date):
        self.email_id = email_id
        self.subject = subject
        self.sender = sender
        self.recipient = recipient
        self.received_date = received_date
