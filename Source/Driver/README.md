# Driver

```sh
Usage: tracker.py [OPTIONS] COMMAND [ARGS]...

Commands:
  runserver

Options:
  --port INTEGER
  --tables TEXT
  --help          Show this message and exit.
```

```sh
python tracker.py runserver --tables ./resources/tables.sql
```

```json
POST localhost:4444
{
    "urls": [],
    "refresh": bool
}
```
