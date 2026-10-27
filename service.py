import xbmc
import xbmcaddon
import xbmcvfs
import json
import shutil
import os

class UpdateMonitor(xbmc.Monitor):
    def __init__(self):
        super().__init__()
        
        self.addon = xbmcaddon.Addon()
        addon_path = xbmcvfs.translatePath(self.addon.getAddonInfo('path'))
        addons_dir = os.path.dirname(os.path.dirname(addon_path))
        
        self.src = os.path.join(addon_path, "resources", "Custom.xml")
        self.colors_dir = os.path.join(addons_dir, "skin.bald", "colors")
        self.dest = os.path.join(self.colors_dir, "Custom.xml")
        
        self.json_command = json.dumps({
            "jsonrpc": "2.0",
            "method": "Settings.SetSettingValue",
            "params": {"setting": "lookandfeel.skincolors", "value": "Custom"},
            "id": 1
        })

    def onNotification(self, sender, method, data):
        if method == 'GUI.OnSkinLoaded':
            current_skin = xbmc.getSkinDir()
            
            if current_skin == 'skin.bald':
                # If the file is missing, the skin was just installed or updated!
                if os.path.exists(self.src) and os.path.exists(self.colors_dir) and not os.path.exists(self.dest):
                    xbmc.log("service.skin.bald.monitor: Custom.xml missing, copying now...", xbmc.LOGDEBUG)
                    
                    shutil.copy2(self.src, self.dest)
                    
                    xbmc.executeJSONRPC(self.json_command)
                    xbmc.executebuiltin('ReloadSkin()')

if __name__ == '__main__':
    monitor = UpdateMonitor()
    while not monitor.abortRequested():
        if monitor.waitForAbort(1):
            break