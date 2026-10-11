import xbmc
import xbmcaddon
import xbmcvfs
import json
import shutil
import os

class UpdateMonitor(xbmc.Monitor):
    def __init__(self):
        super().__init__()
        
        addon = xbmcaddon.Addon()
        # Use xbmcvfs.translatePath instead of xbmc.translatePath
        addon_path = xbmcvfs.translatePath(addon.getAddonInfo('path'))
        addons_dir = os.path.dirname(addon_path)
        
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
        if method in ['System.OnAddonUpdate', 'System.OnAddonInstalled']:
            try:
                payload = json.loads(data)
                if payload.get('id') == 'skin.bald':
                    xbmc.log(f"service.skin.bald.monitor: Detected {method} for skin.bald", xbmc.LOGDEBUG)
                    
                    if os.path.exists(self.src) and os.path.exists(self.colors_dir):
                        shutil.copy2(self.src, self.dest)
                        xbmc.log("service.skin.bald.monitor: Copied Custom.xml successfully", xbmc.LOGDEBUG)
                    
                    xbmc.executeJSONRPC(self.json_command)
                    
            except Exception as e:
                xbmc.log(f"service.skin.bald.monitor Error: {e}", xbmc.LOGERROR)

if __name__ == '__main__':
    monitor = UpdateMonitor()
    while not monitor.abortRequested():
        if monitor.waitForAbort(1):
            break