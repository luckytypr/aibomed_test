FROM python:3.8.3-slim-buster

ENV PYTHONUNBUFFERED=1 COLUMNS=200 TZ=Asia/Almaty

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gettext \
    cmake

# Set timezone
RUN ln -fs /usr/share/zoneinfo/Asia/Almaty /etc/localtime \
    && echo "Asia/Almaty" > /etc/timezone

WORKDIR /src

COPY ./src/requirements.txt ./requirements.txt

# Upgrade pip
RUN pip install --upgrade pip

# Add project dependencies
RUN pip install --no-cache-dir -Ur /src/requirements.txt

COPY . .

CMD ["./entrypoint.sh"]
