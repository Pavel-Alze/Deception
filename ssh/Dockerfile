FROM python:3

COPY . /Deception
WORKDIR /Deception

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

EXPOSE 22

CMD ["ssh.py","-p","22"]
ENTRYPOINT ["python3"]
