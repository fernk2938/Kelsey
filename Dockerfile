FROM php:8.1-apache
COPY ./frontend /var/www/html/
EXPOSE 80
CMD ["apache2-foreground"]
