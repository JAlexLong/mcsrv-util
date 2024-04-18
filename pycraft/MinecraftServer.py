import json
import os
import subprocess
from requests import get


class MinecraftServer:
    def __init__(self, version:str='latest') -> None:
        self.name = "server.jar"
        self.version = version if version != 'latest' else self._get_latest_version()
        # if no config exists
            # gen_config()
                # vanilla or paper?
                # amount of resources to dedicate? (1GB, 2GB, 4GB, 8Gb, etc.)
        # else
            # load_config()

    def load_config(self):
        pass

    def _get_latest_version(self) -> str:
        """Finds the latest version of minecraft servers from Mojang

        Returns:
            str: The latest stable release version (i.e. '1.20.4')
        """
        self._update_version_manifest()
        with open("version_manifest.json", "r") as version_manifest:
            version_data = json.load(version_manifest)
            latest_version_id = version_data['latest']['release']
        return latest_version_id

    def _update_version_manifest(self) -> None:
        version_manifest_url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
        response = get(version_manifest_url)
        data = response.json()
        with open("version_manifest.json", "w") as f:
            json.dump(data, f, sort_keys = True, indent = 4,
                      ensure_ascii=False)

    def _download_server_jar(self) -> bool:
        """Find proper download link from version_manifest.json and
        download it from the official Mojang servers.

        Returns:
            int: Returns 0 if server.jar downloaded successfully, 1 if
            the download failed.
        """
        version_url = ''
        with open("version_manifest.json", "r") as version_manifest:
            data = json.load(version_manifest)
            versions = data['versions']
            for v in versions:
                if self.version == v['id']:
                    version_url = v['url']
        if not version_url:
            return False

        # get the actual download link from the version's json file
        with open("server.jar", "wb") as server_jar:
            response = get(version_url).json()
            server_jar_url = response['downloads']['server']['url']

            print('Downloading server.jar..')
            server_jar_data = get(server_jar_url).content
            server_jar.write(server_jar_data)
            print("Successfully downloaded server.jar.")
            return True

    def start(self) -> None:
        print("Starting server...")
        self._download_server_jar()
        # check if server.jar exists in server location
        # download correct version of server otherwise
        # accept EULA
        process = subprocess.Popen(["java", "-Xmx1024M", "-Xms1024M", "-jar", "server.jar", "nogui"])