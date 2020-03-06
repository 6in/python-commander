## Python Commander

### settings

```
pip install -r requirements.txt
```

* PostgreSQLと接続するときは、PostgreSQLのライブラリが必要

```
sudo dnf install postgresql-devel
```


### SSL settings

```
openssl req -new -x509 -keyout config/server.pem -out config/server.pem -days 365 -nodes
```

