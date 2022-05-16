import pyautogui

def controls(message):
  while True:
    message = message.lower()
    if message == "up":
      pyautogui.keyDown("up")
      pyautogui.keyUp("up")
    elif message == "down":
      pyautogui.keyDown("down")
      pyautogui.keyUp("down")
    elif message == "left":
      pyautogui.keyDown("left")
      pyautogui.keyUp("left")
    elif message == "right":
      pyautogui.keyDown("right")
      pyautogui.keyUp("right")
    elif message == "a":
      pyautogui.keyDown("s")
      pyautogui.keyUp("s")
    elif message == "b":
      pyautogui.keyDown("a")
      pyautogui.keyUp("a")
    elif message == "start":
      pyautogui.keyDown("enter")
      pyautogui.keyUp("enter")