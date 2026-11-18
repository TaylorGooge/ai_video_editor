// Designed 16:9 cards for long-form (edit-spec §6): series, chapter, prompt, query, code stack,
// checklist, step list, outro. Times are scene seconds.
import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, INTER, MONO, gridBg, labelStyle} from './theme';
import {Rich} from './ClaudeUI';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const useT = () => useCurrentFrame() / useVideoConfig().fps;
const inAt = (t: number, t0: number, d = 0.35) => interpolate(t, [t0, t0 + d], [0, 1], clamp);

export const SeriesCard: React.FC<{title: string; beats: string[]}> = ({title, beats}) => {
	const t = useT();
	return (
		<AbsoluteFill style={{...gridBg, padding: '0 160px', justifyContent: 'center'}}>
			<div style={{...labelStyle, opacity: inAt(t, 0)}}>The AI Did What You Asked</div>
			<div style={{fontFamily: INTER, fontWeight: 700, fontSize: 80, color: C.paper, lineHeight: 1.12, marginTop: 24, opacity: inAt(t, 0.15)}}>{title}</div>
			<div style={{display: 'flex', flexWrap: 'wrap', gap: 16, marginTop: 56}}>
				{beats.map((b, i) => (
					<div key={i} style={{fontFamily: INTER, fontWeight: 500, fontSize: 28, color: C.muted, border: `1px solid ${C.border}`, background: C.panel, borderRadius: 999, padding: '10px 24px', opacity: inAt(t, 0.5 + i * 0.18)}}>
						<span style={{color: C.green, marginRight: 10}}>{i + 1}</span>
						{b}
					</div>
				))}
			</div>
		</AbsoluteFill>
	);
};

export const ChapterCard: React.FC<{label: string; title: string}> = ({label, title}) => {
	const t = useT();
	return (
		<AbsoluteFill style={{...gridBg, padding: '0 160px', justifyContent: 'center'}}>
			<div style={{...labelStyle, opacity: inAt(t, 0)}}>{label}</div>
			<div style={{fontFamily: INTER, fontWeight: 700, fontSize: 72, color: C.paper, marginTop: 20, lineHeight: 1.15, opacity: inAt(t, 0.12), transform: `translateY(${(1 - inAt(t, 0.12)) * 16}px)`}}>
				<Rich text={title} />
			</div>
		</AbsoluteFill>
	);
};

// Prompt / query card: Panel with green bar, label, mono body revealed by typing at `cps`.
// `top` (px) pins the card's top edge instead of centring it, so it doesn't drift while it types (Shorts).
export const PromptCard: React.FC<{label: string; title?: string; body: string; cps: number; size?: number; note?: string; columns?: number; top?: number}> = ({label, title, body, cps, size = 32, note, columns = 1, top}) => {
	const t = useT();
	const n = Math.floor(Math.max(0, t - 0.4) * cps);
	return (
		<AbsoluteFill style={{...gridBg, padding: top === undefined ? '60px 96px' : `${top}px 72px 60px`, justifyContent: top === undefined ? 'center' : 'flex-start'}}>
			<div style={{background: C.panel, border: `1px solid ${C.border}`, borderLeft: `4px solid ${C.green}`, borderRadius: 12, padding: '40px 52px', opacity: inAt(t, 0)}}>
				<div style={{fontFamily: INTER, fontWeight: 700, fontSize: 24, letterSpacing: '0.12em', textTransform: 'uppercase', color: C.green}}>{label}</div>
				{title && <div style={{fontFamily: INTER, fontWeight: 700, fontSize: 40, color: C.paper, marginTop: 10}}>{title}</div>}
				<div style={{fontFamily: MONO, fontSize: size, color: C.paper, lineHeight: 1.45, marginTop: 24, whiteSpace: 'pre-wrap', columnCount: columns, columnGap: 64}}>
					{body.slice(0, n)}
					{n < body.length && <span style={{background: C.paper, display: 'inline-block', width: size * 0.55, height: size * 1.05, verticalAlign: 'text-bottom'}} />}
				</div>
			</div>
			{note && (
				<div style={{alignSelf: 'flex-start', marginTop: 24, background: C.green, color: C.ink, fontFamily: INTER, fontWeight: 700, fontSize: 24, letterSpacing: '0.06em', textTransform: 'uppercase', padding: '8px 20px', borderRadius: 999, opacity: inAt(t, 0.6 + body.length / cps)}}>
					{note}
				</div>
			)}
		</AbsoluteFill>
	);
};

