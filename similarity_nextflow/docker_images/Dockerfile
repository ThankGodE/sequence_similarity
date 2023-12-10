FROM debian:latest

LABEL image.author.name "ThankGod Ebenezer"
LABEL image.author.email "tee25@cam.ac.uk"

MAINTAINER "ThankGod Ebenezer"

# define environment variables
ENV MINICONDA_DIR /opt/miniconda/
ENV BIN_LOCAL /usr/local/bin/


# Add environment variable to path
ENV PATH=$MINICONDA_DIR/bin:$PATH
ENV PATH=$BIN_LOCAL/bin/:$PATH

WORKDIR /work_directory/

COPY similarity_python/requirements.txt /work_directory/

# Install base utilities
RUN apt update && \
    apt install -y build-essential  && \
    apt install -y wget && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# install python
RUN apt update && \
    apt install -y python3 && \
    apt install -y python3-pip && \
    apt install -y python3.11-venv

RUN python3 -m venv venv && \
   . venv/bin/activate && \
   pip install --upgrade pip && \
   pip install -r requirements.txt

# Install anaconda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
     /bin/bash ~/miniconda.sh -b -p /opt/miniconda/

# anaconda installations
RUN conda update conda
RUN conda install -c bioconda cd-hit && \
    conda install -c bioconda ucsc-fatotab

# pip installations
RUN pip install biopython==1.81 && \
    pip install tqdm==4.66.1









