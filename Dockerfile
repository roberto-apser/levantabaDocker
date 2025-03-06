FROM python:3.12-slim
EXPOSE 80
COPY api/ /app/api
COPY api/app.py /app
COPY requirements.txt /app
WORKDIR /app
RUN pip --no-cache-dir install --upgrade -r requirements.txt
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
