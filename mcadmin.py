import click
import datetime
import os
import shutil
import psutil
from zipfile import ZipFile

# Globals
YES = ['yes', 'y']
NO = ['no', 'n']


# Create click group for subcommands
# - necessary for decorators to function properly
@click.group()
def cli():
    pass


@cli.command()
@click.option(
    '-b', 
    '--backup-path',
    'backup_path',
    type=click.Path(),
    default='/srv/backup/minecraft/',
    help='path to backup folder',
)
@click.option(
    '-s',
    '--server-path',
    'server_path',
    type=click.Path(exists=True),
    default='/srv/minecraft/',
    help='path to minecraft server',
)
def backup(backup_path, server_path):
    # Check if minecraft server directory exists 
    if not os.path.exists(server_path):
        click.echo(f"No minecraft server detected at '{server_path}'. Exiting...")
        return 1

    if not os.path.exists(backup_path):
        click.echo(f"No backup folder detected at '{backup_path}'. Creating...")
        os.mkdir(backup_path)

    # Create a timestamped filename for the backup
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_filename= f"{backup_path}{timestamp}.zip"

    # Create an archive of the minecraft server directory
    with ZipFile(backup_filename, 'w') as zip_file:
        os.chdir(server_path)
        # Traverse all files in directory
        for folder_name, sub_folders, filenames in os.walk(server_path):
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


@cli.command()
@click.option(
    '-b', 
    '--backup-path',
    'backup_path',
    type=click.Path(exists=True),
    default='/srv/backup/minecraft/',
    help='path to backup folder',
)
@click.option(
    '-s',
    '--server-path',
    'server_path',
    type=click.Path(exists=True),
    default='/srv/minecraft/',
    help='path to minecraft server',
)
def restore(backup_path, server_path):
    # Check if minecraft server directory exists 
    if not os.path.exists(server_path):
        click.echo(f"No minecraft server detected at '{server_path}'. Exiting...")
        return 1
    # Check if backup directory exists
    if not os.path.exists(backup_path):
        click.echo(f"No backup folder detected at '{backup_path}'.")
        return 1

    # show backup options, numbered
    backup_list = []
    for root, subdirs, filenames in os.walk(backup_path):
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
    confirm = input(f"BE CAREFUL! Restoring the minecraft server to a previous snapshot will PERMANENTLY DESTROY all data in '{server_path}' and replace it with the files in {snapshot}.\nContinue? (y/N): ")
    if confirm.lower() in NO or confirm == '':
        return 0

    # remove files in server_path
    try:
        print(f"Deleting {server_path}...")
        shutil.rmtree(server_path)
        print(f"Successfully deleted {server_path}...")
    except:
        print(f"Error deleting {server_path}... Try running as root.")
        return 1

    # extract snapshot to server_path
    archive_path = os.path.join(backup_path, snapshot)
    with ZipFile(archive_path, 'r') as archive:
        try:
            print(f"Restoring snapshot to {server_path}...")
            archive.extractall(server_path)
            print(f"Successfully restored snapshot.")
            return 0
        except:
            print(f"Error extracting archive {snapshot}... Try running as root.")
            return 1
    return 1


@cli.command()
def status():
    """Show basic stats about server

    - show if server is running
    # pseudocode 
    # running = ps aux | grep paper.jar
    # if running:
    #       running = True

    - test outbound connections
    - test incomming connections with curl/wget of small file
    
    """
    for proc in psutil.process_iter(['pid', 'name']):
        print(proc.info)
    pass


def start(server_path):
    pass


def stop():
    pass

if __name__ == "__main__":
    cli()