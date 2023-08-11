# pull official base image
FROM python:3.9

RUN apt update

# set work directory
WORKDIR /src

# install libs
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY app/ /src/app
COPY run.py /src

CMD ["python3", "run.py"]
#CMD ["uvicorn", "app.run:app", "--host", "0.0.0.0", "--port", "8000"]
