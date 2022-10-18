# pull the official base image
FROM python:3.6.8

# set work directory
WORKDIR /Puyuan

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip 

COPY ./requirements.txt /Puyuan

RUN pip install -r requirements.txt

# copy project
COPY . /Puyuan

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]