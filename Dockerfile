FROM pytorch/pytorch:1.2-cuda10.0-cudnn7-runtime

RUN python -c "import torch; print(torch.__version__)"
RUN pip install torchvision==0.4.0

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD python test_seq_style.py