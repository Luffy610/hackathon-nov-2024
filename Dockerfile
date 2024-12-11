FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
WORKDIR backend
EXPOSE 8080
CMD [ "python","alchemist_backend.py"]
