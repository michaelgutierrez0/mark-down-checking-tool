FROM python:3.11.5-alpine3.18

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./src/MarkDownTool-v0.0.1-alpha.py" ]
