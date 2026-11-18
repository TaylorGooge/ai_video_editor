// Screen-recording scene for 16:9 long-form (edit-spec §5, §7).
// Plays pieces of one source clip (trim / speed / freeze), fits it into the safe area,
// and adds eased camera zooms, green highlight boxes (rest dimmed), red circles, masks and labels.
// All rects are in SOURCE pixels; times are in scene seconds.
import React from 'react';
import {AbsoluteFill, Easing, Freeze, Img, OffthreadVideo, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, INTER, MONO} from './theme';

export type Rect = [number, number, number, number];
export type Piece = {d: number; from: number; rate?: number}; // rate 0 = freeze on `from`
export type Label = {t0: number; t1?: number; text: string; x: number; y: number; kind?: 'red' | 'green' | 'panel' | 'mono' | 'lower'; sub?: string; size?: number};
export type ScreenProps = {
	src: string; // path under remotion/public, mp4 or png
	w: number; h: number; // source size
	pieces?: Piece[];
	cam?: {t: number; r: Rect}[]; // camera keyframes; first one is the start framing (default: whole source)
	hl?: {t0: number; t1: number; r: Rect; kind?: 'box' | 'circle' | 'soft'; dim?: boolean}[];
	masks?: {r: Rect; color: string; t0?: number; t1?: number}[]; // optional scene-time window
	labels?: Label[];
	area?: Rect; // display area on the 1920x1080 canvas
	logo?: boolean;
};

const AREA: Rect = [96, 120, 1728, 900]; // keeps the top-right logo corner and bottom margin clear
const EASE = Easing.bezier(0.45, 0, 0.55, 1);
const ZOOM_S = 0.5;

const camAt = (cam: {t: number; r: Rect}[], t: number): Rect => {
	let r = cam[0].r;
	for (let i = 1; i < cam.length; i++) {
		const k = cam[i];
		if (t <= k.t) break;
		const p = interpolate(t, [k.t, k.t + ZOOM_S], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: EASE});
		r = r.map((v, j) => v + (k.r[j] - v) * p) as Rect;
	}
	return r;
};

