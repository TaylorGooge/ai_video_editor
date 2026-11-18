// Claude Code-style terminal panels, re-typeset in brand fonts (not a pixel copy of the app).
// ClaudePrompt: a prompt being typed and submitted. ClaudeResponse: a streamed answer with timed highlights.
import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, INTER, MONO} from './theme';
import {Logo} from './ScreenScene';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

// **bold** and `code` inline markup
export const Rich: React.FC<{text: string}> = ({text}) => (
	<>
		{text.split(/(\*\*[^*]+\*\*|`[^`]+`)/g).map((part, i) =>
			part.startsWith('**') ? (
				<b key={i} style={{color: C.paper, fontWeight: 700}}><Rich text={part.slice(2, -2)} /></b>
			) : part.startsWith('`') ? (
				<span key={i} style={{color: '#A5D6FF'}}>{part.slice(1, -1)}</span>
			) : (
				<span key={i}>{part}</span>
			),
		)}
	</>
);

const Frame: React.FC<{children: React.ReactNode; title?: string}> = ({children, title}) => (
	<AbsoluteFill style={{backgroundColor: C.ink}}>
		<div style={{position: 'absolute', left: 96, top: 120, width: 1728, height: 900, background: '#0A0D12', border: `1px solid ${C.border}`, borderRadius: 12, overflow: 'hidden'}}>
			<div style={{height: 52, borderBottom: `1px solid ${C.border}`, display: 'flex', alignItems: 'center', padding: '0 24px', gap: 10, background: C.panel}}>
				{[C.border, C.border, C.border].map((c, i) => <div key={i} style={{width: 14, height: 14, borderRadius: 7, background: c}} />)}
				<div style={{fontFamily: MONO, fontSize: 22, color: C.muted, marginLeft: 16}}>{title ?? 'claude · ~/app'}</div>
			</div>
			<div style={{padding: '36px 48px'}}>{children}</div>
		</div>
		<Logo />
	</AbsoluteFill>
);

export type ClaudePromptProps = {text: string; typeStart: number; cps: number; enterAt: number; title?: string; size?: number};

export const ClaudePrompt: React.FC<ClaudePromptProps> = ({text, typeStart, cps, enterAt, title, size = 36}) => {
	const t = useCurrentFrame() / useVideoConfig().fps;
	const n = Math.floor(Math.max(0, t - typeStart) * cps);
	const typed = text.slice(0, Math.min(text.length, n));
	const sent = t >= enterAt;
	const caret = Math.floor(t * 2) % 2 === 0;
	const dots = '·'.repeat(1 + (Math.floor(t * 3) % 3));
	const box: React.CSSProperties = {border: `2px solid ${C.border}`, borderRadius: 12, padding: '22px 28px', fontFamily: MONO, fontSize: size, color: C.paper, lineHeight: 1.45, whiteSpace: 'pre-wrap'};
	return (
		<Frame title={title}>
			{sent && (
				<div style={{fontFamily: MONO, fontSize: size, color: C.muted, lineHeight: 1.45, whiteSpace: 'pre-wrap', marginBottom: 36, opacity: interpolate(t, [enterAt, enterAt + 0.2], [0, 1], clamp)}}>
					<span style={{color: C.green}}>{'> '}</span>
					{text}
					<div style={{marginTop: 28, color: C.amber, fontSize: size * 0.85}}>✻ Working {dots}</div>
				</div>
			)}
			<div style={box}>
				<span style={{color: C.green}}>{'> '}</span>
				{sent ? '' : typed}
				<span style={{opacity: caret ? 1 : 0, background: C.paper, display: 'inline-block', width: size * 0.55, height: size * 1.1, verticalAlign: 'text-bottom', marginLeft: 2}} />
			</div>
		</Frame>
	);
};

export type Block = {text: string; bullet?: boolean; indent?: number; gap?: number};
export type ClaudeResponseProps = {prompt?: string; blocks: Block[]; streamStart: number; streamDur: number; hl?: {t0: number; t1: number; blocks: number[]}[]; size?: number; title?: string};

export const ClaudeResponse: React.FC<ClaudeResponseProps> = ({prompt, blocks, streamStart, streamDur, hl = [], size = 27, title}) => {
	const t = useCurrentFrame() / useVideoConfig().fps;
	const shown = interpolate(t, [streamStart, streamStart + streamDur], [0, blocks.length], clamp);
	const active = hl.filter((h) => t >= h.t0 && t < h.t1);
	const on = new Set(active.flatMap((h) => h.blocks));
	const dimLevel = active.length ? interpolate(Math.min(...active.map((h) => Math.min(t - h.t0, h.t1 - t))), [0, 0.25], [0, 1], clamp) : 0;
	return (
		<Frame title={title}>
			{prompt && (
				<div style={{fontFamily: MONO, fontSize: size, color: C.muted, marginBottom: 24, opacity: 1 - dimLevel * 0.5}}>
					<span style={{color: C.green}}>{'> '}</span>
					{prompt}
				</div>
			)}
			{blocks.map((b, i) => {
				const vis = interpolate(shown - i, [0, 1], [0, 1], clamp);
				if (vis <= 0) return null;
				const isOn = on.has(i);
				return (
					<div
						key={i}
						style={{
							display: 'flex', gap: 14, fontFamily: MONO, fontSize: size, lineHeight: 1.42, color: '#C9D1D9', marginTop: b.gap ?? 10,
							marginLeft: (b.indent ?? 0) * 40, opacity: vis * (isOn ? 1 : 1 - dimLevel * 0.62),
							padding: '4px 14px', borderLeft: `4px solid ${isOn ? C.green : 'transparent'}`, borderRadius: 6,
							background: isOn ? `rgba(63,185,80,${0.1 * dimLevel})` : 'transparent',
						}}
					>
						{b.bullet ? <span style={{color: C.muted}}>-</span> : !b.indent && i === 0 ? <span style={{color: C.paper}}>●</span> : null}
						<span style={{whiteSpace: 'pre-wrap'}}>
							<Rich text={b.text} />
						</span>
					</div>
				);
			})}
		</Frame>
	);
};
