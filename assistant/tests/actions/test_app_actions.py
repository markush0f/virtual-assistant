from assistant.core.executor.actions.app_actions import open_app, close_app
import time


def test_open_app():
    assert open_app("Notepad") == "Opened Notepad"
    assert open_app("") == "No app specified."


def test_close_app():
    assert close_app("Notepad") == "Closed Notepad"
    assert close_app("") == "No app specified."


def check_open_app_and_close_app():
    open_app_result = open_app("notepad")
    print(open_app_result)
    time.sleep(10)
    close_app_result = close_app("notepad")
    print(close_app_result)


check_open_app_and_close_app()
