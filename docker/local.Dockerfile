# This docker file is used for local development via docker-compose
# Creating image based on official python3 image
FROM python:3.10

# Fix python printing
ENV PYTHONUNBUFFERED 1

# Installing all python dependencies
ADD requirements.txt ./
RUN pip install -r requirements.txt


# Get the project into the docker container
RUN mkdir /app
WORKDIR /app
ADD ./ /app/
