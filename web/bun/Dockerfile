FROM jarredsumner/bun:edge
WORKDIR /home/ahmedreda2009/app
COPY package.json package.json
COPY bun.lockb bun.lockb
RUN bun install
COPY . .
EXPOSE 3000
ENTRYPOINT ["bun", "index.js"]