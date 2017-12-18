FROM python:3
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["go build -buildmode=c-shared -o govcf-vmc.so", "govcf-vmc.go"]
CMD ["python", "app.py"]
