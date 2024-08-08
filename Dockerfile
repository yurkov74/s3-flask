FROM python:3.12

WORKDIR /usr/src/app

COPY requirements.txt s3flask/* ./

RUN \
  pip install --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt && \
  rm requirements.txt && \
  echo "done."

COPY . .

EXPOSE 5000