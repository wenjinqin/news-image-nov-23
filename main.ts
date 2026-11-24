// Entry program for make.fun news-image-20261123: "Sum up 23 November's
// world news in one image".
//
// The front page itself is entry.png in this same directory (drawn by
// draw23.py). This program does no drawing and needs no network: it
// checks the picture against the contest gate, then places an exact
// copy at $MAKEFUN_OUTPUT_DIR/entry.png (or /output/entry.png when the
// variable is unset). The grader runs this twice and both runs must
// produce identical bytes, so the checked file is copied as-is.
//
// Node 22, standard library only.

import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const MAX_BYTES = 1_048_576;
const MAX_SIDE = 1024;

const PNG_SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
const PNG_IEND = [0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82];

function fail(message) {
  throw new Error(`entry.png failed validation: ${message}`);
}

// Read the width and height out of a PNG's IHDR chunk (bytes 16-23).
function pngDimensions(data) {
  return {
    width: data.readUInt32BE(16),
    height: data.readUInt32BE(20),
  };
}

function validateImage(data, sourcePath) {
  if (data.length === 0) {
    fail(`no bytes read from ${sourcePath}`);
  }
  if (data.length < 8) {
    fail(`only ${data.length} bytes read from ${sourcePath}, too short to identify`);
  }
  if (data.length > MAX_BYTES) {
    fail(`${data.length} bytes exceeds the 1 MiB limit`);
  }

  const looksPng = PNG_SIGNATURE.every((byte, i) => data[i] === byte);
  const looksJpeg =
    data[0] === 0xff &&
    data[1] === 0xd8 &&
    data[data.length - 2] === 0xff &&
    data[data.length - 1] === 0xd9;
  if (!looksPng && !looksJpeg) {
    fail('first bytes match neither PNG nor JPEG');
  }

  if (looksPng) {
    if (data.length < 33) {
      fail('file is too short to hold a PNG header and IEND chunk');
    }
    // Bytes 12-15 must spell IHDR: without it the width/height fields
    // at 16-23 are meaningless, so refuse to trust them.
    const chunkType = data.subarray(12, 16).toString('latin1');
    if (chunkType !== 'IHDR') {
      fail(`first PNG chunk is ${JSON.stringify(chunkType)}, not IHDR`);
    }
    const { width, height } = pngDimensions(data);
    if (width > MAX_SIDE || height > MAX_SIDE) {
      fail(`dimensions ${width}x${height} exceed the ${MAX_SIDE}x${MAX_SIDE} limit`);
    }
    const tailMatches = PNG_IEND.every(
      (byte, i) => data[data.length - PNG_IEND.length + i] === byte,
    );
    if (!tailMatches) {
      fail('PNG does not end with a complete IEND chunk');
    }
    return { format: 'PNG', width, height };
  }
  return { format: 'JPEG', width: null, height: null };
}

const repoRoot = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(repoRoot, 'entry.png');
if (!existsSync(sourcePath)) {
  fail(`expected image file is missing: ${sourcePath}`);
}
const image = readFileSync(sourcePath);
const info = validateImage(image, sourcePath);

const outputDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';
mkdirSync(outputDir, { recursive: true });
const targetPath = join(outputDir, 'entry.png');
writeFileSync(targetPath, image);

// Prove the file the judge will see is exactly the file that was
// validated: read it back and compare every byte.
const delivered = readFileSync(targetPath);
if (delivered.length !== image.length || !delivered.equals(image)) {
  throw new Error(
    `output mismatch: ${targetPath} (${delivered.length} bytes) is not ` +
      `identical to the validated source (${image.length} bytes)`,
  );
}

const sizeNote =
  info.format === 'PNG' ? `, ${info.width}x${info.height}` : '';
console.log(
  `delivered ${info.format} entry.png (${image.length} bytes${sizeNote}) to ${targetPath}`,
);
