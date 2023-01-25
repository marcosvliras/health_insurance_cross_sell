# pull official base image
FROM python:3.9

RUN apt update

# set work directory
WORKDIR /src

# copy project
COPY app/ /src/app


RUN pip install -r app/requirements.txt


CMD ["uvicorn", "app.run:app", "--host", "0.0.0.0", "--port", "80"]
