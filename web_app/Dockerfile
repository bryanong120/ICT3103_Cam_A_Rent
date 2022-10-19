# start by pulling the python image
FROM python:latest

#switch working dir
WORKDIR /app

#copy requirements file into image
COPY requirements.txt /app

#install the dependencies and packages in requirement file
RUN pip3 install -r requirements.txt --no-cache-dir

#copy every content from local file into image
COPY . /app

CMD python app.py
