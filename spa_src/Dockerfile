FROM node:12

WORKDIR /app

COPY package.json /app/
RUN npm install

COPY src/* /app/src/
COPY public/* /app/public/

CMD ["npm", "start"]
