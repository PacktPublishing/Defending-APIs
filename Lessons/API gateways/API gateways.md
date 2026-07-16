# API Gateways
In this lesson, you will learn about the Kong API gateway and how to use it to secure your APIs. You will install Kong locally in Docker, create routes and services, and use plugins to secure the APIs.

## Setup
Follow the [instructions on the Kong documentation site](https://docs.konghq.com/gateway/latest/install/docker/) to install Kong Gateway within your Docker environment. 

The following steps are required: 

* Create a dedicated network for Kong

  ```bash
  docker network create kong-net
  ```

* Start a PostgreSQL container

  ```bash
    docker run -d --name kong-database \
    --network=kong-net \
    -p 5432:5432 \
    -e "POSTGRES_USER=kong" \
    -e "POSTGRES_DB=kong" \
    -e "POSTGRES_PASSWORD=kongpass" \
    postgres:13  
  ```

* Prepare the Kong database

  ```
  docker run --rm --network=kong-net \
    -e "KONG_DATABASE=postgres" \
    -e "KONG_PG_HOST=kong-database" \
    -e "KONG_PG_PASSWORD=kongpass" \
    -e "KONG_PASSWORD=test" \
    kong/kong-gateway:3.5.0.1 kong migrations bootstrap
  ```

* Prepare the Kong database

  ```bash
    docker run -d --name kong-gateway \
    --network=kong-net \
    -e "KONG_DATABASE=postgres" \
    -e "KONG_PG_HOST=kong-database" \
    -e "KONG_PG_USER=kong" \
    -e "KONG_PG_PASSWORD=kongpass" \
    -e "KONG_PROXY_ACCESS_LOG=/dev/stdout" \
    -e "KONG_ADMIN_ACCESS_LOG=/dev/stdout" \
    -e "KONG_PROXY_ERROR_LOG=/dev/stderr" \
    -e "KONG_ADMIN_ERROR_LOG=/dev/stderr" \
    -e "KONG_ADMIN_LISTEN=0.0.0.0:8001" \
    -e "KONG_ADMIN_GUI_URL=http://localhost:8002" \
    -e KONG_LICENSE_DATA \
    -p 8000:8000 \
    -p 8443:8443 \
    -p 8001:8001 \
    -p 8444:8444 \
    -p 8002:8002 \
    -p 8445:8445 \
    -p 8003:8003 \
    -p 8004:8004 \
    kong/kong-gateway:3.5.0.1
  ```

* Verify that the service are running by checking for a 200 status code with the following command:
  
  ` curl -i -X GET --url http://localhost:8001/services`

* Access the UI in a browser at the following URL: [http://localhost:8002](http://localhost:8002)

* If any issues are encountered, check the status of the two Docker containers. You should see the following output:

  ```
  # docker ps
    CONTAINER ID   IMAGE                          COMMAND                  CREATED      STATUS                             PORTS                                                                               NAMES
    
    c9068a15d7ae   kong/kong-gateway:3.5.0.1      "/entrypoint.sh kong…"   3 days ago   Up 58 seconds (health: starting)   0.0.0.0:8000-8004->8000-8004/tcp, 0.0.0.0:8443-8445->8443-8445/tcp, 8446-8447/tcp   kong-gateway
    
    2077a00bc8ba   postgres:13                    "docker-entrypoint.s…"   3 days ago   Up About a minute                  0.0.0.0:5432->5432/tcp                                                              kong-database
  ```

## Instructions

### Step 1: Create routes and services for your API
In the first step you need to create routes (inbound connections) and services (outbound connections) for your API on Kong. You can read more about routes and services [here](https://docs.konghq.com/gateway/latest/get-started/services-and-routes/).

For your target APIs I suggest the following:
* a local installation of vAPI from the hacking session
* a local version of [Pixi](../../Sample%20APIs/Pixi/)
* local version of [HTTPBin](http://httpbin.org)
* the [Mockbin.io](https://mockbin.io/) service
* the [Beeceptor](https://beeceptor.com/) service

One you have connected the routes to the services, verify you can access your API via Kong rather than directly.

### Step 2: Install one or more Kong security plugins  
Install one or more of the free plugins from the [Kong Hub](https://docs.konghq.com/hub/?) and verify these work as expected. 

The following are suggested in order of difficulty:
* [IP Restriction](https://docs.konghq.com/hub/kong-inc/ip-restriction/)
* [Rate Limiting](https://docs.konghq.com/hub/kong-inc/rate-limiting/)
* [Basic Authentication](https://docs.konghq.com/hub/kong-inc/basic-auth/)
* [JWT](https://docs.konghq.com/hub/kong-inc/jwt/) - a free t-shirt to the first person to get this working!

## Further Reading
* [Kong documentation](https://docs.konghq.com/gateway/3.5.x/)
* [Kong Hub](https://docs.konghq.com/hub/?)