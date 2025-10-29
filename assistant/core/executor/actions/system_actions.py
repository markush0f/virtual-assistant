from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyautogui
from assistant.actions_registry import register_action


def get_volume_interface():
    """Get system master volume interface safely (compatible with all Windows versions)."""
    try:
        # Get the enumerator directly
        enumerator = AudioUtilities.GetDeviceEnumerator()
        # eRender = 0, eCapture = 1, eAll = 2
        # eMultimedia = 1, eCommunications = 2
        device = enumerator.GetDefaultAudioEndpoint(0, 1)  # eRender, eMultimedia
        interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        return cast(interface, POINTER(IAudioEndpointVolume))
    except Exception as e:
        print(f"⚠️ Error getting volume interface: {e}")
        return None

@register_action(description="Decrease system volume by 10%")
def volume_up(increment=0.1):
    volume = get_volume_interface()
    if not volume:
        print("Could not access system volume.")
        return
    current = volume.GetMasterVolumeLevelScalar()
    new_volume = min(1.0, current + increment)
    volume.SetMasterVolumeLevelScalar(new_volume, None)
    print(f"🔊 Volume increased to {int(new_volume * 100)}%")


@register_action(description="Decrease system volume by 10%")
def volume_down(decrement=0.1):
    """Decrease system volume by a given step (0.0 to 1.0)."""
    volume = get_volume_interface()
    if not volume:
        print("Could not access system volume.")
        return
    current = volume.GetMasterVolumeLevelScalar()
    new_volume = max(0.0, current - decrement)
    volume.SetMasterVolumeLevelScalar(new_volume, None)
    print(f"Volume decreased to {new_volume:.2f}")


@register_action(description="Toggle mute or unmute system sound")
def mute_toggle():
    """Toggle mute/unmute."""
    volume = get_volume_interface()
    is_muted = volume.GetMute()
    volume.SetMute(not is_muted, None)
    print("Muted" if not is_muted else "🔊 Unmuted")


@register_action(description="Unmute the system volume")
def unmute():
    """Unmute the system volume."""
    volume = get_volume_interface()
    volume.SetMute(0, None)
    print("🔊 System unmuted")


@register_action(description="Take a screenshot and save it as screenshot.png")
def take_screenshot(filename="screenshot.png"):
    """Take a screenshot and save it."""
    img = pyautogui.screenshot()
    img.save(filename)
    print(f"📸 Screenshot saved as {filename}")
