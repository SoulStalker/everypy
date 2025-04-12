from .service_handlers import router as service_router
from .user_handlers import router as user_router
from .funny_handlers import router as funny_router

__all__ = ['user_router', 'service_router', 'funny_router']
