import uuid
from datetime import datetime

from sqlalchemy import Column, UUID, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class AbstractModel(Base):

    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    created_at = Column(DateTime, default=datetime.now)

    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
