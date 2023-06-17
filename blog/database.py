from contextvars import ContextVar
from typing import Dict, Optional
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session as SQLASession
from blog import _Session, engine

_session: ContextVar[Optional[SQLASession]] = ContextVar("_session", default=None)

Base = declarative_base()

class MissingSessionError:
    """
    Raised when a session is accessed before it has been initialised
    """
    pass

class SessionMeta(type):
    """
    using this metaclass means that we can access db.session as a property at a class level,
    """
    @property
    def session(self) -> SQLASession:
        """Return an instance of Session local to the current async context."""
        if _Session is None:
            raise SessionNotInitialisedError

        session = _session.get()
        if session is None:
            raise MissingSessionError

        return session

class SessionNotInitialisedError(Exception):
    """
    Raised when a session is accessed before it has been initialised
    """
    pass

class Session(metaclass=SessionMeta):
    """
    Context manager for a session
    """
    def __init__(self, session_args: Dict = None, commit_on_exit: bool = False):
        self.token = None
        self.session_args = session_args or {}
        self.commit_on_exit = commit_on_exit

    def __enter__(self):
        """
        These methods are called when the Session() object is used as a context manager.
        :return: Session object
        """
        if not isinstance(_Session, sessionmaker):
            raise SessionNotInitialisedError
        self.token = _session.set(_Session(**self.session_args))
        return type(self)

    def __exit__(self, exc_type, exc_value, traceback):
        """
        These methods are called when the Session() object is used as a context manager.
        :return: None
        """
        sess = _session.get()
        if exc_type is not None:
            sess.rollback()

        if self.commit_on_exit:
            sess.commit()

        sess.close()
        _session.reset(self.token)


class ModelMixin(Base, metaclass=SessionMeta):
    """
    Base model for all models
    """
    __abstract__ = True

    # saves a model instance to the database and commits the session when the instance is created
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session.add(self)
        self.session.commit()

db: SessionMeta = Session

with db():
    ModelMixin.set_session(db.session)

ModelMixin.metadata.create_all(bind = engine)