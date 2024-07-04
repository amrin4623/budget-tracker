FROM python
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . .
ENV MONGODB_URL=${MONGODB_URL}
EXPOSE 5000
CMD [ "python3", "app.py" ]