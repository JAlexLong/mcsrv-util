import click
import datetime
import json
import os
import shutil

from requests import get
from zipfile import ZipFile

class MinecraftServer:
    def __init__(self, version:str='latest'):
        if version == 'latest':
            self.version = self._get_latest_mc_version()
        else:
            self.version = version
        self.server_path = "/var/minecraft/"
        self.backup_path = "/var/minecraft/backups"
        # if no config exists
            # gen_config()
                # vanilla or paper?
                # amount of resources to dedicate? (1GB, 2GB, 4GB, 8Gb, etc.)
        # else
            # load_config()
        self._start_server()

    def _generate_config(self):
        pass

    def _load_config(self):
        pass

    def _update_version_manifest(self):
        version_manifest_url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
        response = get(version_manifest_url)
        data = response.json()
        with open("version_manifest.json", "w") as f:
            json.dump(data, f, ensure_ascii=False)
            #latest_release = data['latest']['release']

    def _download_server_jar(self):
        try:
            with open("version_manifest.json", "r") as version_manifest:
                server_jar_url = version_manifest.read()
                print(server_jar_url)
        except:
            print("ERROR!!1")

    def _start_server(self):
        self._download_server_jar()
        pass

    def _backup(self):
        # Check if minecraft server directory exists
        if not os.path.exists(self.server_path):
            click.echo(f"No minecraft server detected at '{self.server_path}'. Exiting...")
            return 1

        if not os.path.exists(self.backup_path):
            click.echo(f"No backup folder detected at '{self.backup_path}'. Creating...")
            os.mkdir(self.backup_path)

        # Create a timestamped filename for the backup
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_filename= f"{self.backup_path}{timestamp}.zip"

        # Create an archive of the minecraft server directory
        with ZipFile(backup_filename, 'w') as zip_file:
            os.chdir(self.server_path)
            # Traverse all files in directory
            for folder_name, sub_folders, filenames in os.walk(self.server_path):
                for filename in filenames:
                    # Create filepath of files in directory
                    file_path = os.path.join(folder_name, filename)
                    # Add files to zip file
                    zip_file.write(file_path, os.path.basename(file_path))

        # Check if the file exists in the backup directory
        if os.path.exists(backup_filename):
            click.echo(f"Minecraft server backup saved to '{backup_filename}'")
            return 0
        else:
            click.echo(f"Minecraft server backup failed...")
            return 1

    def _restore(self):
        # Check if minecraft server directory exists
        if not os.path.exists(self.server_path):
            click.echo(f"No minecraft server detected at '{self.server_path}'. Exiting...")
            return 1
        # Check if backup directory exists
        if not os.path.exists(self.backup_path):
            click.echo(f"No backup folder detected at '{self.backup_path}'.")
            return 1

        # show backup options, numbered
        backup_list = []
        for root, subdirs, filenames in os.walk(self.backup_path):
            # FEATURE: add subdir traversing with -r option
            for filename in filenames:
                if filename.lower().endswith('.zip'):
                    backup_list.append(filename)

        # prompt user for selection
        selecting = True
        while selecting:
            for i, archive in enumerate(backup_list):
                print(f"{i+1}) {archive}")
            selection = input("\nWhich snapshot would you like to restore from?\nEnter 'q' to quit.\n> ")
            if selection.lower() in 'q':
                return 0

            # validate user input
            try:
                selection = int(selection)
                if selection-1 in range(len(backup_list)):
                    print(f"{selection}) {backup_list[selection-1]}")
                    snapshot = backup_list[selection-1]
                    selecting = False
                else:
                    print(f"Invalid selection '{selection}'.\n")
            except ValueError:
                print(f"Invalid selection '{selection}'.\n")

        # confirm selection with warning of server destruction
        confirm = input(f"BE CAREFUL! Restoring the minecraft server to a previous snapshot will PERMANENTLY DESTROY all data in '{self.server_path}' and replace it with the files in {snapshot}.\nContinue? (y/N): ")
        if confirm.lower() in NO or confirm == '':
            return 0

        # remove files in server_path
        try:
            print(f"Deleting {self.server_path}...")
            shutil.rmtree(self.server_path)
            print(f"Successfully deleted {self.server_path}...")
        except:
            print(f"Error deleting {self.server_path}... Try running as root.")
            return 1

        # extract snapshot to server_path
        archive_path = os.path.join(self.backup_path, snapshot)
        with ZipFile(archive_path, 'r') as archive:
            try:
                print(f"Restoring snapshot to {self.server_path}...")
                archive.extractall(self.server_path)
                print(f"Successfully restored snapshot.")
                return 0
            except:
                print(f"Error extracting archive {snapshot}... Try running as root.")
                return 1

    def _status(self):
        """Show basic stats about server

        - show if server is running
        # pseudocode
        # running = ps aux | grep paper.jar
        # if running:
        #       running = True

        - test outbound connections
        - test incoming connections with curl/wget of small file

        """
        pass



server = MinecraftServer()