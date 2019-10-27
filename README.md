### Пример работы (в работе с MongoDB)
Для запуска использовать `docker-compose up`
```
$nc localhost 5001
{"action":"get", "key":1}
{"status": "Not found"}
{"action":"put", "key": 1, "message": "hello"}
{"status": "Created"}
{"action":"get", "key":1}
{"status": "Ok", "message": "hello"}
{"action":"delete", "key": 1}
{"status": "Ok"}
```
