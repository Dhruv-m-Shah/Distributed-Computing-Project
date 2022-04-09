FROM ubuntu:20.04
RUN apt-get update --yes
RUN apt-get install cmake --yes
RUN apt-get install g++ --yes
COPY ./ ./
EXPOSE $PORT
RUN rm -rf build
RUN mkdir build
RUN cd build
RUN cmake ..
RUN cmake --build .
CMD ./src/CWF/main --http-address 0.0.0.0 --http-port $PORT