import cv2
import math
import numpy as np
from copy import copy, deepcopy
from win32api import GetSystemMetrics


# radius of circles
RADIUS = 4
points_dict = {'background': []}
# Existing masks, BGR order
masks = {
    "background": {
        "min": [120, 208, 253],
        "max": [124, 208, 255]
    }
}


def draw_screen():
    """Draw the current state of the image with all points."""
    draw_all_points()


def select_point_color(key):
    """Select a color based on the key.
    Args:
        key (str): The key to select the color for.
    Returns:
        tuple: A tuple representing the BGR color.
    """
    # Black
    return (0, 0, 0)


def draw_all_points():
    """Draw all points stored in points_dict on the image."""
    global points_dict
    for key, pointlist in points_dict.items():
        color = select_point_color(key)
        for x, y in pointlist:
            cv2.circle(img, (x, y), RADIUS, color, -1)


def draw_point(x, y):
    """Draw a point on the image at the specified coordinates.
    Args:
        x (int): x-coordinate of the point.
        y (int): y-coordinate of the point.
    """
    color = select_point_color('background')
    cv2.circle(img, (x, y), RADIUS, color, -1)


def check_point_marked(x, y):
    """Check if the point is within the radius of any marked point.
    If it is, remove that point from the list.
    Args:
        x (int): x-coordinate of the mouse click.
        y (int): y-coordinate of the mouse click.
    """
    global points_dict
    for Px, Py in points_dict['background']:
        mouse_point_dist = math.sqrt((abs(Px-x) ** 2) + (abs(Py-y) ** 2))
        if mouse_point_dist <= RADIUS:
            # remove point.
            points_dict['background'].remove([Px, Py])
            return


def resize_img_to_screen_size(img):
    """Resize the image to fit the screen size.
    Args:
        img (numpy.ndarray): The image to resize.
    """
    # get screen size
    screen_width = GetSystemMetrics(0)
    screen_height = GetSystemMetrics(1)

    # get image size
    width = img.shape[1]
    height = img.shape[0]

    # scale image to maxsize:
    x_max_scale = screen_width / width
    # remove a few pixels for taskbar
    y_max_scale = (screen_height * 0.9) / height
    # percent of original size
    scale_percent = (100 * min(x_max_scale, y_max_scale))
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return img


def mark_mouse_coords(event, x, y, flags, param):
    """Handle mouse events to mark coordinates on the image.
    Args:
        event: The mouse event.
        x (int): x-coordinate of the mouse event.
        y (int): y-coordinate of the mouse event.
        flags: Any flags associated with the mouse event.
        param: Additional parameters (not used).
    """
    global mode, points_dict, img, origin_img
    # add point
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"color of point{y, x} is: {img[y, x]}")
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        print(f"HSV of selected point: {hsv[y, x]}")
        points_dict['background'].append([x, y])
        draw_point(x, y)
    # right button remove point
    elif event == cv2.EVENT_RBUTTONDOWN:
        check_point_marked(x, y)
        # clean image and redraw all points
        img = copy(origin_img)
        apply_existing_mask()
        mask_img()
        draw_screen()
    # update image
    cv2.imshow("image", img)


def mask_img():
    """Apply a mask to the image based on the selected points."""
    selected_colors = []
    for key, pointlist in points_dict.items():
        for x, y in pointlist:
            selected_colors.append(origin_img[y, x])
    np_array = np.array(selected_colors)
    min_values = np_array.min(axis=0)
    max_values = np_array.max(axis=0)
    mask = cv2.inRange(origin_img, min_values, max_values)
    img[mask != 0] = [255, 255, 255]
    print(f"masking values are min {min_values}, max: {max_values}")


def apply_existing_mask():
    """Apply existing masks to the image."""
    global img
    for key, mask in masks.items():
        mask = cv2.inRange(origin_img, np.array(mask['min']),
                           np.array(mask['max']))
        img[mask != 0] = [255, 255, 255]


if __name__ == '__main__':
    img = cv2.imread('images/ChatGPT Image.png')
    img = resize_img_to_screen_size(img)
    origin_img = deepcopy(img)

    apply_existing_mask()
    draw_screen()
    cv2.imshow("image", img)
    cv2.setMouseCallback('image', mark_mouse_coords)

    print('Chromakey test program')
    print('Press m to update the mask, escape to exit')
    while True:
        # int value of character
        pressedkey = cv2.waitKey(0)
        if pressedkey == ord('m'):
            apply_existing_mask()
            mask_img()
        # Wait for ESC key to exit
        elif pressedkey == 27:
            cv2.destroyAllWindows()
            break
