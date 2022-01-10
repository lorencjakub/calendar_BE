# Client calendar

## Frontend development mode
```bash
cd ./templates/static
npm run start
```

## Build production Docker image
```bash
podman build . -f Dockerfile -t client_calendar

# test it
podman run --rm -it -p 8001:8000 localhost/client_calendar:latest
```