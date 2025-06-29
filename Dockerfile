FROM python:3.13

LABEL mantainer="mmtmmt945@gmail.com"
LABEL version="1.0.0"

WORKDIR /src

COPY requirements.txt /src/

RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . /src/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "8000"]