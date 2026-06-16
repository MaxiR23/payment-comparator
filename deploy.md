# Flask — instrucciones de deploy

## Estructura del proyecto

```
payment-comparator/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   ├── css/style.css
│   └── js/
├── config/
│   └── settings.py
├── src/
│   ├── reader.py
│   ├── comparator.py
│   └── writer.py
├── uploads/                ← se crea automáticamente
└── output/                 ← se crea automáticamente
```

---

## Instalación en el VPS

```bash
# 1. Clonar / subir el proyecto
cd /var/www/payment-comparator

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Probar que arranca
python app.py
# → abrí http://TU_IP:5000 en el browser
```

---

## Producción con gunicorn + nginx

### gunicorn (proceso Python)

```bash
gunicorn -w 2 -b 127.0.0.1:5000 app:app
```

### systemd (para que corra siempre)

Creá `/etc/systemd/system/pagos.service`:

```ini
[Unit]
Description=Comparador de Pagos
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/payment-comparator
ExecStart=/var/www/payment-comparator/venv/bin/gunicorn -w 2 -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload
systemctl enable pagos
systemctl start pagos
```

### nginx (proxy reverso)

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    client_max_body_size 25M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
nginx -t && systemctl reload nginx
```

### HTTPS gratis con Let's Encrypt

```bash
apt install certbot python3-certbot-nginx
certbot --nginx -d tu-dominio.com
```

---

## Limpieza de reportes viejos (opcional)

Agregá este cron para borrar reportes de más de 1 hora:

```bash
# crontab -e
0 * * * * find /var/www/payment-comparator/output -name "*.xlsx" -mmin +60 -delete
```