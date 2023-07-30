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

        

def flip(attribute, name_on, name_off):
    def decorator(klass):
        def turn_on(self):
            setattr(self.world.turtle, attribute, True)
            self.world.redraw()
        def turn_off(self):
            setattr(self.world.turtle, attribute, False)
            self.world.redraw()
        setattr(klass, name_on, turn_on)
        setattr(klass, name_off, turn_off)
        return klass
    return decorator

@flip("visible", "show", "hide")
@flip("drawing", "down", "up")
@dataclasses.dataclass
class TurtleWorld:
    world: World
    
    @property
    def output(self):
        self.world.redraw()
        return self.world.output
    
    def turn(self, angle):
        self.world.turtle.turn(angle)
        self.world.redraw()

    def forward(self, size):
        self.world.move(size)
        self.world.redraw()

    def backward(self, size):
        self.forward(-size)

    def reset(self):
        self.world.reset()
        self.world.redraw()

tw = TurtleWorld(World((600, 600)))
for name in ["turn", "forward", "backward", "show", "hide", "down", "up", "reset"]:
    globals()[name] = getattr(tw, name)
tw.output