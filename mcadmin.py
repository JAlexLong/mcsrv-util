import click
import datetime
import os
import tarfile

@click.group()
def cli():
    pass

@cli.command()
@click.option(
    '-d', 
    '--destination',
    type=click.Path(),
    default='/srv/minecraft/backup/',
    help='path to backup folder',
)
@click.option(
    '-s',
    '--server',
    type=click.Path(exists=True),
    default='/srv/minecraft/',
    help='path to minecraft server',
)
def backup(destination, server):
    # Check if minecraft server directory exists 
    if not os.path.exists(server):
        click.echo(f"No minecraft server detected at '{server}'. Exiting...")
        return 1
    
    if not os.path.exists(destination):
        click.echo(f"No backup folder detected at '{destination}'. Creating...")
        os.mkdir(destination)

    # Create a timestamped filename for the backup
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = f"{destination}{timestamp}.tar.gz"

    # Create a tar archive of the minecraft server directory
    with tarfile.open(backup_file, "w:gz") as tar:
        os.chdir(server)
        tar.add("./")
    click.echo(f"Minecraft server backup saved to '{backup_file}'")
    return 0

if __name__ == "__main__":
    cli()