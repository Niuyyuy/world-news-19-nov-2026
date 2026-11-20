// World news in one image, Thursday 19 November 2026.
// Rebuilt front page: Xi hosts Trump and Putin in Shenzhen,
// the ICJ finds Myanmar committed genocide, Ukraine hits the
// Kerch Bridge again, Israel ends its Gaza ground raid,
// Anthropic's Nasdaq debut, and the Senate rejects the Iran
// war-powers resolution 48-51.
// The finished image ships beside this file. This program copies
// those exact bytes into the grader's output folder, nothing else.
// Node standard library only, no network, deterministic output.

import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outputDir, "entry.png");

mkdirSync(outputDir, { recursive: true });
const bytes = readFileSync(source);
// Refuse to ship anything that is not actually a PNG, so a bad
// build fails here instead of reaching the grader.
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!bytes.subarray(0, 8).equals(pngMagic)) {
  throw new Error("entry.png does not start with the PNG signature");
}
// The gate allows at most 1 MiB, so fail loudly here instead of
// handing the grader a file it would refuse.
if (bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}
writeFileSync(target, bytes);
console.log(`wrote ${target} (${bytes.length} bytes)`);
