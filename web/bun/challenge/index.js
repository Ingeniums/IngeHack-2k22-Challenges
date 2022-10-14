import { serve } from "bun";
import { fileURLToPath } from "url";
import { readFileSync } from "fs";
import { parse } from "qs";

serve({
   fetch(req) {
    const query = req?.url.split("?")[1];
    const { file } = parse(query);
    if (file) {
      let content;
      if (JSON.stringify(file).includes("flag")) {
        return new Response(":(", { status: 400 });
      }
      try {
        content = readFileSync(fileURLToPath(file));
      } catch (err) {
        console.log(err);
      }
      return new Response(content, { status: 200 });
    }
    return new Response("Hello world", { status: 200 });
  },
  development: process.env.NODE_ENV !== "production",
  port: 3000,
});
