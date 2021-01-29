
## Activate Python Virtual Environment
```
. venv/bin/activate
```
On Windows
```
> venv\Scripts\activate
```


## Start Server
```
(venv) andrew@macbook-pro:api-server $ export FLASK_APP=server.py
(venv) andrew@macbook-pro:api-server $ flask run
```

## Test Endpoint
In a separate Terminal than that which is now running the local Flask server
```
andrew@macbook-pro:~ $ curl -d "data=fact" http://127.0.0.1:5000/factcheck 

FACT!

andrew@macbook-pro:~ $ curl -d "data=fakenews" http://127.0.0.1:5000/factcheck 

FALSE
```


Leave Virtual Environment
```
(venv) andrew@macbook-pro:api-server $ deactivate
```
