import click
import datetime

import MinecraftServer


# Create click group for subcommands
# - necessary for decorators to function properly
@click.group()
def cli():
    pass


if __name__ == "__main__":
    cli()