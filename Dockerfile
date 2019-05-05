FROM daknuett/python3-docker

ADD . /install
WORKDIR /install

RUN python3 setup.py install
RUN python3 -m pip install jupyter

RUN adduser notebooks
VOLUME /home/notebooks 
WORKDIR /home/notebooks

CMD su notebooks -c "jupyter notebook --ip=0.0.0.0 --port=8080"
