# Getting Start

env: linux

first, download model from here:
https://github.com/mistralai/mistral-inference

assume model in `models` file

```
python -m venv venv
pip install -r requirements.txt
```

# usage

(ensure modify path in script depends your env)

## command line chat:

```
bash interact-chat.sh
```

## server

```
bash deploy-server.sh
```

if you want run in backend, run with nohup command:

```

bash nohup deploy-server.sh

```

or modify script by yourself.

enjoy!