import json
from requests import get

class MinecraftServer:
    def __init__(self, version:str='latest') -> None:
        self.version = version if version != 'latest' else self._get_latest_version()
        # if no config exists
            # gen_config()
                # vanilla or paper?
                # amount of resources to dedicate? (1GB, 2GB, 4GB, 8Gb, etc.)
        # else
            # load_config()

    def _get_latest_version(self) -> str:
        self._update_version_manifest()
        with open("version_manifest.json", "r") as version_manifest:
            data = json.load(version_manifest)
            version = data['latest']['release']
        return version

    def _update_version_manifest(self) -> None:
        version_manifest_url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
        response = get(version_manifest_url)
        data = response.json()
        with open("version_manifest.json", "w") as f:
            json.dump(data, f, sort_keys = True, indent = 4,
                      ensure_ascii=False)

    def _download_server_jar(self) -> None:
        # check if version_manifest.json already exists
        version_url = ''
        with open("version_manifest.json", "r") as version_manifest:
            data = json.load(version_manifest)
            versions = data['versions']
            for v in versions:
                if self.version == v['id']:
                    version_url = v['url']
        if not version_url:
            return 1
        # get the actual download link from the version's json file
        response = get(version_url).json()
        server_jar_url = response['downloads']['server']['url']
        print('Downloading server.jar..')
        server_jar_data = get(server_jar_url).content
        with open("server.jar", "wb") as server_jar:
            server_jar.write(server_jar_data)

    def start(self) -> None:
        # check if server.jar exists in server location
        # download correct version of server otherwise
        print("Starting server...")
        #self._download_server_jar()
