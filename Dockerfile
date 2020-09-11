FROM pytorch/pytorch:1.2-cuda10.0-cudnn7-runtime

RUN apt-get update
RUN apt-get install -y apt-file
RUN apt-file update
RUN apt-file search libgthread-2.0.so.0
RUN apt-get install -y libglib2.0-0 libsm6 libxext6 libxrender-dev

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
WORKDIR ./Generation
RUN mkdir -p ./Drawing/examples

EXPOSE 80
CMD python ./Server/server.py