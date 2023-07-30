import importlib.metadata

__version__ = importlib.metadata.version(__name__)

from .widget import Widget, start