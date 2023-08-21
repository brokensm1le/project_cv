FROM python:3

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN mkdir /app/uploads

RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "main.py"]
