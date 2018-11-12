# clarifai-test
## Coding challenge for Clarifai

PLEASE NOTE: The bulk of code in this project was **not** created from scratch. The database-related modules are standard components pulled from active Binary repos; init.yaml, docker-compose.yaml, and the Makefile are modified from standard project boilerplate. It's convenience code that forms the start of most new projects in the toolshed.

### Requirements
The code assumes Python 3.5 or higher. You should have pipenv installed. I've generated a requirements.txt file for the convenience of those who have the wrong opinion about dependency management. ;-)

### Connecting to a database instance
I used PostgreSQL running in a local Docker container for this project, but you can point it at any database instance simply by updating the parameters in init.yaml. Assuming a live instance with testdb already created, you prepare it for the run by issuing 

`make import-data`

The `make dblogin` convenience target is only applicable if you're running Postgres in a container specified by the docker-compose.yaml file. Note that there are no volumes mapped in the docker-compose, so all data in the container is ephemeral.

### Running the code
Issue `pipenv install` to install the dependencies, then `pipenv run ./data-eng-challenge` with the appropriate args to run the code. Running the script without any args will return a usage string. Before using the --highest-duration arg, you must create the rollup table by issuing `data-eng-challenge --create-rollup`. (All the SQL code is in the main module.)

### Notes
The instructions in Part 1 don't explicitly say we should be casting float outputs to integers, but I assumed it from the sample answers.
The instructions in Part 2 of the challenge README were not entirely clear as to which columns were needed (aside from the obvious ones) in the rollup table. For the sake of readability I kept the list minimal, but adding the others is a trivial update. It was also not clear what was meant by "collapse across model versions", since calls to different versions of the same model are in fact separate calls with their own call stats. 

### Improvements
Automated testing. To do this I'd add a small sample dataset where the call stats for a given model work out to a known value against which we check the outputs.

