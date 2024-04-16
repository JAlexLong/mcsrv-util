# minecraftctl

Minecraft Server Utility

**minecraftctl** is a cli application that automates several tasks such as creating server backups and restoring from backups should something go wrong. This will be expanded to creating a server from scratch, as well as being a way to handle plugins.

## Installation

1. Create a Python virtual environment

```sh
$ python -m venv ./venv
$ source venv/bin/activate
(venv) $
```

2. Install minecraftctl in editable mode

```sh
(venv) $ python -m pip install -e .
```

## Run the Project

```sh
(venv) $ minecraftctl backup
Success!
```

## Features

minecraftctl currently provides the following options:

- `backup` compresses files from `/var/minecraft/` and stores the archive in `/var/minecraft/backups/`.

## About the Author

John Alexander Long II - Email: johnalexanderlong@gmail.com

## License

Distributed under the GPLv3 license. See `LICENSE` in the root directory of this repo for more information.
