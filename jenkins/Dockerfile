FROM jenkins/jenkins

USER root

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    wget unzip \
    libglib2.0-0 \
    chromium \
    firefox-esr \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    netcat-openbsd  \
    && apt-get clean

USER jenkins
