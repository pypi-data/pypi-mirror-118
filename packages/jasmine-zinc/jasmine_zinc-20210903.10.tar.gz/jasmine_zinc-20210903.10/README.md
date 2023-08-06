# Jasmine Zinc

## Usage: Module

### get_avatars
```python
from jasmine_zinc import get_avatars

avatars = get_avatars(
    server_url='http://user:password@server_ip:7180',
)

print(avatars)
```

### talk_on_server
```python
from jasmine_zinc import talk_on_server, Talk

result = talk_on_server(
    server_url='http://user:password@server_ip:7180',
    cid=5201,
    talk=Talk(
        talktext='てすと',
    ),
)

print(result.message)
```

### record_talk
```python
from jasmine_zinc import record_talk, Talk

result = record_talk(
    server_url='http://user:password@server_ip:7180',
    cid=5201,
    talk=Talk(
        talktext='てすと',
    ),
    frequency=48000,
)


from playsound import playsound
import tempfile

with tempfile.NamedTemporaryFile() as fp:
    fp.write(result.wave_binary)

    playsound(fp.name)
```


## Usage: Console Scripts
### Environment Variables
```env
SERVER_URL=http://user:password@server_ip:7180
```

### jaz_get_avatars
Fetch avatar list (`cid`, `name`, etc.). Currently, the output format is work in progress.

```shell
jaz_get_avatars --server-url=http://user:password@server_ip:7180

export SERVER_URL=http://user:password@server_ip:7180
jaz_get_avatars
```

### jaz_talk_on_server
Talk on server.

```shell
jaz_talk_on_server 5201 "talktext" --server-url=http://user:password@server_ip:7180

export SERVER_URL=http://user:password@server_ip:7180
jaz_talk_on_server 5201 "talktext"
```

### jaz_record_talk
Record a talk voice on server, download as a wave file and play on client.

```shell
jaz_record_talk 5201 "talktext" --server-url=http://user:password@server_ip:7180

export SERVER_URL=http://user:password@server_ip:7180
jaz_record_talk 5201 "talktext"
```

## Development: Test Console Scripts
### Create .env file
```env
SERVER_URL=http://user:password@server_ip:7180
```

### Execute
```shell
./scripts/get_avatars

./scripts/talk_on_server 5201 てすと

./scripts/record_talk 5201 てすと
```
