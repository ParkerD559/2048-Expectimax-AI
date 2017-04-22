##############################################
#
# David Parker
# crazdave@gmail.com
#
# 2017
#
##############################################
import Tkinter as Tk

CELL_COLOR = '#cdc1b4'
GRID_COLOR = '#bbada0'
TEXT_COLOR = '#776e65'
GRID_HEIGHT = 600
GRID_WIDTH = 600
CELL_WIDTH = GRID_WIDTH*.85/4
CELL_HEIGHT = GRID_HEIGHT*.85/4

COLOR_2 = '#eee4da'


def _grid_to_topleft(x, y):
    x0_border_offset = GRID_WIDTH * .03 * (x + 1)
    x0_cell_offset = CELL_WIDTH * x
    x0 = x0_border_offset + x0_cell_offset
    y0_border_offset = GRID_HEIGHT * .03 * (y + 1)
    y0_cell_offset = CELL_HEIGHT * y
    y0 = y0_border_offset + y0_cell_offset
    return x0, y0


class _Cell(object):

    def __init__(self, canvas, (x0, y0, x1, y1), value):
        if not value:
            value = '2'
        self.canvas = canvas
        self.cell_id = self.canvas.create_rectangle(x0, y0, x1, y1, fill=COLOR_2, width=0)
        self.text_id = self.canvas.create_text(x0+((x1-x0)/2), y0+((y1-y0)/2),
                                   text=value,
                                   font=('Helvetica', '36', 'bold'),
                                   fill=TEXT_COLOR)

    def delete(self):
        print "Deleting object!"
        self.canvas.delete(self.cell_id)
        self.canvas.delete(self.text_id)

    def up(self, x, y, value):
        # HAVE WE BEEN DELETED??
        if self.cell_id not in self.canvas.find_all():
            return
        new_x, new_y = _grid_to_topleft(x, y)
        curr_x, curr_y = tuple(self.canvas.coords(self.cell_id)[0:2])
        # Is the cell already there?
        if (new_x, new_y) == (curr_x, curr_y):
            self.canvas.itemconfigure(self.text_id, text=str(value))
            return
        delta_x, delta_y = new_x - curr_x, new_y - curr_y
        velocity_y = -75.0
        # Will the velocity overshoot it?
        if delta_y > velocity_y:
            velocity_y = delta_y
        self.canvas.move(self.cell_id, 0, velocity_y)
        self.canvas.move(self.text_id, 0, velocity_y)
        self.canvas.update()
        self.canvas.after(25, self.up, x, y, value)

    def down(self, x, y, value):
        if self.cell_id not in self.canvas.find_all():
            return
        new_x, new_y = _grid_to_topleft(x, y)
        curr_x, curr_y = tuple(self.canvas.coords(self.cell_id)[0:2])
        # Is the cell already there?
        if (new_x, new_y) == (curr_x, curr_y):
            self.canvas.itemconfigure(self.text_id, text=str(value))
            return
        delta_x, delta_y = new_x - curr_x, new_y - curr_y
        velocity_y = 75.0
        # Will the velocity overshoot it?
        if delta_y < velocity_y:
            velocity_y = delta_y
        self.canvas.move(self.cell_id, 0, velocity_y)
        self.canvas.move(self.text_id, 0, velocity_y)
        self.canvas.update()
        self.canvas.after(25, self.down, x, y, value)

    def left(self, x, y, value):
        if self.cell_id not in self.canvas.find_all():
            return
        new_x, new_y = _grid_to_topleft(x, y)
        curr_x, curr_y = tuple(self.canvas.coords(self.cell_id)[0:2])
        # Is the cell already there?
        if (new_x, new_y) == (curr_x, curr_y):
            self.canvas.itemconfigure(self.text_id, text=str(value))
            return
        delta_x, delta_y = new_x - curr_x, new_y - curr_y
        velocity_x = -75.0
        # Will the velocity overshoot it?
        if delta_x > velocity_x:
            velocity_x = delta_x
        self.canvas.move(self.cell_id, velocity_x, 0)
        self.canvas.move(self.text_id, velocity_x, 0)
        self.canvas.update()
        self.canvas.after(25, self.left, x, y, value)

    def right(self, x, y, value):
        if self.cell_id not in self.canvas.find_all():
            return
        new_x, new_y = _grid_to_topleft(x, y)
        curr_x, curr_y = tuple(self.canvas.coords(self.cell_id)[0:2])
        # Is the cell already there?
        if (new_x, new_y) == (curr_x, curr_y):
            self.canvas.itemconfigure(self.text_id, text=str(value))
            return
        delta_x, delta_y = new_x - curr_x, new_y - curr_y
        velocity_x = 75.0
        # Will the velocity overshoot it?
        if delta_x < velocity_x:
            velocity_x = delta_x
        self.canvas.move(self.cell_id, velocity_x, 0)
        self.canvas.move(self.text_id, velocity_x, 0)
        self.canvas.update()
        self.canvas.after(25, self.right, x, y, value)


