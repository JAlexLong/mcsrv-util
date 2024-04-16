class MinecraftServer:
    def __init__(self, version=None):
        if not version:
            # default to latest version
            self.get_latest_version()
            pass
    
    def get_latest_version(self):
        pass