FROM python:3.14

RUN mkdir /mock_service

WORKDIR /mock_service

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh