import pyautogui


def nav_to_image(image, clicks, off_x=0, off_y=0):
    '''give the image path at and the clicks as the default parameters
    this helps you to navigate the cursor and click that image if that image is present on the screen
    '''
    position = pyautogui.locateCenterOnScreen(image, confidence=.8)

    if position is None:
        print(f'{image} not Found..')
        return None
    else:
        pyautogui.moveTo(position, duration=.5)
        pyautogui.moveRel(off_x, off_y, duration=.2)
        pyautogui.click(clicks=clicks, interval=.1)
        return "yes"

