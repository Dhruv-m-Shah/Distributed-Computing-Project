FROM ubuntu:20.04
RUN apt-get update --yes
RUN apt-get install cmake --yes
RUN apt-get install g++ --yes
COPY ./ ./
EXPOSE 8080
RUN rm -r build
RUN mkdir build
RUN cd build
RUN cmake ..
RUN cmake --build .
CMD ./src/CWF/main