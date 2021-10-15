FROM continuumio/miniconda3
WORKDIR /project
ADD . /project
RUN pip install -r requirements.txt
ENV FLASK_APP=poke-api
EXPOSE 5000
CMD ["python", "app.py"]