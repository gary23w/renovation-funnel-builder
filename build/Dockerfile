FROM php:7.4-apache

# Set the environment variable for the funnel port?
# ENV FUNNEL_PORT=8484

WORKDIR /var/www/html

RUN rm -rf ./*

COPY ./eavestrough /var/www/html

EXPOSE $FUNNEL_PORT

RUN echo "Listen $FUNNEL_PORT" >> /etc/apache2/ports.conf && \
    sed -i "/<VirtualHost \*:80>/c\<VirtualHost *:$FUNNEL_PORT>" /etc/apache2/sites-available/000-default.conf

RUN a2enmod rewrite

RUN a2enmod headers

CMD ["apache2-foreground"]
