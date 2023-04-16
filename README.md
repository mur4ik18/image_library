# zakhar_website
You should work with this project carefully

## Very important enformation
- database is in docker
- database has volume
- all images not saves in docker
- we have tests but i need rewrite a lot of tests

## Important commands
```
docker-compose -f .\docker-compose.prod.yml up --build -d
```
```
docker-compose stop
```
```
docker container ls | grep "web"
docker logs id
```

database:

```
sudo su - postgres
pg_dump --dbname=Name --host=Host --port=Port --username=username -f db.dump
psql -U username -p port -h 127.0.0.1 -d dbname < db.dump
```
## :memo: License ##
Made with :heart: by <a href="https://github.com/mur4ik18" target="_blank">mur4ik18</a>

<a href="#top">Back to top</a>
