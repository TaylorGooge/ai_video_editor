// Transparent overlay for a Short: header, designed cards, pane labels and captions.
// ffmpeg builds the cropped screen footage; this is composited on top.
import React from 'react';
import {AbsoluteFill, Sequence, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, INTER, labelStyle} from './theme';
import {ShortCaptions, Word} from './ShortCaptions';
import {VerticalTitleCard, VerticalTitleCardProps} from './VerticalTitleCard';
import {RowsCard} from './RowsCard';
import {EndCard, EndCardProps} from './EndCard';

export type Card =
	| {kind: 'title'; from: number; to: number; props: VerticalTitleCardProps}
	| {kind: 'rows'; from: number; to: number; props?: {label?: string; title?: string}}
	| {kind: 'end'; from: number; to: number; props?: EndCardProps};

export type PaneLabel = {text: string; x: number; y: number; from: number; to: number};

export type ShortOverlayProps = {
	durationInFrames: number;
	header: {label: string; title: string} | null; // null = no header (footage fills the frame)
	words: Word[];
	cards: Card[];
	labels: PaneLabel[];
	// Optional caption centre (px, 1080x1920 frame) per time range; default is the middle third.
	captionY?: {from: number; to: number; y: number}[];
};

const FADE = 5; // frames

const Fade: React.FC<{dur: number; first: boolean; children: React.ReactNode}> = ({dur, first, children}) => {
	const f = useCurrentFrame();
	const opacity = first
		? interpolate(f, [dur - FADE, dur], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})
		: interpolate(f, [0, FADE, dur - FADE, dur], [0, 1, 1, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	return <AbsoluteFill style={{opacity}}>{children}</AbsoluteFill>;
};

export const ShortOverlay: React.FC<ShortOverlayProps> = ({header, words, cards, labels, captionY}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const t = frame / fps;
	const onCard = cards.some((c) => t >= c.from && t < c.to);
	const capY = captionY?.find((r) => t >= r.from && t < r.to)?.y;

	return (
		<AbsoluteFill>
			{!onCard && header ? (
				<div style={{position: 'absolute', left: 96, right: 96, top: 120}}>
					<div style={{...labelStyle, fontSize: 26}}>{header.label}</div>
					<div style={{fontFamily: INTER, fontWeight: 700, fontSize: 58, color: C.paper, marginTop: 8}}>{header.title}</div>
				</div>
			) : null}

			{labels.map((l, i) =>
				t >= l.from && t < l.to ? (
					<div
						key={i}
						style={{
							position: 'absolute',
							left: l.x,
							top: l.y,
							padding: '6px 18px',
							borderRadius: 999,
							backgroundColor: C.panel,
							border: `2px solid ${C.border}`,
							fontFamily: INTER,
							fontWeight: 700,
							fontSize: 26,
							letterSpacing: '0.08em',
							color: C.paper,
						}}
					>
						{l.text}
					</div>
				) : null,
			)}

			{cards.map((c, i) => {
				const from = Math.round(c.from * fps);
				const dur = Math.round((c.to - c.from) * fps);
				const first = from === 0;
				return (
					<Sequence key={i} from={from} durationInFrames={dur}>
						<Fade dur={dur} first={first}>
							{c.kind === 'title' ? (
								<VerticalTitleCard {...c.props} />
							) : c.kind === 'end' ? (
								<EndCard {...(c.props ?? {})} />
							) : (
								<RowsCard {...(c.props ?? {})} />
							)}
						</Fade>
					</Sequence>
				);
			})}

			{cards.some((c) => c.kind === 'end' && t >= c.from) ? null : <ShortCaptions words={words} centerY={capY} />}
		</AbsoluteFill>
	);
};