// Stacked code snippets; each lights up at `on`, pills appear at `pillAt`.
export const CodeStack: React.FC<{items: {file: string; code: string; on: number; pill: string}[]; pillAt: number; title?: string}> = ({items, pillAt, title}) => {
	const t = useT();
	const anyOn = items.some((it) => t >= it.on);
	return (
		<AbsoluteFill style={{...gridBg, padding: '0 140px', justifyContent: 'center', gap: 28}}>
			{title && <div style={{...labelStyle, marginBottom: 4}}>{title}</div>}
			{items.map((it, i) => {
				const lit = inAt(t, it.on, 0.3);
				return (
					<div key={i} style={{background: C.panel, border: `1px solid ${C.border}`, borderLeft: `4px solid ${lit > 0.5 ? C.green : C.border}`, borderRadius: 12, padding: '22px 32px', opacity: anyOn ? 0.45 + 0.55 * lit : 1, display: 'flex', alignItems: 'center', gap: 28}}>
						<div style={{flex: 1}}>
							<div style={{fontFamily: MONO, fontSize: 24, color: C.muted}}>{it.file}</div>
							<div style={{fontFamily: MONO, fontSize: 36, color: C.paper, marginTop: 8, whiteSpace: 'pre'}}><Rich text={it.code} /></div>
						</div>
						<div style={{background: C.red, color: C.ink, fontFamily: INTER, fontWeight: 700, fontSize: 24, textTransform: 'uppercase', letterSpacing: '0.06em', padding: '8px 18px', borderRadius: 999, opacity: inAt(t, pillAt + i * 0.25), whiteSpace: 'nowrap'}}>{it.pill}</div>
					</div>
				);
			})}
		</AbsoluteFill>
	);
};

export const Checklist: React.FC<{title?: string; items: {text: string; at: number}[]; doneAt: number; done: number}> = ({title, items, doneAt, done}) => {
	const t = useT();
	return (
		<AbsoluteFill style={{...gridBg, padding: '0 200px', justifyContent: 'center', gap: 26}}>
			{title && <div style={{...labelStyle, opacity: inAt(t, 0)}}>{title}</div>}
			{items.map((it, i) => {
				const o = inAt(t, it.at);
				const mark = inAt(t, doneAt + i * 0.2);
				const ok = i < done;
				return (
					<div key={i} style={{display: 'flex', alignItems: 'center', gap: 28, opacity: o, transform: `translateX(${(1 - o) * -20}px)`}}>
						<div style={{width: 56, height: 56, borderRadius: 12, border: `3px solid ${mark > 0.5 ? (ok ? C.green : C.amber) : C.border}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: INTER, fontWeight: 700, fontSize: 36, color: ok ? C.green : C.amber}}>
							<span style={{opacity: mark}}>{ok ? '✓' : '!'}</span>
						</div>
						<div style={{fontFamily: INTER, fontWeight: 700, fontSize: 60, color: C.paper}}>{it.text}</div>
						{!ok && <div style={{fontFamily: INTER, fontWeight: 500, fontSize: 28, color: C.amber, opacity: mark}}>not done</div>}
					</div>
				);
			})}
		</AbsoluteFill>
	);
};

// Five-step list; `active` = [{t, i}] which step is lit from time t; `subs` appear under step `subOf`.
export const StepList: React.FC<{title?: string; steps: string[]; active: {t: number; i: number}[]; subs?: {text: string; at: number}[]; subOf?: number}> = ({title, steps, active, subs = [], subOf = 0}) => {
	const t = useT();
	let cur = -1;
	for (const a of active) if (t >= a.t) cur = a.i;
	return (
		<AbsoluteFill style={{...gridBg, padding: '0 180px', justifyContent: 'center'}}>
			{title && <div style={{...labelStyle, marginBottom: 28}}>{title}</div>}
			{steps.map((s, i) => {
				const lit = i === cur;
				return (
					<div key={i}>
						<div style={{display: 'flex', alignItems: 'baseline', gap: 26, padding: '12px 0', opacity: cur < 0 || lit ? 1 : 0.38}}>
							<div style={{fontFamily: INTER, fontWeight: 700, fontSize: 44, color: lit ? C.green : C.muted, width: 40}}>{i + 1}</div>
							<div style={{fontFamily: INTER, fontWeight: 700, fontSize: 52, color: C.paper}}>{s}</div>
						</div>
						{i === subOf && lit &&
							subs.map((sb, j) => (
								<div key={j} style={{marginLeft: 66, fontFamily: INTER, fontWeight: 500, fontSize: 34, color: C.muted, padding: '4px 0', opacity: inAt(t, sb.at)}}>
									<span style={{color: C.green, marginRight: 14}}>·</span>
									{sb.text}
								</div>
							))}
					</div>
				);
			})}
		</AbsoluteFill>
	);
};

export const Outro: React.FC = () => <Img src={staticFile('brand/pbd-scene-bg-1920x1080.png')} style={{width: 1920, height: 1080}} />;
