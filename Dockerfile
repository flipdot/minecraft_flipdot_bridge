FROM python:3.7

RUN pip install pipenv
RUN mkdir /app

WORKDIR /app

COPY Pipfile* ./
RUN pipenv install

COPY app.py ./
ENTRYPOINT ["pipenv", "run"]
CMD python app.py