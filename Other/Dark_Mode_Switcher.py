import winreg

try:
    REG_PATH = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize"
    reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    key = winreg.OpenKey(reg, REG_PATH)
    previous = winreg.QueryValueEx(key, "AppsUseLightTheme")[0]
    now = 1 if previous == 0 else 0
    winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
    registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_WRITE)
    winreg.SetValueEx(registry_key, "AppsUseLightTheme", 0, winreg.REG_DWORD, now)
    winreg.CloseKey(registry_key)
    print("Registry added")
except Exception as bug:
    print(bug)
