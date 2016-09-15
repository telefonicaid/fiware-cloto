FROM ubuntu
RUN apt-get update
RUN apt-get -y install  python-dev \
   libpq-dev libmysqlclient-dev libpq-dev \
   git wget curl libffi-dev zip python-mysqldb\
   supervisor python-clips build-essential gcc
RUN curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
RUN python get-pip.py 
RUN git clone https://github.com/telefonicaid/fiware-cloto /opt/fiware-cloto
WORKDIR /opt/fiware-cloto
RUN mkdir /etc/fiware.d/
RUN mkdir /var/log/fiware-cloto
RUN pip install -r requirements.txt
RUN pip install virtualenv
COPY fiware-cloto.cfg /etc/fiware.d/fiware-cloto.cfg
COPY sonar-project.properties sonar-project.properties
CMD ./build.sh jenkins_build
