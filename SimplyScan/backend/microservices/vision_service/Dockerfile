# /backend/microservices/account-service/Dockerfile

FROM python:3.10-slim
WORKDIR /app
COPY ../../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# If need ML or Additional libraries
# RUN pip install opencv-python-headless tensorflow 
COPY . .
EXPOSE 5000
CMD python vision.py
