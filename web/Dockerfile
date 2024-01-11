FROM python:3

COPY . /Deception
WORKDIR /Deception

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip
RUN pip3 install uvicorn
RUN pip3 install fastapi

EXPOSE 8000

CMD ["server.py"]
ENTRYPOINT ["python3"]
