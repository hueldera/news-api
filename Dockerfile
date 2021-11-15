FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR /app

COPY Pipfile* ./
COPY requirements.txt ./

RUN pip install pipenv && \
    pipenv install --system --deploy --clear

COPY . ./