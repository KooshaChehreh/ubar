FROM docker.arvancloud.ir/python:3.12

# RUN mkdir /app

WORKDIR /app
 

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
 
RUN pip install --upgrade pip 
 
COPY requirements.txt  ./requirements.txt
 
RUN pip install --no-cache-dir -r requirements.txt
 
COPY . /app
 
EXPOSE 8000

CMD ["gunicorn", "--reload", "--workers=4", "--worker-tmp-dir", "/dev/shm", "--bind=0.0.0.0:8000", "--chdir", "/app/ubar", "ubar.wsgi"]

