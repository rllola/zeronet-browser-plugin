import sys
import os
import subprocess

from Plugin import PluginManager
from Translate import translate as _
from util.Flag import flag
from Config import config
from Site import SiteManager

@PluginManager.registerTo("UiWebsocket")
class UiWebsocketPlugin(object):

    @flag.admin
    @flag.no_multiuser
    def actionServerUpdate(self, to):
        def cbServerUpdate(res):
            self.response(to, res)
            if not res:
                return False
            for websocket in self.server.websockets:
                websocket.cmd(
                    "notification",
                    ["info", _["Close the browser to finish updating ZeroNet core."], 20000]
                )
                #websocket.cmd("updating")

            import main
            main.update_after_shutdown = True

            if not sys.platform.startswith("linux"):
                SiteManager.site_manager.save()
                main.file_server.stop()
                main.ui_server.stop()

        if os.access(os.getcwd(), os.W_OK):
            self.cmd(
                "confirm",
                [_["Update <b>ZeroNet client</b> to latest version?"], _["Update"]],
                cbServerUpdate
            )

        else:
            self.cmd(
                "notification",
                ["info", _["You don't seem to have the required permissions to do the update <br/> You fix this by adding the current user to the zeronet-browser group <br/> <b>sudo usermod -a -G zeronet-browser $USER</b> "]]
            )
