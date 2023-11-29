## Prerequisites
### Python 🐍
> **`3.10` or newer.**
### Docker 🐳
> **Install compose if you haven't already**
## Installation
**Clone & Run**
````zsh
chmod +x ./scripts/install.sh && ./scripts/install.sh
````
## Services (4)
### Services:
1) **App:**
    - **Port:** `8000`
    - **Dockerfile:** `msrv.dockerfile`
2) **Redis Databases**
   - **Tokens cacher:**
        - **port:** `40888`
   - **Rate limiter**
        - **port:** `40185`
3) **Redis insights:**
    - **Port:** `8001`

## Run the Msrv:
##### The root `compose.yaml` file runs all containers
````commandline
docker compose -f compose.yaml up  --build
````
##### if you're in dev mode append this to the above command
````commandline
 --remove-orphans
````
> Do not run this flag in prod G
````commandline
uvicorn msrv.run:apx --reload --port=9696 && docker compose -f compose.yaml  up --build --remove-orphans
````
