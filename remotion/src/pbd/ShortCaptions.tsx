// Burned-in Shorts captions (edit-spec-v1 §9): Inter Bold, Paper on Panel @75%,
// current word green, 2–4 words per caption, max 2 lines, middle third.
import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {C, INTER} from './theme';

export type Word = {w: string; start: number; end: number}; // seconds, output timeline

const MAX_WORDS = 4;
const GAP_BREAK = 0.45; // a pause this long starts a new caption

export const chunkWords = (words: Word[]): Word[][] => {
	const chunks: Word[][] = [];
	let cur: Word[] = [];
	words.forEach((wd, i) => {
		const prev = words[i - 1];
		const breakHere =
			cur.length >= MAX_WORDS ||
			(prev && wd.start - prev.end > GAP_BREAK) ||
			(prev && /[.?!,:;]$/.test(prev.w) && cur.length >= 2) ||
			(prev && /[.?!]$/.test(prev.w));
		if (cur.length && breakHere) {
			chunks.push(cur);
			cur = [];
		}
		cur.push(wd);
	});
	if (cur.length) chunks.push(cur);
	return chunks;
};

export const ShortCaptions: React.FC<{words: Word[]; centerY?: number; fontSize?: number}> = ({
	words,
	centerY = 1225,
	fontSize = 68,
}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const t = frame / fps;
	const chunks = React.useMemo(() => chunkWords(words), [words]);

	const idx = chunks.findIndex((c, i) => {
		const start = c[0].start;
		const next = chunks[i + 1];
		const end = next ? Math.min(next[0].start, c[c.length - 1].end + 0.6) : c[c.length - 1].end + 0.6;
		return t >= start && t < end;
	});
	if (idx < 0) return null;
	const chunk = chunks[idx];

	return (
		<div
			style={{
				position: 'absolute',
				left: 0,
				right: 0,
				top: centerY,
				transform: 'translateY(-50%)',
				display: 'flex',
				justifyContent: 'center',
			}}
		>
			<div
				style={{
					maxWidth: 920,
					padding: '14px 30px',
					borderRadius: 12,
					backgroundColor: 'rgba(22, 27, 34, 0.75)',
					fontFamily: INTER,
					fontWeight: 700,
					fontSize,
					lineHeight: 1.18,
					textAlign: 'center',
					color: C.paper,
				}}
			>
				{chunk.map((wd, i) => {
					const next = chunk[i + 1];
					const active = t >= wd.start && (next ? t < next.start : true);
					return (
						<span key={i} style={{color: active ? C.green : C.paper}}>
							{wd.w}
							{i < chunk.length - 1 ? ' ' : ''}
						</span>
					);
				})}
			</div>
		</div>
	);
};
