from __future__ import annotations
import base64
import contextlib
import dataclasses
import functools
from importlib import resources
import math

import ipywidgets
from IPython.display import display

from PIL import Image, ImageDraw

from .turtle import Turtle

# Workaround for JupyterLite, where Image._repr_png_ is not working properly
# when using an output as a context for some reason.
@dataclasses.dataclass(frozen=True)
class _ImageHTML:
    img: Image
    
    def _repr_html_(self):
        return f'<img src="data:image/png;base64,{base64.b64encode(self.img._repr_png_()).decode("ascii")}">'

@dataclasses.dataclass(frozen=True)
class _WorldDetails:
    img: Image.Image
    draw: ImageDraw.Draw
    turtle: Turtle
    
    @classmethod
    def from_size(cls, size):
        return cls(
            img = Image.new("RGBA", self.size, color=(255,255,255)),
            draw = ImageDraw.Draw(self.img),
            turtle = Turtle(),
        )
            
@dataclasses.dataclass
class World:
    size: Tuple[int, int]
    
    @functools.cached_property
    def details(self) -> _WorldDetails:
        return _WorldDetails.from_size(self.size)
    
    @property
    def turtle(self):
        return self.details.turtle

    def reset(self):
        with contextlib.suppress(AttributeError):
            del self.details
    
    def redraw(self):
        img = self.details.img.copy()
        self.turtle.draw_icon(img)
        self.output.clear_output(wait=True)
        with self.output:
            display(ImageHTML(img))

    def move(self, stride):
        line_params = self.turtle.move(stride, self.size)
        if line_params is None:
            return
        self.details.draw.line(line_params, width=2, fill=(0,0,0))
