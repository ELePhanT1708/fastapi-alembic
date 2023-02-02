FROM python:3.11

WORKDIR /project

COPY requirements.txt /project/requirements.txt

RUN pip install  -r /project/requirements.txt

#
COPY . /project/
COPY src /project/
COPY migrations /project/

EXPOSE 8000
#
CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]