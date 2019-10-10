import sys
import os

from Plugin import PluginManager
from Translate import translate as _
from util.Flag import flag


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
            #SiteManager.site_manager.save()
            #main.file_server.stop()
            #main.ui_server.stop()

        self.cmd(
            "confirm",
            [_["Update <b>ZeroNet client</b> to latest version?"], _["Update"]],
            cbServerUpdate
        )
