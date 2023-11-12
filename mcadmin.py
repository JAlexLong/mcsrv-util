import click
import datetime
import os
import psutil
import shutil
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
    default='/var/lib/mcadmin/backups/',
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
def backup(backup_path: str, server_path: str) -> bool:
    backup_success = False
    # Check if minecraft server directory exists 
    if not os.path.exists(server_path):
        click.echo(f"No minecraft server detected at '{server_path}'. Exiting...")
        return backup_success

    if not os.path.exists(backup_path):
        click.echo(f"No backup folder detected at '{backup_path}'. ")
        try:
            os.mkdir(backup_path)
            # os.chown(backup_path, gid=gid) # find out how to get uid of current user
        except PermissionError:
            click.echo("Permission denied. Try again as root...")
            return backup_success

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
        return True
    else:
        click.echo(f"Minecraft server backup failed...")
        return False


@cli.command()
@click.option(
    '-b', 
    '--backup-path',
    'backup_path',
    type=click.Path(exists=True),
    default='/var/lib/mcadmin/backups/',
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
def restore(backup_path: str, server_path: str) -> bool:
    """Restores server from a previous snapshot archive.

    Args:
        backup_path (str): the path to the backups directory
        server_path (str): the path to the server directory

    Returns:
        bool: True if restoration is successful, False otherwise
    """
    # Check if minecraft server directory exists 
    if not os.path.exists(server_path):
        click.echo(f"No minecraft server detected at '{server_path}'. Exiting...")
        return False

    # Check if backup directory exists
    if not os.path.exists(backup_path):
        click.echo(f"No backup folder detected at '{backup_path}'.")
        return False

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
            click.echo(f"{i+1}) {archive}") 
        selection = input("\nWhich snapshot would you like to restore from?\nEnter 'q' to quit.\n> ")
        if selection.lower() in 'q':
            return 0

        # validate user input
        try:
            selection = int(selection)
            if selection-1 in range(len(backup_list)):
                click.echo(f"{selection}) {backup_list[selection-1]}")
                snapshot = backup_list[selection-1]
                selecting = False
            else:
                click.echo(f"Invalid selection '{selection}'.\n")
        except ValueError:
            click.echo(f"Invalid selection '{selection}'.\n")

    # confirm selection with warning of server destruction
    confirm = input(f"BE CAREFUL! Restoring the minecraft server to a previous snapshot will PERMANENTLY DESTROY all data in '{server_path}' and replace it with the files in {snapshot}.\nContinue? (y/N): ")
    if confirm.lower() in NO or confirm == '':
        return False
    
    restore = False

    # remove files in server_path
    try:
        click.echo(f"Deleting {server_path}...")
        shutil.rmtree(server_path)
        click.echo(f"Successfully deleted all files in {server_path}...")
    except PermissionError:
        click.echo(f"Error deleting {server_path}... Try running as root.")
        return restore

    # extract snapshot to server_path
    archive_path = os.path.join(backup_path, snapshot)
    with ZipFile(archive_path, 'r') as archive:
        try:
            click.echo(f"Restoring snapshot to {server_path}...")
            archive.extractall(server_path)
            os.chown(server_path, gid=944)
            restore = True
        except Exception as e:
            click.echo(f"Error extracting archive {snapshot}... Try running as root.")
            click.echo(e)

    if restore:
        click.echo(f"Successfully restored snapshot.")

    return restore


@cli.command()
@click.option(
    '-s',
    '--server-path',
    'server_path',
    type=click.Path(exists=True),
    default='/srv/minecraft/',
    help='path to minecraft server',
)
def status(server_path: str) -> bool:
    """Check running status of the server and its connection to the internet.

    Args:
        server_path (str): the path to the server

    Returns:
        bool: Returns True if both server process is running and external connections work.
    """
    # Find server process and report its status
    running = False
    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'status']):
        try:
            pinfo = proc.as_dict()
            if pinfo['name'] == 'java' and 'paper.jar' in pinfo['cmdline']:
                # Print the server information
                click.echo(f"Minecraft server process status:")
                click.echo(f"PID: {pinfo['pid']}")
                click.echo(f"Name: {pinfo['name']}")
                click.echo(f"Status: {pinfo['status']}")
                click.echo(f"Username: {pinfo['username']}")
                running = True
        except:
            pass

    if not running:
        click.echo("Minecraft server process status:")
        click.echo("PID: Not Found")
        click.echo("Name: Not Found")
        click.echo("Status: Not Found")

    return running

def start(server_path):
    pass


def stop():
    pass

if __name__ == "__main__":
    cli()