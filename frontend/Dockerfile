FROM node:20-bullseye

RUN npm install -g http-server

WORKDIR /app

COPY . .

RUN rm -rf node_modules package-lock.json

RUN npm install

EXPOSE 80
CMD [ "npm", "run", "dev" ]


# RUN npm run build
# EXPOSE 8080
# CMD [ "http-server", "dist" ]
