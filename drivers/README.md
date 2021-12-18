# A.L.F.R.E.D. Drivers

Drivers interface the various hardware used within A.L.F.R.E.D. with the application space. They are self-contained applications, running in the background of a Docker container, and exchange data via Redis

## Usage

Cookiecutter is recommended for creating a new driver. You can install Cookiecutter via pip or pipx (recommended).

To create a new driver without Cookiecutter, copy the `{{ cookiecutter.device_name }}` folder into the `drivers` (next to the other drivers) and replace all instances of `{{ cookiecutter.device_name }}` with your device name.

To create a new driver with Cookiecutter installed with pip, `cd` into the drivers directory (next to the other dirvers) and run:

```bash
cookiecutter ../template
```

and give the device name when prompted. It will replace all instances of `{{ cookiecutter.device_name }}` automatically.

To create a new driver with Cookiecutter installed with pipx, `cd` into the drivers directory (next to the other dirvers) and run:

```bash
pipx run cookiecutter ../template
```

and give the device name when prompted. It will replace all instances of `{{ cookiecutter.device_name }}` automatically.

## Specification

Drivers MUST procure data from hardware and produce such data to a Redis PubSub topic.

Drivers SHOULD implement an automatic loop to get data from the device (Data Producer). They CAN implement a way to send commands to the device to control it (Command Getters).

Nomenclature for the topic name is:

- `device-data-<device_name>` for data producers.

- `device-command--<device_name>` for command getters.
