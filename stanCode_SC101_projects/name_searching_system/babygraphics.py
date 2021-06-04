"""
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.

YOUR DESCRIPTION HERE
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt'
]
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 500     # 原始為600，但會超過我的視窗~~所以調低
YEARS = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index of the current year in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                              with the specified year.
    """
    x = GRAPH_MARGIN_SIZE+((width-(GRAPH_MARGIN_SIZE*2))/len(YEARS))*year_index
    return x


def draw_fixed_lines(canvas):
    """
    Erases all existing information on the given canvas and then
    draws the fixed background lines on it.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.

    Returns:
        This function does not return any value.
    """
    canvas.delete('all')            # delete all existing lines from the canvas

    # Write your code below this line
    #################################

    canvas.create_line(GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE, CANVAS_WIDTH-GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE)
    canvas.create_line(GRAPH_MARGIN_SIZE, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, CANVAS_WIDTH - GRAPH_MARGIN_SIZE, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE)
    height = CANVAS_HEIGHT
    for i in range(len(YEARS)):
        x = get_x_coordinate(CANVAS_WIDTH, i)
        canvas.create_line(x, 0, x, height)
        canvas.create_text(x, (CANVAS_HEIGHT-GRAPH_MARGIN_SIZE), text=YEARS[i], anchor=tkinter.NW)


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid

    # Write your code below this line
    #################################
    y_height = (CANVAS_HEIGHT-GRAPH_MARGIN_SIZE*2)  # 圖表Y軸高度
    y_axis = GRAPH_MARGIN_SIZE      # 圖表上限Y軸高度(起始值)

    for i in range(len(lookup_names)):
        if lookup_names[i] in name_data:
            for j in range(len(YEARS)):                         # 查找年份排名，訂定y座標
                if str(YEARS[j]) in name_data[lookup_names[i]]:
                    rank = int(name_data[lookup_names[i]][str(YEARS[j])])
                    y1 = y_axis + ((y_height / 1000) * rank)
                else:
                    y1 = CANVAS_HEIGHT-GRAPH_MARGIN_SIZE        # 如果沒有排名資訊，y座標訂定為最底限
                    rank = '*'
                x1 = get_x_coordinate(CANVAS_WIDTH, j)
                if j == 0:
                    y0 = y1
                    x0 = x1
                    canvas.create_text(x1+TEXT_DX, y1, text=(lookup_names[i], str(rank)), anchor=tkinter.SW, fill=COLORS[i % 3])
                    continue
                canvas.create_line(x0, y0, x1, y1, fill=COLORS[i % 3], width=LINE_WIDTH)
                canvas.create_text(x1+TEXT_DX, y1, text=(lookup_names[i], str(rank)), anchor=tkinter.SW, fill=COLORS[i % 3])
                y0 = y1
                x0 = x1


# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
