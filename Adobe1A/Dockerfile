ARG TARGETPLATFORM
FROM --platform=$TARGETPLATFORM python:3.10.14-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY process_pdfs.py .

CMD ["python", "process_pdfs.py"]