class Graphics(Tk.Frame):

    def __init__(self, initial=None, master=None):
        Tk.Frame.__init__(self, master)
        self.grid()
        self.back_grid = Tk.Canvas(self, bg=GRID_COLOR, height=GRID_HEIGHT, width=GRID_WIDTH)
        self._cell_objs = {}  # Stores all taken cells
        self._create_widgets()  # Creates the blank cells
        self.update()
        self.back_grid.focus_set()  # Put canvas in focus so keys are recognized
        if initial:
            for y, row in enumerate(initial):
                for x, col in enumerate(row):
                    if col != '0':
                        self.new_cell(x, y, col)

    def _create_widgets(self):
        for cell in range(0, 16):
            x0_border_offset = GRID_WIDTH*.03*((cell % 4)+1)
            x0_cell_offset = CELL_WIDTH*(cell % 4)
            x0 = x0_border_offset+x0_cell_offset
            y0_border_offset = GRID_HEIGHT*.03*(cell/4+1)
            y0_cell_offset = CELL_HEIGHT*(cell/4)
            y0 = y0_border_offset+y0_cell_offset
            x1 = x0+CELL_WIDTH
            y1 = y0+CELL_HEIGHT
            self.back_grid.create_rectangle(x0, y0, x1, y1, fill=CELL_COLOR, width=0)
        self.back_grid.grid()

    def up(self, x1, y1, x2, y2, collide, value):
        print (x1, y1)
        if (x1, y1) != (x2, y2):
            self._cell_objs[x1, y1].up(x2, y2, value)  # Translate cell at that spot
            if collide:
                self._cell_objs[x2, y2].delete()
            self._cell_objs[x2, y2] = self._cell_objs[x1, y1]  # Put new placement cell in dictionary
            self._cell_objs[x1, y1] = None  # Free up old spot

    def down(self, x1, y1, x2, y2, collide, value):
        print (x1, y1)
        if (x1, y1) != (x2, y2):
            self._cell_objs[x1, y1].down(x2, y2, value)  # Translate cell at that spot
            if collide:
                self._cell_objs[x2, y2].delete()
            self._cell_objs[x2, y2] = self._cell_objs[x1, y1]  # Put new placement cell in dictionary
            self._cell_objs[x1, y1] = None  # Free up old spot

    def left(self, x1, y1, x2, y2, collide, value):
        print (x1, y1)
        if (x1, y1) != (x2, y2):
            self._cell_objs[x1, y1].left(x2, y2, value)  # Translate cell at that spot
            if collide:
                self._cell_objs[x2, y2].delete()
            self._cell_objs[x2, y2] = self._cell_objs[x1, y1]  # Put new placement cell in dictionary
            self._cell_objs[x1, y1] = None  # Free up old spot

    def right(self, x1, y1, x2, y2, collide, value):
        print (x1, y1)
        if (x1, y1) != (x2, y2):
            self._cell_objs[x1, y1].right(x2, y2, value)  # Translate cell at that spot
            if collide:
                self._cell_objs[x2, y2].delete()
            self._cell_objs[x2, y2] = self._cell_objs[x1, y1]  # Put new placement cell in dictionary
            self._cell_objs[x1, y1] = None  # Free up old spot

    def new_cell(self, x, y, value=None):
        # Check if index is within grid, should always be
        assert x < 4 and y < 4
        # Math to place object on canvas
        x0, y0 = _grid_to_topleft(x, y)
        x1 = x0 + CELL_WIDTH  # Calc bottom right coords of cell
        y1 = y0 + CELL_HEIGHT
        # Call Cell object constructor
        cell = _Cell(self.back_grid, (x0, y0, x1, y1), value)
        self._cell_objs[x, y] = cell
