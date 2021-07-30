FROM python:3.8 as builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#RUN apt update apt install postgresql-dev gcc python3-dev musl-dev
RUN apt-get update
RUN apt-get upgrade -y && apt-get install postgresql gcc python3-dev musl-dev -y


RUN pip install --upgrade pip

COPY . .

COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


FROM python:3.8

RUN mkdir -p /home/app

RUN groupadd app
RUN useradd -m -g app app -p PASSWORD
RUN usermod -aG app app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

RUN apt-get update \
    && apt-get install netcat -y
RUN apt-get upgrade -y && apt-get install dos2unix

COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY ./entrypoint.prod.sh $APP_HOME

COPY . $APP_HOME

RUN dos2unix /home/app/web/entrypoint.sh

RUN chmod +x /home/app/web/entrypoint.sh

RUN chown -R app:app $APP_HOME

USER app

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]