FROM ubuntu:impish-20220404
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get upgrade && apt-get update -y && apt-get install -y --no-install-recommends ca-certificates \
    apt-transport-https \
    software-properties-common \
    locales 

RUN locale-gen en_US.UTF-8

RUN apt-get update; \
    apt-get install -y --allow-unauthenticated \
    build-essential \
    gcc \
    libc6 \
    libc6-dev \
    libclang-dev \
    php \
    libapache2-mod-php8.0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN php -v
RUN php -i | grep "Configuration File (php.ini) Path" | awk '{print $6}'

ENV PATH=/root/.cargo/bin:$PATH
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- --default-toolchain stable -y
RUN apt-get update && apt-get install -y php-dev

COPY app /app
WORKDIR /app/inge_gateway/
RUN cargo build --release

RUN echo 'extension=/app/inge_gateway/target/release/libinge_gateway.so' >> $(php -i | grep "Configuration File (php.ini) Path" | awk '{print $6}')/php.ini
RUN echo 'extension=/app/inge_gateway/target/release/libinge_gateway.so' >> /etc/php/8.0/apache2/php.ini
RUN php -m
# COPY app/inge_gateway/target/release/libinge_gateway.so /dev/php/modules/
# COPY app/server/index.php /var/www/html/

# RUN chmod 755 /var/www/html/index.php