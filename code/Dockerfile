FROM alpine:3.5

MAINTAINER Jan Holthuis "jan.holthuis@ruhr-uni-bochum.de"

# Create user (do it early so we don't need to do this every time we change
# something)
RUN mkdir /data
RUN adduser -D -h /data xjcc
RUN mkdir -p /opt/xjcc

# Install dependencies
RUN apk add --update \
    ca-certificates \
    python3 \
    nodejs \
    py-setuptools \
    py-lxml \
    maven \
    openjdk8 \
    ruby \
    ruby-irb \
    ruby-rdoc

# Install NodeJS dependencies
RUN npm install -g \
    https://github.com/Holzhaus/xmldom/archive/b025df61e65536ddf5cf396fefbdded973108ba1.tar.gz \
    x2js@3.1.0 \
    jxon@2.0.0-beta.4 \
    jsonml-tools@2.0.0 \
    https://github.com/Holzhaus/jsonml/archive/c8c15cc276eda15a85b67a4883196efe4528b171.tar.gz

# Install Ruby dependencies
RUN gem install cobravsmongoose --version '=0.0.2'

# Install Python requirements
COPY requirements.txt /opt/xjcc/requirements.txt
RUN pip3 install -r /opt/xjcc/requirements.txt

# Clean up package cache
RUN rm -rf /var/cache/apk/*

# Install python package
COPY xjcc /opt/xjcc/xjcc
RUN cd /opt/xjcc/xjcc && ./setup.py install

# Install nodejs helper library
COPY node-xjcc /opt/xjcc/node-xjcc
RUN npm install -g /opt/xjcc/node-xjcc

# Install converter wrappers
COPY xjcc-jsonlib /opt/xjcc/xjcc-jsonlib
RUN cd /opt/xjcc/xjcc-jsonlib && ./setup.py install

COPY xjcc-jsonml /opt/xjcc/xjcc-jsonml
RUN cd /opt/xjcc/xjcc-jsonml && ./setup.py install

COPY xjcc-jxon /opt/xjcc/xjcc-jxon
RUN cd /opt/xjcc/xjcc-jxon && ./setup.py install

COPY xjcc-orgjsonxml /opt/xjcc/xjcc-orgjsonxml
RUN cd /opt/xjcc/xjcc-orgjsonxml && ./setup.py install

COPY xjcc-pesterfish /opt/xjcc/xjcc-pesterfish
RUN cd /opt/xjcc/xjcc-pesterfish && ./setup.py install

COPY xjcc-x2js /opt/xjcc/xjcc-x2js
RUN cd /opt/xjcc/xjcc-x2js && ./setup.py install

COPY xjcc-xmljson /opt/xjcc/xjcc-xmljson
RUN cd /opt/xjcc/xjcc-xmljson && ./setup.py install

COPY xjcc-cobravsmongoose /opt/xjcc/xjcc-cobravsmongoose
RUN cd /opt/xjcc/xjcc-cobravsmongoose && ./setup.py install

RUN rm -rf /opt/xjcc

RUN mkdir -p /usr/share/xjcc
COPY test-documents /usr/share/xjcc/test-documents

# Don't run as root inside container
USER xjcc

# Allow persistant data storage by mapping /data to the host system via
#     $ docker run -it -v /path/on/host:/data
VOLUME /data
WORKDIR /data
CMD ["/bin/sh"]
