# Garlic Butter

[![Build Container](https://github.com/soup-bowl/garlic-butter/actions/workflows/build.yml/badge.svg)](https://github.com/soup-bowl/garlic-butter/actions/workflows/build.yml)
[![CodeFactor](https://www.codefactor.io/repository/github/soup-bowl/garlic-butter/badge)](https://www.codefactor.io/repository/github/soup-bowl/garlic-butter)

![Pokemon - Yellow Version - Special Pikachu Edition](https://github.com/soup-bowl/garlic-butter/assets/11209477/d83f8a6f-1d6c-4e62-9b20-45050e35d904)

A game art generator for SBC computing type devices. uses the **[Libretro Thumbnails](https://thumbnails.libretro.com/)** archive.

> [!WARNING]
> This is **alpha software** - use at your own risk.

## Running

### Docker/Podman

```
docker run -it --rm -v "$(pwd):/app" ghcr.io/soup-bowl/garlic-butter:latest /app --help
```

Works on both **AMD64** and **ARM64**, and don't change `/app` in the command.

### Without

To traditionally build and run, you will need **Python 3.12 or greater**, and **[Poetry](https://pypi.org/project/poetry/)**.

```bash
poetry install
poetry run python -m butter --help
```

## Related

* Libretro Art (not affliated): https://github.com/libretro-thumbnails/libretro-thumbnails
* Pre-processor project: https://github.com/soup-bowl/rgs