const fade = (t: number, t0: number, t1: number, d = 0.25) =>
	interpolate(t, [t0, t0 + d, t1 - d, t1], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

export const LabelView: React.FC<{l: Label; t: number}> = ({l, t}) => {
	const o = fade(t, l.t0, l.t1 ?? 1e9);
	if (o <= 0) return null;
	const base: React.CSSProperties = {position: 'absolute', left: l.x, top: l.y, opacity: o};
	if (l.kind === 'red' || l.kind === 'green')
		return (
			<div style={{...base, background: l.kind === 'red' ? C.red : C.green, color: C.ink, fontFamily: INTER, fontWeight: 700, fontSize: l.size ?? 26, textTransform: 'uppercase', letterSpacing: '0.06em', padding: '8px 20px', borderRadius: 999}}>
				{l.text}
			</div>
		);
	if (l.kind === 'lower')
		return (
			<div style={{...base, background: C.panel, borderLeft: `4px solid ${C.green}`, borderRadius: 12, padding: '20px 32px', border: `1px solid ${C.border}`, borderLeftWidth: 4, borderLeftColor: C.green}}>
				<div style={{fontFamily: INTER, fontWeight: 700, fontSize: 40, color: C.paper}}>{l.text}</div>
				{l.sub && <div style={{fontFamily: INTER, fontWeight: 500, fontSize: 28, color: C.muted, marginTop: 6}}>{l.sub}</div>}
			</div>
		);
	return (
		<div style={{...base, background: C.panel, border: `1px solid ${C.border}`, borderLeft: `4px solid ${C.green}`, borderRadius: 12, padding: '14px 24px', fontFamily: l.kind === 'mono' ? MONO : INTER, fontWeight: l.kind === 'mono' ? 400 : 700, fontSize: l.size ?? 34, color: C.paper, whiteSpace: 'pre'}}>
			{l.text}
			{l.sub && <div style={{fontFamily: INTER, fontWeight: 500, fontSize: 26, color: C.muted, marginTop: 4, whiteSpace: 'normal'}}>{l.sub}</div>}
		</div>
	);
};

export const Logo: React.FC = () => (
	<Img src={staticFile('brand/pbd-badge-A-padlock.png')} style={{position: 'absolute', right: 40, top: 40, height: 72, opacity: 0.75}} />
);

export const ScreenScene: React.FC<ScreenProps> = (p) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const t = frame / fps;
	const area = p.area ?? AREA;
	const cam = p.cam?.length ? p.cam : [{t: 0, r: [0, 0, p.w, p.h] as Rect}];
	const r = camAt(cam, t);
	const s = Math.min(area[2] / r[2], area[3] / r[3]);
	const ox = area[0] + area[2] / 2 - (r[0] + r[2] / 2) * s;
	const oy = area[1] + area[3] / 2 - (r[1] + r[3] / 2) * s;
	// visible window = camera rect, clipped to the display area
	const vw = Math.min(area[2], r[2] * s), vh = Math.min(area[3], r[3] * s);
	const clip: Rect = [area[0] + (area[2] - vw) / 2, area[1] + (area[3] - vh) / 2, vw, vh];
	const toScreen = (q: Rect): Rect => [ox + q[0] * s, oy + q[1] * s, q[2] * s, q[3] * s];
	const isImg = p.src.endsWith('.png');

	let acc = 0;
	const media = isImg ? (
		<Img src={staticFile(p.src)} style={{width: p.w, height: p.h}} />
	) : (
		(p.pieces ?? [{d: 999, from: 0, rate: 1}]).map((pc, i) => {
			const from = Math.round(acc * fps);
			const dur = Math.max(1, Math.round((acc + pc.d) * fps) - from);
			acc += pc.d;
			const v = <OffthreadVideo muted src={staticFile(p.src)} trimBefore={Math.round(pc.from * fps)} playbackRate={pc.rate === 0 ? 1 : pc.rate ?? 1} style={{width: p.w, height: p.h}} />;
			return (
				<Sequence key={i} from={from} durationInFrames={dur} layout="none">
					{pc.rate === 0 ? <Freeze frame={0}>{v}</Freeze> : v}
				</Sequence>
			);
		})
	);

	return (
		<AbsoluteFill style={{backgroundColor: C.ink}}>
			<div style={{position: 'absolute', left: clip[0], top: clip[1], width: clip[2], height: clip[3], overflow: 'hidden', borderRadius: 12, boxShadow: `0 0 0 1px ${C.border}`}}>
				<div style={{position: 'absolute', left: ox - clip[0], top: oy - clip[1], width: p.w, height: p.h, transform: `scale(${s})`, transformOrigin: '0 0'}}>
					{media}
					{(p.masks ?? []).map((m, i) =>
						t >= (m.t0 ?? -1) && t < (m.t1 ?? 1e9) ? (
							<div key={i} style={{position: 'absolute', left: m.r[0], top: m.r[1], width: m.r[2], height: m.r[3], background: m.color}} />
						) : null,
					)}
				</div>
				{(p.hl ?? []).map((h, i) => {
					const o = fade(t, h.t0, h.t1);
					if (o <= 0) return null;
					const pad = h.kind === 'circle' ? 14 : 8;
					const q = toScreen(h.r);
					const st: React.CSSProperties = {position: 'absolute', left: q[0] - pad - clip[0], top: q[1] - pad - clip[1], width: q[2] + pad * 2, height: q[3] + pad * 2, opacity: o, borderRadius: h.kind === 'circle' ? '50%' : 12};
					if (h.kind === 'circle') return <div key={i} style={{...st, border: `5px solid ${C.red}`}} />;
					return <div key={i} style={{...st, border: h.kind === 'soft' ? `3px solid ${C.green}AA` : `4px solid ${C.green}`, boxShadow: h.dim === false || h.kind === 'soft' ? undefined : `0 0 0 4000px rgba(13,17,23,0.6)`}} />;
				})}
			</div>
			{(p.labels ?? []).map((l, i) => <LabelView key={i} l={l} t={t} />)}
			{p.logo !== false && <Logo />}
		</AbsoluteFill>
	);
};
