FROM node:14-slim
LABEL authors="siddhant vijay singh"

WORKDIR /user/src/app
COPY ./package.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
