# Jasmine Zinc

## Usage: Console Scripts
### Environment Variables
```env
SERVER_URL=http://user:password@server_ip:7180
```

### jaz_get_avatars
Fetch avatar list (`cid`, `name`, etc.).

### jaz_talk_on_server
Talk on server.

### jaz_record_talk
Record a talk voice on server, download as a wave file and play on client.


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
