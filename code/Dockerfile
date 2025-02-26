FROM ubuntu:xenial

MAINTAINER Jan Holthuis "jan.holthuis@ruhr-uni-bochum.de"

# Create user (do it early so we don't need to do this every time we change
# something)
RUN useradd -m -d /data xjcc
RUN mkdir -p /opt/xjcc

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    unzip \
    python3 \
    python3-setuptools \
    python3-lxml \
    python3-pip \
    python3-wheel \
    nodejs \
    npm \
    openjdk-8-jdk-headless \
    maven \
    ruby \
    irb \
    php \
    php-json \
    composer \
    curl \
    mono-gac \
    mono-mcs \
    mono-runtime \
    libmono-system-runtime-serialization4.0-cil \
    libmono-system-xml-linq4.0-cil \
    libmono-system-xml4.0-cil \
    libmono-system-numerics4.0-cil

# Symlink "nodejs" to "node"
RUN ln -s /usr/bin/nodejs /usr/local/bin/node

# Install NodeJS dependencies
RUN npm install -g \
    https://github.com/Holzhaus/xmldom/archive/b025df61e65536ddf5cf396fefbdded973108ba1.tar.gz \
    x2js@3.1.0 \
    jxon@2.0.0-beta.4 \
    jsonml-tools@2.0.0 \
    https://github.com/Holzhaus/jsonml/archive/c8c15cc276eda15a85b67a4883196efe4528b171.tar.gz \
    https://github.com/Holzhaus/x2js/archive/d1a7c1995f0874504ca031ec6ee78607a60ffc27.tar.gz

# Install Ruby dependencies
RUN gem install cobravsmongoose --version '=0.0.2'

# Install PHP depencies
ENV COMPOSER_HOME /user/local/share/composer_home
COPY composer.json "${COMPOSER_HOME}/composer.json"
RUN composer global install --prefer-dist

# Install Mono/C# dependencies
RUN curl -OL https://github.com/JamesNK/Newtonsoft.Json/releases/download/10.0.3/Json100r3.zip && unzip -p Json100r3.zip Bin?net40?Newtonsoft.Json.dll > Newtonsoft.Json.dll && gacutil -i Newtonsoft.Json.dll -package NewtonsoftJson && rm Json100r3.zip Newtonsoft.Json.dll

# Install Python requirements
COPY requirements.txt /opt/xjcc/requirements.txt
RUN pip3 install -r /opt/xjcc/requirements.txt

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

COPY xjcc-x2jsabdmob /opt/xjcc/xjcc-x2jsabdmob
RUN cd /opt/xjcc/xjcc-x2jsabdmob && ./setup.py install

COPY xjcc-xmljson /opt/xjcc/xjcc-xmljson
RUN cd /opt/xjcc/xjcc-xmljson && ./setup.py install

COPY xjcc-cobravsmongoose /opt/xjcc/xjcc-cobravsmongoose
RUN cd /opt/xjcc/xjcc-cobravsmongoose && ./setup.py install

COPY xjcc-greencapexml /opt/xjcc/xjcc-greencapexml
RUN cd /opt/xjcc/xjcc-greencapexml && ./setup.py install

COPY xjcc-newtonsoftjson /opt/xjcc/xjcc-newtonsoftjson
RUN cd /opt/xjcc/xjcc-newtonsoftjson && ./setup.py install

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
