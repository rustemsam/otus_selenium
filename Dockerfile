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
    netcat-openbsd  \
    && apt-get clean

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["pytest", "-v", "--alluredir", "allure-results"]
