# Dockerfile-frontend
FROM python:3.8-slim
WORKDIR /app
COPY requirements-frontend.txt ./
RUN pip install --no-cache-dir -r requirements-frontend.txt
COPY . .
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]