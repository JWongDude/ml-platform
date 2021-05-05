FROM continuumio/miniconda3

# Create Conda Environment
ADD environment.yml environment.yml
RUN conda env create -f environment.yml

# Activate it 
RUN echo "conda activate $(head -1 environment.yml | cut -d' ' -f2)" >> ~/.bashrc
ENV PATH /opt/conda/envs/$(head -1 environment.yml | cut -d' ' -f2)/bin:$PATH

# For LibGL Import Error (Pytorch-Tensorflow Conflict)
RUN apt-get update && apt-get install -y libgl1-mesa-dev

# For PyQt error 
RUN apt-get install libxi6 libgconf-2-4 -y

# For displaying GUI 
ENV DISPLAY=:0.0
ENV QT_PLUGIN_PATH=/usr/lib/qt/plugins

WORKDIR /app
COPY /app ./
ENTRYPOINT [ "conda", "run", "-n", "fresh_env", "xvfb-run", "python", "app.py" ]