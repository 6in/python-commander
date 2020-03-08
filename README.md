## Python Commander

### settings

```
pip install -r requirements.txt
```

* PostgreSQLと接続するときは、PostgreSQLのライブラリが必要

```
sudo dnf install postgresql-devel
```

* MySQLと接続するときは、MySQLのライブラリが必要
```
sudo dnf install mysql-devel
```


### SSL settings

```
openssl req -new -x509 -keyout config/server.pem -out config/server.pem -days 365 -nodes
```

