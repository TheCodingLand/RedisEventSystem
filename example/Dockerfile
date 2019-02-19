FROM python:latest

RUN apt-get update && apt-get install -y \
        build-essential \
        wget \
        git \
        python3-dev \
        unixodbc-dev


RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

RUN git clone https://github.com/facebookresearch/fastText.git
WORKDIR /usr/src/app/fastText
RUN python setup.py install
RUN make
RUN chmod 777 /usr/src/app/fastText/fasttext
WORKDIR /usr/src/app
RUN mkdir /usr/src/app/model
RUN wget https://s3-us-west-1.amazonaws.com/fasttext-vectors/supervised_models/lid.176.ftz -O /usr/src/app/model/model.ftz

WORKDIR /usr/src/app

ADD . /usr/src/app
CMD python3 main.py