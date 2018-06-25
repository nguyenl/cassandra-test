FROM python:3.6.0-slim

# install the python requirements
ADD web/requirements.txt /opt/web/requirements.txt
RUN pip install -r /opt/web/requirements.txt 

ADD web/app.py /opt/web/app.py
ADD web/static /opt/web/static

## expose the port
EXPOSE 5000

ENV FLASK_APP=/opt/web/app.py
ENV FLASK_ENV=development

## start the command
CMD ["flask", "run", "--host=0.0.0.0"]
