FROM ubuntu
RUN apt-get update
RUN apt-get -y install python-pip python-dev \
   libpq-dev libmysqlclient-dev libpq-dev \
   git libffi-dev netcat 
RUN git clone https://github.com/telefonicaid/fiware-cloto /opt/fiware-cloto
WORKDIR /opt/fiware-cloto/fiware_cloto/cloto/tests/acceptance
RUN pip install -r requirements.txt --allow-all-external
COPY configuration.py commons/configuration.py
COPY start.sh start.sh
CMD ./start.sh
