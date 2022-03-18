FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install pipenv

COPY ./requirements.txt /app

RUN pip install -r requirements.txt 

COPY . /app

EXPOSE 81

# CMD ["uvicorn", "app.main:api", "--reload", "--host", "0.0.0.0", "--port", "81"]
CMD ["uvicorn", "app.main:api", "--host", "0.0.0.0", "--port", "81"]
