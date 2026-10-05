FROM nginx:alpine

# Copiar archivos estáticos al directorio web de Nginx
COPY index.html /usr/share/nginx/html/index.html
COPY presentacion-izon-consulting.html /usr/share/nginx/html/presentacion-izon-consulting.html
COPY . /usr/share/nginx/html/

# Exponer el puerto estándar
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
