from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyautogui


def get_volume_interface():
    """Get system master volume interface."""
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))


def volume_up(increment=0.1):
    """Increase system volume by a given step (0.0 to 1.0)."""
    volume = get_volume_interface()
    current = volume.GetMasterVolumeLevelScalar()
    new_volume = min(1.0, current + increment)
    volume.SetMasterVolumeLevelScalar(new_volume, None)


def volume_down(decrement=0.1):
    """Decrease system volume by a given step (0.0 to 1.0)."""
    volume = get_volume_interface()
    current = volume.GetMasterVolumeLevelScalar()
    new_volume = max(0.0, current - decrement)
    volume.SetMasterVolumeLevelScalar(new_volume, None)


def mute_toggle():
    """Toggle mute/unmute."""
    volume = get_volume_interface()
    is_muted = volume.GetMute()
    volume.SetMute(not is_muted, None)


def unmute():
    """Unmute the system volume."""
    volume = get_volume_interface()
    volume.SetMute(0, None)


def take_screenshot(filename="screenshot.png"):
    """Take a screenshot and save it."""
    img = pyautogui.screenshot()
    img.save(filename)
    print(f"📸 Screenshot saved as {filename}")


