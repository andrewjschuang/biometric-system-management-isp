FROM node:20-slim

WORKDIR /app

COPY package*.json ./
RUN npm install -g localtunnel && npm install

COPY . .

RUN npm run build

ENV PORT=5173
EXPOSE 5173

CMD ["npm", "run", "start"]