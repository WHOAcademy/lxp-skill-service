FROM quay.io/whoacademy/python-38:latest

ENV PYTHONUNBUFFERED 1

ARG build_url=default
ARG git_commit=default
ARG git_url=default

LABEL labs.build.url="${build_url}" \
      labs.git.tag="${git_commit}" \
      labs.git.url="${git_url}"

COPY . $HOME

RUN pip install -r requirements.txt

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8080