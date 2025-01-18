
FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    chromium \
    firefox-esr \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    wget unzip \
    && apt-get clean

RUN pip install -r requirements.txt

COPY . .

CMD ["pytest", "-v", "--alluredir", "allure-results"]