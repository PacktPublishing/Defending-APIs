# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11-slim

RUN apt update && apt upgrade -y && apt install curl httpie htop -y

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY jwt_tool.py /opt/.
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD echo 'USAGE: "docker run --rm -v "$(PWD)/app:/app" --privileged -u root -it pythonbox /bin/bash"'