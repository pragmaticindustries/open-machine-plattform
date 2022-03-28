FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY prod_requirements.txt /code/
RUN pip install -r prod_requirements.txt
COPY . /code/
ENTRYPOINT ["bash", "start.sh"]