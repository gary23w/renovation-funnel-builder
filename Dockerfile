FROM php:7.4-apache

WORKDIR /var/www/html

RUN rm -rf ./*

COPY ./prod /var/www/html

EXPOSE $FUNNEL_PORT

RUN echo 'Listen ${FUNNEL_PORT}' >> /etc/apache2/ports.conf

RUN sed -i '/<VirtualHost \*:80>/c\<VirtualHost *:${FUNNEL_PORT}>' /etc/apache2/sites-available/000-default.conf

RUN a2enmod rewrite

RUN a2enmod headers

CMD ["apache2-foreground"]