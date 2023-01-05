# [Choice] Python version (use -bullseye variants on local arm64/Apple Silicon): 3, 3.10, 3.9, 3.8, 3.7, 3.6, 3-bullseye, 3.10-bullseye, 3.9-bullseye, 3.8-bullseye, 3.7-bullseye, 3.6-bullseye, 3-buster, 3.10-buster, 3.9-buster, 3.8-buster, 3.7-buster, 3.6-buster
ARG VARIANT="3.7-bullseye"

# Use microsoft provided python image, as it contains allready necessary tools. It's build on top of the official python image.
FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Copy app to workspace folder, and install requirements
WORKDIR /app
COPY . .
RUN pip --disable-pip-version-check --no-cache-dir install -r requirements.txt

# Install self as editable module. In a long run it would be recommeded
# to remove `COPY` and only install module.
RUN pip --disable-pip-version-check install -v -e .

# Create vscode extension folder, and change ownership of it.
ARG USERNAME=vscode
RUN test ! -z "{$USERNAME}" && mkdir -p /home/${USERNAME}/.vscode-server/extensions && \
    chown -R $USERNAME /home/$USERNAME/.vscode-server

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

# [Optional] Uncomment this line to install global node packages.
# RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && npm install -g <your-package-here>" 2>&1

# Declare default flask app as environment variable
ARG FLASK_APP=tjts5901.app
ENV FLASK_APP=${FLASK_APP}

# Setup the default port for flask to listen on
ARG PORT=5001
ENV PORT=${PORT}

EXPOSE ${PORT}

# Run Flask app, and listen all the interfaces
CMD flask run --host=0.0.0.0 --port="${PORT}"

# Run nothing, so that the container can be used as a base image
# CMD ["bash", "-c", "sleep infinity"]

# Run Flask app using Gunicorn, which unlike Flask, doesn't complain about being development thing.
#CMD ["gunicorn", "--bind", "0.0.0.0:${PORT}", "tjts5901.app:app"]
