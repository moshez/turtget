import dataclasses

from .world import World

def _redrawing(func):
    def ret_value(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        finally:
            self.world.redraw()
    ret_value.redrawing = True
    return ret_value

def _flip(attribute):
    @_redrawing
    def turn_on(self):
        setattr(self.world.turtle, attribute, True)
    @_redrawing
    def turn_off(self):
        setattr(self.world.turtle, attribute, False)
    return turn_on, turn_off

@dataclasses.dataclass
class Widget:
    world: World

    show, hide = _flip("visible")
    down, up = _flip("drawing")

    @property
    def output(self):
        self.world.redraw()
        return self.world.output

    @_redrawing    
    def turn(self, angle):
        self.world.turtle.turn(angle)

    @_redrawing    
    def forward(self, stride):
        self.world.move(stride)

    @_redrawing
    def backward(self, stride):
        self.forward(-stride)

    @_redrawing
    def reset(self):
        self.world.reset()
        
    @classmethod
    def redrawing_functions(cls):
        for name in dir(cls):
            if not getattr(getattr(cls, name), "redrawing", False):
                continue
            yield name

def start(size=600):
    the_globals = sys._getframe(1).f_globals
    tw = Widget(World(600, 600))
    for name in Widget.redrawing_functions:
        the_globals[name] = getattr(tw, name)
    return tw.output
