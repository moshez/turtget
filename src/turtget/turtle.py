from __future__ import annotations
from importlib import resources
import dataclasses
from typing import Tuple, Optional

from PIL import Image

def _get_turtle_icon() -> Image.Image:
    turtle = resources.files("turtget").joinpath("turtle.png")
    raw_img = Image.open(turtle)
    return raw_img.resize((20, 20)).convert("RGBA")

_TURTLE_ICON = _get_turtle_icon()

@dataclasses.dataclass
class Turtle:
    visible: bool = dataclasses.field(default=True, init=False)
    drawing: bool = dataclasses.field(default=True, init=False)
    heading: int = dataclasses.field(default=0, init=False)
    location: Tuple[int, int] = dataclasses.field(default=(0, 0), init=False)
    
    @property
    def true_heading(self) -> float:
        return ((self.heading - 90) / 360) * math.tau

    def turn(self, angle: float) -> None:
        self.heading = (self.heading + angle) % 360
        
    def move(self, stride: int, size: int) -> Optional[Tuple[Tuple[int,int],Tuple[int,int]]]:
        x, y = self.location
        hd = self.true_heading
        max_x, max_y = size
        corr_x, corr_y = (value//2 for value in size)
        relative_x, relative_y = x + corr_x, y + corr_y
        new_relative_x = (relative_x + int(stride * math.cos(hd))) % max_x
        new_relative_y = (relative_y + int(stride * math.sin(hd))) % max_y
        self.location = new_relative_x - corr_x, new_relative_y - corr_y
        if self.drawing:
            return (relative_x, relative_y), (new_relative_x, new_relative_y)        
        
    def draw_icon(self, img: Image.Image) -> None:
        if not self.visible:
            return
        my_icon = _TURTLE_ICON.rotate(-self.heading)
        x, y = self.location
        size = img.size
        corr_x, corr_y = (value//2 for value in size)
        relative_x, relative_y = x + corr_x, y + corr_y
        dx, dy = my_icon.size
        relative_x -= dx//2
        relative_y -= dx//2
        img.paste(my_icon, (relative_x, relative_y), mask=my_icon.getchannel("A"))

