FROM nginx:latest

# Удаление стандартного дефолтного конфига, чтобы он не перебивал наш порт 80
RUN rm /etc/nginx/conf.d/default.conf

#Создание папки под статику внутри контейнера Nginx
RUN mkdir -p /app/staticfiles

# Копирование нашего кастомного главного конфигурационного файла
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

# Запуск Nginx на переднем плане
CMD ["nginx", "-g", "daemon off;"]