## Getting Started
* Install Docker: `https://docs.docker.com/get-docker/`
* Clone project: `https://github.com/srh09/fast_api_playground.git`
* Setup a virtual env w Python 3.9: `python -m venv .venv` then `source .venv/bin/activate`
* Install Poetry: `pip install poetry`
* Create Docker image(s): `bin/run.sh build`
* Start Docker containers: `bin/run.sh start`
* In Chrome or web browser visit: `http://localhost:8000/api/v1/test`

## NOTES:
* Remote into local server: `sudo docker exec -it [name (ex. fastapi-web-1)] ../bin/bash`
