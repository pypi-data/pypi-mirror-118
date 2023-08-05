A simple script to wait for Docker daemon to be active.

## Installation

```bash
python3 -m pip install wait-for-docker
```

## Usage

```bash
wait-for-docker && command_which_uses_docker
```

The command wait until Docker daemon gets active. There's no configuration.
