import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib as matplotlib

def load_image(path):
    """
    Load an image using matplotlib and return as numpy array.
    :param path: The file path of the image to load
    :return: A numpy array with image[y,x,band]
    """
    return mpimg.imread(path)


def pick_single( image, n=-1, width=15, backend='TkAgg', ticks=False, line=False, **kwds ):
    """
    Pick a list of points on an individual image. Enter will return value, cancel will restart and closing window
    will return an empty list of picked points. Right click to undo last operation.

    :param image: The image to pick on (string path or numpy array).
    :param n: The number of points to pick. -1 (defaults) allows unlimited points.
    :param width: The width of the plot to create.
    :param backend: The matplotlib backend to use. Set to None to use currently active backend.
    :param ticks: True if axes ticks should be displayed. Default is False.
    :param line: True if a line should be drawn between successively picked points.
    :keyword : Keywords are passed to plt.imshow.
    :return: A list of tuples containing each (x,y) picked.
    """

    if isinstance(image, str):
        image = load_image(image)

    # set backend
    if backend is not None:
        matplotlib.use(backend)

    aspx = image.shape[0] / image.shape[1]

    # setup figure
    fig,ax = plt.subplots(1,1, figsize=(width,width*aspx))
    ax.imshow( image, **kwds )
    if not ticks:
        ax.set_xticks([])
        ax.set_yticks([])

    # setup callback
    points = []
    redo = [False]
    def onclick(event):
        if n != -1 and len(points) >= n:
            plt.close(event.canvas.figure) # done!
            return

        points.append( (event.xdata, event.ydata) )
        ax.scatter( event.xdata, event.ydata, marker='o' )
        if line and len(points) > 1:
            x0,y0 = points[-1]
            x1,y1 = points[-2]
            ax.plot( [x0,x1], [y0,y1], color='k' )
        plt.draw()
    def onkey(event):
        if event.key == 'escape':
            points.clear()
            redo[0] = True # relaunch once thread is unblocked
            plt.close(event.canvas.figure)
        elif event.key == 'enter':
            plt.close(event.canvas.figure)

    fig.canvas.mpl_connect('button_press_event', onclick )
    fig.canvas.mpl_connect('key_press_event', onkey )
    fig.tight_layout()
    plt.show() # block until finished picking

    if len(points) == 0 and redo[0]:
        return pick_single( image, n, width, backend, ticks, line, **kwds )
    return points

def pick_multi( image1, image2, n=-1, width=15, backend='TkAgg', ticks=False, line=False, **kwds ):
    """
    Pick a list of points on two images. Enter will return value, cancel will restart and closing window
    will return an empty list of picked points. Right click to undo last operation.

    :param image1: the first image to pick (string path or numpy array).
    :param image2: the second image to pick (string path or numpy array).
    :param n: The number of points to pick. -1 (defaults) allows unlimited points.
    :param width: The width of the plot to create.
    :param backend: The matplotlib backend to use. Set to None to use currently active backend.
    :param ticks: True if axes ticks should be displayed. Default is False.
    :param line: True if a line should be drawn between successively picked points.
    :keyword : Keywords are passed to plt.imshow for each image.
    :return:
    """

    if isinstance(image1, str):
        image1 = load_image(image1)
    if isinstance(image2, str):
        image2 = load_image(image2)

    # set backend
    if backend is not None:
        matplotlib.use(backend)

    aspx = image1.shape[0] / image1.shape[1]

    # setup figure
    fig,ax = plt.subplots(2,1, figsize=(width,width*aspx))
    ax[0].imshow( image1, **kwds )
    ax[1].imshow( image2, **kwds )
    if not ticks:
        for a in ax:
            a.set_xticks([])
            a.set_yticks([])

    # setup callback
    points_1 = []
    points_2 = []
    redo = [False]
    def onclick(event):
        if n != -1 and len(points_1) >= n and len(points_2) >= n: # done!
            plt.close(event.canvas.figure)
            return
        if event.inaxes is ax[0]:
            if n== -1 or len(points_1) < n:
                points_1.append( (event.xdata, event.ydata) )
                ax[0].scatter( event.xdata, event.ydata, marker='o' )
                if line and len(points_1) > 1:
                    x0, y0 = points_1[-1]
                    x1, y1 = points_1[-2]
                    ax[0].plot([x0, x1], [y0, y1], color='k')
        elif event.inaxes is ax[1]:
            if n == -1 or len(points_2) < n:
                points_2.append((event.xdata, event.ydata))
                ax[1].scatter(event.xdata, event.ydata, marker='o')
                if line and len(points_2) > 1:
                    x0, y0 = points_2[-1]
                    x1, y1 = points_2[-2]
                    ax[1].plot([x0, x1], [y0, y1], color='k')
        plt.draw()

    def onkey(event):
        if event.key == 'escape':
            points_1.clear()
            points_2.clear()
            redo[0] = True # relaunch once thread is unblocked
            plt.close(event.canvas.figure)
        elif event.key == 'enter':
            plt.close(event.canvas.figure)

    fig.canvas.mpl_connect('button_press_event', onclick )
    fig.canvas.mpl_connect('key_press_event', onkey )
    fig.tight_layout()
    plt.show() # block until finished picking
    if (len(points_1) == 0 or len(points_2) == 0) and redo[0]:
        return pick_multi( image1, image2, n, width, backend, ticks, line, **kwds )
    return points_1, points_2

def save_points( out, path1, points1, path2=None, points2=None):
    """
    Save points to a text file.
    :param out: Path of the output file to write
    :param path1: Path of the first image, or None to omit.
    :param points1: Points picked in first image.
    :param path2: Path of second image, or None to omit.
    :param points2: Points picked from the second image, or None.
    :returns : the number of points or point-pairs written to the file.
    """
    n = 0
    if out is not None:
        with open(out, 'w') as f:
            if points1 is not None and points2 is None:  # single-image mode
                if path1 is not None:
                    f.write(path1 + '\n')
                for px, py in points1:
                    f.write('%f,%f\n' % (px, py))
                    n += 1
            elif points1 is not None and points2 is not None:  # multi-image mode
                if path1 is not None and path2 is not None:
                    f.write(path1 + '\n')
                    f.write(path2 + '\n')
                for _p1, _p2 in zip(points1, points2):
                    f.write('%f,%f,    %f,%f\n' % (_p1[0], _p1[1], _p2[0], _p2[1]))
                    n += 1
    return n

def launch_gui( n = -1 ):
    """
    Launch GUI application.

    :param n: The number of points to pick. -1 (defaults) allows unlimited points.
    """

    import easygui

    file1 = easygui.fileopenbox(msg="Choose a file")
    file2 = easygui.fileopenbox(msg="Choose a second file (or cancel to work with single image)")

    P1, P2 = None, None
    if file2 is None and file1 is not None:
        P1 = pick_single(file1, n=n)
    elif file2 is not None and file1 is not None:
        P1, P2 = pick_multi(file1, file2, n=n)
    else:
        return # cancel

    out = easygui.filesavebox(msg="Choose output")
    n = save_points( out, file1, P1, file2, P2 )

    if easygui.ynbox("Saved %d points to %s. Would you like to re-launch?" % (n, out), "Process a new file?", ):
        launch_gui() # recurse

# launch in gui mode
if __name__ == '__main__':
    launch_gui()




