FROM debian

WORKDIR /data
ADD . .

RUN apt update
RUN apt install --yes python3 python3-pip
RUN ls
RUN pip3 install --no-input -r requirements.txt
ENV FLASK_APP=bikeservice
RUN pip3 list
RUN flask init-db
EXPOSE 8080
ENTRYPOINT ["waitress-serve", "--call", "bikeservice:create_app"]
