FROM python:3.10


WORKDIR /app
COPY . .

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt



EXPOSE 8090
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8090"]