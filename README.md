# Cowsim

A simple cow pen simulator.

### Current Issues

> This is a hastily implemented cow pen simulator where it's main purpose is
> to demostrate software engineering practices, Python competency, and OOP concepts.
> The actual simulation runtime is currently buggy and results produced are flawed.

- Poor performance for large populations of cows
- Numerical data seems to rapidly converge to zero after about two iterations, which
  suggests that the algorithms (regarding feeding, reproduction, death, etc)
  probably need to be tweaked.
- CLI is probably needs better ergonomics and input validation.
- A separate module for analyzing data results would be helpful for understanding insights.
- There's probably other issues that I'm not aware of.

## Features
- Cow reproduction
- Cow death
- Caloric intake through food
- Caloric expenditure
- Cow age, weight, sex, and emotions
- Supported simulation environments:
  - Cow Pen
- Supported species:
  - Purple Angus (fictitious)

## Requirements
- Python 3.10 or greater
- Pip
- Docker (optional)

## Building

> Note: It is recommended to build and install `cowsim` in a virtual
> environment (e.g. venv, virtualenv, etc).

### Docker
If you have [Docker Compose](https://docs.docker.com/compose/install/)
installed on your system, you can generate the wheel file with the following
command:

```bash
docker compose run --rm dist
```

This will create a directory called `build/` where you can install the wheel
file using `pip`. Example:

```bash
pip install ./build/cowsim-0.1.0-py3-none-any.whl
```

### Local
If you do not have Docker installed, you can build the package locally. First
install the required `pip` packages:
```bash
> pip install --upgrade build setuptools
> python3 -m build --wheel --outdir=./build
> pip install ./build/cowsim-0.1.0-py3-none-any.whl
```

## Usage
You can see all options for running `cowsim` with the `--help` flag.
```bash
cowsim --help
```

To run a cow simulation with default values, simply run:
```bash
cowsim run
```
