FROM nginx:mainline-alpine
ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app

COPY nginx.conf /etc/nginx/nginx.conf
COPY /www /app
