FROM python:3.13

WORKDIR /app/

COPY parking_management/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/

EXPOSE 8000

ENTRYPOINT ["/bin/sh", "-c", "chmod +x /app/entrypoint.sh && /app/entrypoint.sh"]
