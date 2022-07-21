FROM python:3.10
WORKDIR /dictionary_project
ENV PYTHONDONTWIRTEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY Pipfile Pipfile.lock /dictionary_project/
RUN pip install pipenv && pipenv install --system