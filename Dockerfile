FROM ubuntu:14.04
# COPY AGEseq.pl /opt
# COPY blat /opt
ENV PATH="/opt:${PATH}"

RUN apt-get update
RUN apt-get -y install wget libcurl3
RUN wget https://raw.githubusercontent.com/TsailabBioinformatics/AGEseq/master/AGEseq/AGEseq.pl -P /opt/
RUN wget http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/blat/blat -P /opt/
RUN ["chmod", "+x", "/opt/blat"]
RUN mkdir data

CMD perl /opt/AGEseq.pl /data/reads /data/targets.txt /data/AGE_output.txt