# MULTI STAGE DOCKERFILE
# BASE STAGE
# Base image from dockerhub/hub.docker.com
FROM python:3.9 as base-stage
# Set the working directory
WORKDIR /temp
# Install Poetry to base-stage
RUN pip install poetry
# Copy pyproject and lock file from local to base-stage
COPY ./pyproject.toml ./poetry.lock* /temp/
# Export the poetry lock file to the requirements.txt for use by pip
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# BUILD STAGE
FROM python:3.9 as build-stage
# Set the working directory
WORKDIR /app
# Copy the requirements.txt file from the base-stage to build-stage
# We don't need Poetry in this stage since requirements.txt is read by pip
COPY --from=base-stage /temp/requirements.txt /app/requirements.txt
# Install the package dependencies that Poetry generated
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
# Copy source code from local to build-stage
COPY /src /app/src

# EXPOSE 8000

CMD [ "uvicorn",  "src.main:app", "--host=0.0.0.0", "--reload"]
