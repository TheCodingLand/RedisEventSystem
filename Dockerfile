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

#This is a full wikipedia extract. using that later
#RUN wget https://s3-us-west-1.amazonaws.com/fasttext-vectors/word-vectors-v2/cc.fr.300.bin.gz
#RUN gunzip cc.fr.300.bin.gz
# add app

RUN make
RUN chmod 777 /usr/src/app/fastText/fasttext
RUN pip install pyfasttext
RUN mkdir -p /data/logs/
RUN mkdir -p /data/models/ 
#Sample Language Classification model
RUN mkdir -p /data/models/language/0/doc
RUN wget https://s3-us-west-1.amazonaws.com/fasttext-vectors/supervised_models/lid.176.ftz -O /data/models/language/0/model.ftz
WORKDIR /usr/src/app

RUN pip install -r requirements.txt
ADD . /usr/src/app
CMD python3 main.py