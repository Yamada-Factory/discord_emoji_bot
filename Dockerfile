FROM debian:buster

RUN apt-get update && apt-get install git cmake g++ python libfontconfig1-dev \
    libx11-dev libxcomposite-dev libgl1-mesa-dev libglu1-mesa-dev freeglut3-dev ca-certificates fontconfig \
    python3 python3-pip -y
RUN git clone https://github.com/emoji-gen/emojilib.git
WORKDIR emojilib
RUN git submodule update --init --recursive && \
    cd externals/libemoji && \
    cmake . && \
    make


FROM python:3.9-buster

RUN apt-get update && apt-get install git libgl1-mesa-dev libglu1-mesa-dev -y
RUN git clone https://github.com/emoji-gen/emojilib.git

COPY --from=0 /emojilib/externals/libemoji/lib /emojilib/externals/libemoji/lib
COPY --from=0 /emojilib/externals/libemoji/include /emojilib/externals/libemoji/include

WORKDIR emojilib
RUN pip3 install cython py-cord
RUN python setup.py install
RUN python3 -m pip install -U git+https://github.com/Pycord-Development/pycord
WORKDIR /app

ADD fonts /app/fonts
ADD main.py /app
CMD python main.py
