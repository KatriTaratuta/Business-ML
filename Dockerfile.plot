## Dockerfile для `plot.py`
FROM python:3.9-slim
WORKDIR /app
COPY plot.py requirements.txt ./
RUN pip install -r requirements.txt
CMD ["python", "plot.py"]