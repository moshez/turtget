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
    def from_size(cls, size: Tuple[int, int]) -> _WorldDetails:
        return cls(
            img = Image.new("RGBA", size, color=(255,255,255)),
            draw = ImageDraw.Draw(self.img),
            turtle = Turtle(),
        )

            
@dataclasses.dataclass
class World:
    size: Tuple[int, int]
    
    # In general, private methods are an anti-pattern.
    # In this case:
    # * This is barely a method
    # * It could be refactored into a `ResettableDetails`
    #   class, but the benefit for the extra complexity
    #   would be minimal.
    @functools.cached_property
    def _details(self) -> _WorldDetails:
        return _WorldDetails.from_size(self.size)
    
    @functools.cached_property
    def output(self) -> ipywidgets.Output:
        return ipywidgets.Output()
    
    @property
    def turtle(self) -> Turtle:
        return self._details.turtle

    def reset(self) -> None:
        with contextlib.suppress(AttributeError):
            del self._details
    
    def redraw(self) -> None:
        img = self._details.img.copy()
        self.turtle.draw_icon(img)
        self.output.clear_output(wait=True)
        with self.output:
            display(ImageHTML(img))

    def move(self, stride: int) -> None:
        line_params = self.turtle.move(stride, self.size)
        if line_params is None:
            return
        self._details.draw.line(line_params, width=2, fill=(0,0,0))
