import winreg


def set_reg(name, value):
    try:
        REG_PATH = r"Control Panel\Desktop"
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(registry_key)
        print("Wallpaper registry added")
    except Exception as bug:
        print(bug)
