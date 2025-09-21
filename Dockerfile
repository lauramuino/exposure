FROM python:3.11-slim

WORKDIR /app

#CHECK WHAT IS THE BEST WAY TO ORGINZE FILES OF THE APP IN CONTRAST OF THE DOCKERFILE 
COPY requirements .

RUN pip install --no-cache-dir -r requirements

COPY . .

EXPOSE 8000 

#check more about uvicorn server and this parameters, what is it that it does, and also see about nginx
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
