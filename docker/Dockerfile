FROM continuumio/miniconda3

RUN conda create -n myenv python=3.6
RUN echo "conda activate myenv" > ~/.bashrc

# +++ Python dependencies +++
ADD requirements.txt /opt/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r /opt/requirements.txt

# +++ Copy and untar source files +++
RUN mkdir /opt/app && \
    mkdir /opt/app/data
ADD app.tar /opt/app

ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf
ADD start_app.sh /opt
RUN chmod 700 /opt/start_app.sh
EXPOSE 8000
