// World news in one image, Thursday 19 November 2026.
// Front page: Trump, Xi and Putin meet in Shenzhen, Crimea
// bridge attacked again, Israel launches Gaza ground operation,
// Anthropic's record $81.3bn IPO, Van Gogh sells for $190.4m,
// and Estonia to close its Russia border.
// This program ships the finished front page beside it and writes
// exactly those bytes to the grader's output folder, every run.
// It uses only the Node standard library, reads no network, and
// writes nothing else, so two runs produce identical output.

import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outputDir, "entry.png");

mkdirSync(outputDir, { recursive: true });
const bytes = readFileSync(source);
// The competition gate allows at most 1 MiB; fail loudly here
// rather than submitting a file the gate would refuse.
if (bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}
writeFileSync(target, bytes);
console.log(`wrote ${target} (${bytes.length} bytes)`);
