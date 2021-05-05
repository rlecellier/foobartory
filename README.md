# Foobarty

## Install and run

```shell
$ git clone https://github.com/rlecellier/foobartory.git
$ mkvirtualenv foobartory
$ pip install -r requirements.txt
$ cd foobartory/src
$ python run.py
```

in order to make it quicker, you can add a `src/config/local_config.ini` file with :

```ini
[default]
tick_duration_in_second = 0.01
```


## Code quality

in `src/` directory
```shell
isort .
pylint $(git ls-files '*.py') --output-format="colorized" --score=no
```


## Structure

```
└── src/
    ├── config/
    |   ├── config.ini # foobartory default configuration.
    |   └── local_config.ini # local configuration override default.
    ├── core/
    |   ├──actions.py
    |   ├──foobartory.py
    |   ├──products.py
    |   └──warehouse.py
    ├── run.py
    └── settings.py
```

## TODO

* add some tests
* add git hooks
* configure log file

## Ideas

* add actions configuration
* think about a strategy configuration
* add configuration check (action duration against tick duration)
* add a report file for each run with configuration details and run details
