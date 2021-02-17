# WYIN backend - feed microservice
This is a REST API for WYIN feed

## Table of contents
* [Getting started]
* [API docs]
* [I want to contribute/learn more technical details]


## Getting started
1. [Download and install Docker]

2. Build a container
```
make build
```
or
```
docker build -t wyin-be-feed .
```

3. Run server
```
make run
```
or
```
docker run -p 8080:8080 wyin-be-feed:latest
```

4. Query `/health` endpoint
```
curl -i http://localhost:8080/health
```


## API docs
(Make sure that server is running)
* [Swagger UI](http://localhost:8080/docs)
* [OpenAPI specification](http://localhost:8080/openapi.json)


## I want to contribute/learn more technical details
Check out [CONTRIBUTING](CONTRIBUTING.md)



[Getting started]: #getting-started
[API docs]: #api-docs
[I want to contribute/learn more technical details]: #i-want-to-contributelearn-more-technical-details

[Download and install Docker]: https://docs.docker.com/get-started/#download-and-install-docker
