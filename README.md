1. clone application

2. Specify the local port for fastapi to run on in the Dockerfile and docker-compose.yml files

3. Cd into the project directory in terminal

4. Build the cocker container with "docker-compose build" (sudo docker-compose build)

5. Run the container with "docker-compose up" (sudo docker-compose up) \*\*To run in detach mode use "docker-compose up -d"

6. Access swagger UI at localhost/api/docs or on allocated port

7. Database is mounted in a separate docker container but PGadmin can be accessed at "http://196.43.196.108:8988/browser/"

\__(\*_\*)\_\_/
/ \
