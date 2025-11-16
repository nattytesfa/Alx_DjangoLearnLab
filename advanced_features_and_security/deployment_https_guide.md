# HTTPS Deployment Configuration Guide

## Overview
This guide provides instructions for configuring your Django application to use HTTPS in production, including web server configuration and SSL certificate setup.

## Web Server Configuration Examples

### Nginx Configuration (nginx.conf)

### Important: Proxy Header Configuration
When using a reverse proxy like Nginx, you must configure the `X-Forwarded-Proto` header:

```nginx
location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;  # This tells Django it's HTTPS
}
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Security: Redirect all HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Certificate Configuration
    ssl_certificate /path/to/your/fullchain.pem;
    ssl_certificate_key /path/to/your/privkey.pem;
    
    # Security: SSL Protocol Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    # Security: HSTS Header (complements Django's HSTS settings)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    
    # Django Application Configuration
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Static Files
    location /static/ {
        alias /path/to/your/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Media Files
    location /media/ {
        alias /path/to/your/media/;
        expires 1d;
    }
}

<VirtualHost *:80>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    
    # Security: Redirect to HTTPS
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    
    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /path/to/your/certificate.crt
    SSLCertificateKeyFile /path/to/your/private.key
    SSLCertificateChainFile /path/to/your/ca_bundle.crt
    
    # Security Headers
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    Header always set X-Frame-Options "DENY"
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-XSS-Protection "1; mode=block"
    
    # Django WSGI Configuration
    WSGIDaemonProcess yourproject python-path=/path/to/your/project
    WSGIProcessGroup yourproject
    WSGIScriptAlias / /path/to/your/project/wsgi.py
    
    # Static Files
    Alias /static/ /path/to/your/staticfiles/
    <Directory /path/to/your/staticfiles>
        Require all granted
    </Directory>
    
    # Media Files
    Alias /media/ /path/to/your/media/
    <Directory /path/to/your/media>
        Require all granted
    </Directory>
</VirtualHost>
