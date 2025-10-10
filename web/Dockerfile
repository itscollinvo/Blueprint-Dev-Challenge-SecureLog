# web/Dockerfile
FROM node:20-alpine

WORKDIR /app

# Corrected path: Copies package.json from the context root (./web)
COPY package*.json ./
RUN npm install

# Corrected path: Copies everything else from the context root (./web)
COPY . ./

EXPOSE 3000

CMD ["npm", "start"]