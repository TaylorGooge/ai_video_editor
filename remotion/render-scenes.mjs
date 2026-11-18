// Render long-form scenes one by one (bundle once). Skips scenes whose props haven't changed.
// node render-scenes.mjs <scenes.json> <outDir> <scale> [only-id,...]
// scenes.json: [{id, props:{kind, dur, ...}}]. Concurrency 2 (weak machine, see CLAUDE.md).
import {bundle} from '@remotion/bundler';
import {renderMedia, selectComposition} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const [scenesFile, outDir, scaleArg, only] = process.argv.slice(2);
const scale = scaleArg === '720' ? 2 / 3 : Number(scaleArg || 1);
const scenes = JSON.parse(fs.readFileSync(scenesFile, 'utf8'));
fs.mkdirSync(outDir, {recursive: true});
const want = only ? new Set(only.split(',')) : null;
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts')});
for (const s of scenes) {
	if (want && !want.has(s.id)) continue;
	const out = path.join(outDir, `${s.id}.mp4`);
	const hash = crypto.createHash('md5').update(JSON.stringify(s.props) + scale).digest('hex');
	const hf = out + '.hash';
	if (fs.existsSync(out) && fs.existsSync(hf) && fs.readFileSync(hf, 'utf8') === hash) continue;
	const t0 = Date.now();
	const composition = await selectComposition({serveUrl, id: 'LongScene', inputProps: s.props});
	await renderMedia({composition, serveUrl, codec: 'h264', outputLocation: out, inputProps: s.props, scale, concurrency: 2,
		crf: scale < 1 ? 20 : 18, x264Preset: scale < 1 ? 'veryfast' : 'slow', muted: true, offthreadVideoCacheSizeInBytes: 512 * 1024 * 1024});
	fs.writeFileSync(hf, hash);
	console.log(`${s.id} ${s.props.kind} ${s.props.dur}s in ${((Date.now() - t0) / 1000).toFixed(0)}s`);
}
