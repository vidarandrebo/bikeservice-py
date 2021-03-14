FROM archlinux

WORKDIR /data
ADD . .

RUN pacman -Sy
RUN pacman -S python python-pip --noconfirm
RUN ls
RUN pip install --no-input -r requirements.txt
ENV FLASK_APP=bikeservice
RUN pip list
RUN flask init-db
EXPOSE 8080
ENTRYPOINT ["waitress-serve", "--call", "bikeservice:create_app"]
