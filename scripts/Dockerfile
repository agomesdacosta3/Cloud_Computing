# Use a lightweight base image
FROM alpine:latest

# Set the working directory
WORKDIR /scripts

# Install curl, PostgreSQL client tools, and Docker client
RUN apk --no-cache add curl postgresql-client docker

# Copy the test scripts into the container
COPY ./test_app.sh .
COPY ./test_container.sh .
COPY ./entrypoint.sh .

# Set the entry point to run the entrypoint script
ENTRYPOINT ["/bin/sh", "./entrypoint.sh"]
