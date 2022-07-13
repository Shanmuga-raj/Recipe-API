FROM python:3
LABEL maintainer='Shanmugaraj'

ENV PYTHONBUFFERED 1
RUN mkdir /app

COPY requirements.txt /tmp/requirements.txt
COPY requirements.dev.txt /tmp/requirements.dev.txt

WORKDIR /app
COPY . /app/

EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
	/py/bin/pip install --upgrade pip && \
	/py/bin/pip install -r /tmp/requirements.txt && \
	if [ $DEV = 'true' ]; \
		then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
	fi && \
	rm -rf /tmp && \
	adduser \
		--disabled-password \
		--no-create-home \
		django-user

ENV PATH="/py/bin:$PATH"

USER django-user