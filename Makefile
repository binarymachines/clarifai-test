#
#

up:
	docker-compose up -d

down: 
	docker-compose down --remove-orphans -v

docker-rm:
	docker-compose rm -f

bounce: down docker-rm up


import-data:
	 psql -h localhost --port=6432 -U dba -d testdb -f DEtest.sql

clear-data:
	psql -h localhost --port=6432 -U dba -d testdb -f purgedb.sql

dump-data:
	pg_dump -h localhost --port=6432 -U dba -d testdb --schema public -t clarifai_events_ru > rollup.txt

dblogin:
	psql -h localhost --port=6432 -U dba -d testdb


