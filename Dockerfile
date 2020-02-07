FROM python:3.6.5
RUN mkdir -p /tukulsa-backend
COPY . /tukulsa-backend
RUN pip install -r /tukulsa-backend/requirements.txt
WORKDIR /tukulsa-backend
ENTRYPOINT [ "sh" ]
CMD [ "start.sh" ]
