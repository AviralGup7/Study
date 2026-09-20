#!/usr/bin/env node
/* compile.mjs -- drive texlive.js's emscripten pdftex from Node.
 *
 *   node compile.mjs <texliveDir> <main.tex> <out.pdf> [passes]
 *
 * <texliveDir> is the directory that contains texmf-dist/, texmf-var/ and
 * texmf.cnf (i.e. node_modules/texlive/texlive). Its contents are mounted at /
 * inside the worker's MEMFS, so texmf-dist becomes /texmf-dist and kpathsea
 * finds everything.
 *
 * <main.tex> is read from the host; every sibling file in the same directory is
 * mounted next to it, so \includegraphics and \input of local files work.
 *
 * The PDF is read back out of MEMFS and written next to <main.tex>.
 *
 * Notes for whoever edits this:
 *  - There is no NODEFS in this build, so the ~3200-file tree has to be pushed
 *    in with FS_createPath + FS_createDataFile. Commands are fired without
 *    awaiting and flushed on one awaited message: the worker is single-threaded
 *    and FIFO, so awaiting the last of a batch guarantees all prior ones ran.
 *  - FS_createLazyFilesFromList uses XMLHttpRequest and is unusable in Node.
 *  - pre.js stringifies file bytes with String.fromCharCode, so the Node side
 *    must decode with Buffer.from(s, 'latin1') -- 'utf8' corrupts the PDF.
 *  - TeX's own "main memory size" is set by the format file, NOT by
 *    set_TOTAL_MEMORY. Raising TOTAL_MEMORY will not fix a capacity error.
 */
import Worker from 'web-worker';
import fs from 'fs';
import path from 'path';

const [texliveDirArg, mainTexArg, outPdfArg, passesArg] = process.argv.slice(2);
if (!texliveDirArg || !mainTexArg || !outPdfArg) {
  console.error('usage: node compile.mjs <texliveDir> <main.tex> <out.pdf> [passes]');
  process.exit(2);
}
const passes = Math.max(1, parseInt(passesArg || '2', 10));
const texliveDir = path.resolve(texliveDirArg);
const mainTex = path.resolve(mainTexArg);
const mainName = path.basename(mainTex);
const outName = path.basename(outPdfArg);
const hostOutDir = path.dirname(mainTex);

// node resolves bare specifiers relative to THIS file, so compile.mjs has to
// sit somewhere that can see node_modules/web-worker -- see setup.sh.
const here = path.dirname(new URL(import.meta.url).pathname);
const workerPath = fs.existsSync(path.join(here, 'node_modules/texlive/pdftex-worker.js'))
  ? path.join(here, 'node_modules/texlive/pdftex-worker.js')
  : path.resolve('node_modules/texlive/pdftex-worker.js');
if (!fs.existsSync(workerPath)) {
  console.error('cannot find ' + workerPath + ' -- run tools/latex/setup.sh first');
  process.exit(2);
}

const worker = new Worker(workerPath);
let nextId = 0;
const waiters = new Map();
let isReady = false;
const readyWaiters = [];
let sawError = false;
let fatal = false;

worker.onmessage = (ev) => {
  let d;
  try { d = JSON.parse(ev.data); } catch { return; }
  switch (d.command) {
    case 'ready':
      isReady = true;
      readyWaiters.splice(0).forEach((f) => f());
      break;
    case 'stdout':
      process.stdout.write('stdout: ' + d.contents + '\n');
      // pdftex prints this before bailing out; if we go on to FS_readFile the
      // missing file throws INSIDE the worker, it aborts, and no reply ever
      // comes back -- the caller hangs forever instead of seeing the failure.
      if (/no output PDF file produced|Fatal error occurred/.test(d.contents)) {
        fatal = true;
      }
      break;
    case 'stderr':
      process.stdout.write('stderr: ' + d.contents + '\n');
      break;
    case 'error':
      sawError = true;
      process.stdout.write('! ' + d.message + '\n');
      break;
    default: {
      const w = waiters.get(d.msg_id);
      if (w) { waiters.delete(d.msg_id); w(d.result); }
    }
  }
};
worker.onerror = (e) => { console.error('worker error: ' + (e.message || e)); process.exit(3); };

const whenReady = () => isReady ? Promise.resolve()
  : new Promise((r) => readyWaiters.push(r));

/** Send a command; resolve with its result when the worker answers. */
function send(command, args, await_it = true) {
  const msg_id = nextId++;
  const payload = JSON.stringify({ command, arguments: args, msg_id });
  if (!await_it) { worker.postMessage(payload); return Promise.resolve(); }
  return new Promise((resolve) => { waiters.set(msg_id, resolve); worker.postMessage(payload); });
}

function walk(dir, base, out) {
  for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, ent.name);
    const rel = base ? base + '/' + ent.name : ent.name;
    if (ent.isDirectory()) walk(full, rel, out);
    else if (ent.isFile()) out.push([rel, full]);
  }
}

async function main() {
  await whenReady();
  await send('set_TOTAL_MEMORY', [256 * 1024 * 1024]);

  // 1. the texlive tree -> /
  const tree = [];
  walk(texliveDir, '', tree);
  const dirs = new Set();
  for (const [rel] of tree) {
    const parts = rel.split('/');
    for (let i = 1; i < parts.length; i++) dirs.add(parts.slice(0, i).join('/'));
  }
  for (const d of [...dirs].sort()) await send('FS_createPath', ['/', d, true, true], false);
  await send('FS_createPath', ['/', 'tl-out', true, true]);          // flush point
  for (const [rel, full] of tree) {
    await send('FS_createDataFile',
      ['/' + path.posix.dirname(rel), path.posix.basename(rel),
       fs.readFileSync(full, 'latin1'), true, true], false);
  }

  // 2. the main .tex and every sibling file in its directory
  const srcDir = path.dirname(mainTex);
  for (const ent of fs.readdirSync(srcDir, { withFileTypes: true })) {
    if (!ent.isFile()) continue;
    const p = path.join(srcDir, ent.name);
    if (fs.statSync(p).size > 8 * 1024 * 1024) continue;             // skip huge assets
    await send('FS_createDataFile', ['/', ent.name, fs.readFileSync(p, 'latin1'), true, true], false);
  }
  await send('FS_createPath', ['/', 'srcflush', true, true]);        // flush point

  // 3. compile
  for (let i = 0; i < passes; i++) {
    await send('run', ['-interaction=nonstopmode', '-output-format', 'pdf', mainName]);
  }

  // 4. read the PDF back -- but never touch MEMFS if pdftex already failed,
  // or the worker aborts on the missing file and we hang (see onmessage).
  if (fatal || sawError) {
    console.log('no PDF produced: pdftex reported a fatal error');
    worker.terminate();
    process.exit(1);
  }
  const stem = mainName.replace(/\.tex$/, '');
  let data = null;
  for (const c of ['/' + outName.replace(/\.pdf$/, '') + '.pdf', '/' + stem + '.pdf']) {
    data = await send('FS_readFile', [c]);
    if (data) break;
  }
  if (!data) { console.log('no PDF produced'); worker.terminate(); process.exit(1); }
  const outPath = path.join(hostOutDir, outName);
  fs.writeFileSync(outPath, Buffer.from(data, 'latin1'));
  console.log('success: ' + outPath);
  worker.terminate();
  process.exit(sawError ? 1 : 0);
}

main().catch((e) => { console.error(e); process.exit(4); });
