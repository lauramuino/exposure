FROM python:3.11-slim

WORKDIR /exposure-app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000 

#check more about uvicorn server and this parameters, what is it that it does, and also see about nginx
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
