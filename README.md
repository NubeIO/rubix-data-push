# Rubix Date Push

## Running in development

- Use [`poetry`](https://github.com/python-poetry/poetry) to manage dependencies
- Simple script to install

    ```bash
    ./setup.sh
    ```

- Join `venv`


    ```
        poetry shell
    ```

- Build local binary

    ```bash
    poetry run pyinstaller run.py -n rubix-data-push --clean --onefile --add-data pyproject.toml:. --add-data config:config
    ```

  The output is: `dist/rubix-data-push`

## Docker build

### Build

```bash
./docker.sh
```

The output image is: `rubix-data-push:dev`

### Run

```bash
docker volume create rubix-data-push
docker run --rm -it -p 2020:2020 -v rubix-data-push-data:/data --name rubix-data-push rubix-data-push:dev
```

## Deploy on Production

- Download release artifact
- Review help and start

```bash
$ rubix-data-push -h
Usage: rubix-data-push [OPTIONS]

Options:
  -p, --port INTEGER       Port  [default: 2020]
  -g, --global-dir PATH    Global dir
  -d, --data-dir PATH      Application data dir
  -c, --config-dir PATH    Application config dir
  -i, --identifier TEXT    Identifier  [default: lora]
  --prod                   Production mode
  -s, --setting-file TEXT  Rubix-Lora: setting json file
  -l, --logging-conf TEXT  Rubix-Lora: logging config file
  --gunicorn-config TEXT   Gunicorn: config file(gunicorn.conf.py)
  -h, --help               Show this message and exit.
```

