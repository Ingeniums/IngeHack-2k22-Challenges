import express from "express";
import { exec } from "child_process";
import { createHash } from "crypto";

const PORT = 3000;
const app = express();
const STORE = new Map();
const redis_commands = {
  get: 'redis-cli -p 6379 GET "*"',
  set: "redis-cli -p 6379 SET key value",
};

const generateOtp = (username) =>
  createHash("sha256")
    .update(`${username}-${Math.random().toString()}`)
    .digest("hex");

const encodeString = (str) => createHash("md5").update(str).digest("base64");

app.get("/get*", (req, res) =>
  res.json(
    Array.from(STORE).map(([k, v]) => {
      return { [k]: v };
    })
  )
);

app.get("/set*", (req, res) => {
  let {
    query: { otp, username, key, value },
  } = req;
  if (otp && otp.length < 5 && otp in STORE) {
    otp = generateOtp(username);
    if (!STORE.has(otp)) {
      const obj = {};
      obj[username][key] = value;
      STORE.set(otp, obj);
    }
    return res.json({ success: true });
  }
  return res.json({ success: false });
});

app.trace("/cache*", (req, res) => {
  const store = JSON.stringify(
    Array.from(STORE).map(([k, v]) => {
      return { [k]: v };
    })
  );
  if (redis_commands?.secret_command) {
    exec(
      redis_commands?.secret_command + `cache ${encodeString(store)}`,
      (err) => {
        if (err) {
          return res.json({ success: false });
        }
      }
    );
  }
});

app.listen(PORT, () => console.log(`Listening on port ${PORT}`));
