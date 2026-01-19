import os
import webbrowser


def open_youtube():
    webbrowser.open("https://youtube.com")


def open_notepad():
    os.system("notepad")  # Windows


def open_calculator():
    os.system("calc")  # Windows


if __name__ == "__main__":
    print("Testing app launches...")

    print("Opening YouTube in the browser")
    open_youtube()

    input("Press ENTER to open Notepad...")
    open_notepad()

    input("Press ENTER to open Calculator...")
    open_calculator()

    print("Test finished")
