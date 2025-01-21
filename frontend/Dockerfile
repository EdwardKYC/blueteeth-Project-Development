# Frontend Dockerfile
FROM node:18

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install --save-dev

COPY . .

RUN npm run build
CMD ["npm", "run", "dev"]