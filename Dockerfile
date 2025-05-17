# Python 3.9 base image
FROM python:3.9-slim

# Çalışma dizinini belirle
WORKDIR /app

# Sistem bağımlılıklarını kur (örneğin: gunicorn için derleyici gerekebilir)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Gereksinimleri ekle ve yükle
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY ./app /app


# Flask uygulaması 5000 portunda çalışacak
EXPOSE 5000

# Gunicorn ile SSL destekli başlat
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]