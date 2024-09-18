from quay.io/jupyter/base-notebook

USER ${NB_UID}

COPY requirements.txt /home/jovyan/
COPY ./setup.py /home/jovyan/
COPY ./hpc4ag/* /home/jovyan/hpc4ag/
COPY Notebooks/ML-cropID/GeoDeepLearningTutorial.ipynb /home/jovyan/
COPY Notebooks/Parallel-SNP/*.ipynb /home/jovyan/

USER root

RUN apt-get update -y && \
  apt-get install -y gdal-bin libgdal-dev libgeos-dev libproj-dev

USER ${NB_UID}

RUN pip install -r /home/jovyan/requirements.txt 
#  pip install /home/jovyan/

USER root

RUN apt-get clean && \
  apt-get autoclean && \
  apt-get autoremove --purge 

USER ${NB_UID}

CMD [ "/usr/local/bin/start-notebook.py"]