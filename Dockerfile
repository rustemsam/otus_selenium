
FROM python:3.12


WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    chromium \
    firefox-esr \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    wget unzip \
    && apt-get clean


RUN pip install -U pip \
    && pip install pytest==8.3.3 \
    && pip install selenium==4.25.0 \
    && pip install pydantic==2.10.5 \
    && pip install allure-pytest==2.13.5 \
    && pip install allure-python-commons==2.13.5


CMD ["pytest", "-v", "--alluredir", "allure-results"]