FROM node:latest

WORKDIR /app
COPY ./package.json .
RUN yarn
COPY . .

RUN chown -R node:node /app 
USER node
RUN echo "IngeHack{4lw4ys-w1th-pr0t0-72187312}" > flag.txt
RUN chmod 444 flag.txt

EXPOSE 3000
CMD ["node", "server.js"]
