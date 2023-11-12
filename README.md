# mcadmin

Minecraft Server Utility

**mcadmin** is a cli application that automates several tasks such as creating server backups and restoring from backups should something go wrong. This will be expanded to downloading, customizing, and administrating your server, as well as list information about your plugins.

## Installation

1. Create a Python virtual environment

```sh
$ python -m venv ./venv
$ source venv/bin/activate
(venv) $
```

2. Install mcadmin in editable mode

```sh
(venv) $ python -m pip install -e .
```

## Run the Project

```sh
(venv) $ mcadmin backup
Success!
```

## Features

mcadmin currently provides the following options:

- `backup` compresses files from `/srv/minecraft/` and stores the zip file in `/var/lib/mcadmin/backup/`.
- `restore` extracts files from a backup snapshot by searching for zip files in `/var/lib/mcadmin/backup`.
- `status` shows the running status of the server and it's corresponding pid.

## About the Author

J. Alex Long - Email: johnalexanderlong@gmail.com

## License

Distributed under the GPLv3 license. See `LICENSE` in the root directory of this repo for more information.
