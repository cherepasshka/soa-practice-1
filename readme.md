# Service oriented architecture practice-1

Сервис сериализации структурированных данных состоит из прокси сервера, к которому пользователь делает запросы, и из воркеров, которым перенаправляется пользовательский запрос и которые выполняют сериализацию и десериализацию.

## Использование:

Для начала надо сгенерировать proto файл с помощью:

```bash
protoc --python_out=. serialization_worker/serialization_module/schemas/proto_scheme.proto
```

Чтобы собрать и запустить проект необходимо выполнить  следующие команды, вместо `{{file.env}}` нужно подставить название файла с переменными окружения, для примера можно использовать [`example.env`](https://github.com/cherepasshka/soa-practice-1/blob/main/example.env)

```bash
docker-compose --env-file {{file.env}} build
docker-compose --env-file {{file.env}} up
```
После этого можно подключится к прокси сервису с помощью следующей команды:

```bash
nc 127.0.0.1 4242 -u
```
Далее необходимо ввести запрос.

Поддерживаются чувствительные к регистру запросы:

- get_statistics JSON
- get_statistics MESSAGEPACK
- get_statistics NATIVE
- get_statistics YAML
- get_statistics XML
- get_statistics AVRO
- get_statistics all

Структура у всех запросов одинаковая, порядок строк не важен:
```yaml
int: {целое число}
float: {вещественное число}
list_str: {массив строк, строки должны быть разделены пробелами (!)}
list_int: {массив целых чисел, числа должны быть разделены пробелами (!)}
list_float: {массив вещественных чисел, числа должны быть разделены пробелами (!)}
dict: {словарь строк}
```

После каждого запроса необходимо ввести `end`.

Пример запроса:

```
get_statistics all
int: 4200
float: 42.42
list_int: [1 2 3]
list_str: ['one' 'two' 'three']
dict: {"key": 'value'}
list_float: [1.2 3.4]
end
```