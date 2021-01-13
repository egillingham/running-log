# running-log


# Local Dev
Local development uses local mysql instance run via Docker. To get started, build and run that.

1. Build the main container
```
docker build -t running-log .
```

2. Start the containers in the background
```
docker-compose up -d
```

3. Should be able to access the website via http://0.0.0.0:5051/
4. Some tables (like hearts) may need to be added to the local MySQL Instance. Ask Erin for a dump.
    - Can access the instance via Sequel Pro via host = 127.0.0.1, user  = root, password = toor


Once the docker mysql container is up, you can also just run the app via command line instead of rebuilding the docker container:
```sh
python website/app.py
```