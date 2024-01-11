FROM python:3

COPY . /Deception
WORKDIR /Deception

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip

EXPOSE 21

CMD ["mainftp.py"]
ENTRYPOINT ["python3"]
