// 9:16 "one box vs one row per post" card (vertical version of the long-form fix card).
import React from 'react';
import {AbsoluteFill, Img, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, INTER, gridBg, labelStyle} from './theme';

const NAMES = ['Maria', 'Dev', 'Priya', 'Sam', 'Alex', 'Maria', 'Sam', 'Dev', 'Priya', 'Alex', 'Maria', 'Sam', 'Dev', 'Priya', 'Alex', 'Maria'];

const Pill: React.FC<{text: string; color: string; dim?: boolean}> = ({text, color, dim}) => (
	<span
		style={{
			display: 'inline-block',
			padding: '6px 16px',
			borderRadius: 999,
			backgroundColor: color,
			color: C.ink,
			fontFamily: INTER,
			fontWeight: 700,
			fontSize: 24,
			letterSpacing: '0.06em',
			textTransform: 'uppercase',
			opacity: dim ? 0.45 : 1,
		}}
	>
		{text}
	</span>
);

export const RowsCard: React.FC<{label?: string; title?: string}> = ({
	label = 'The fix',
	title = 'Give every post its own row',
}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();

	return (
		<AbsoluteFill style={gridBg}>
			<div style={{position: 'absolute', left: 96, right: 96, top: 150}}>
				<div style={labelStyle}>{label}</div>
				<div style={{fontFamily: INTER, fontWeight: 700, fontSize: 80, lineHeight: 1.08, color: C.paper, marginTop: 18}}>{title}</div>
			</div>

			{/* Before: the whole app in one row (dimmed) */}
			<div style={{position: 'absolute', left: 96, right: 96, top: 440, opacity: 0.5}}>
				<Pill text="One row" color={C.red} dim />
				<div
					style={{
						marginTop: 14,
						height: 92,
						borderRadius: 12,
						border: `2px solid ${C.red}66`,
						backgroundColor: C.panel,
						display: 'flex',
						alignItems: 'center',
						paddingLeft: 28,
						fontFamily: INTER,
						fontWeight: 700,
						fontSize: 36,
						color: C.muted,
					}}
				>
					the whole app
				</div>
			</div>

			{/* After: one row per post */}
			<div style={{position: 'absolute', left: 96, right: 96, top: 660}}>
				<Pill text="One row per post" color={C.green} />
				<div
					style={{
						marginTop: 14,
						padding: 16,
						borderRadius: 12,
						border: `2px solid ${C.green}`,
						display: 'grid',
						gridTemplateColumns: 'repeat(4, 1fr)',
						gap: 12,
					}}
				>
					{NAMES.map((n, i) => {
						const s = spring({frame: frame - 6 - i * 2, fps, config: {damping: 200}, durationInFrames: 12});
						return (
							<div
								key={i}
								style={{
									height: 70,
									borderRadius: 10,
									border: `2px solid ${C.green}99`,
									backgroundColor: C.panel,
									padding: '8px 12px',
									opacity: s,
									transform: `scale(${0.9 + 0.1 * s})`,
								}}
							>
								<div style={{fontFamily: INTER, fontWeight: 700, fontSize: 24, color: C.paper}}>{n}</div>
								<div style={{marginTop: 8, height: 8, width: '70%', borderRadius: 4, backgroundColor: C.border}} />
							</div>
						);
					})}
				</div>
			</div>

			<div style={{position: 'absolute', left: 96, right: 96, top: 1360, fontFamily: INTER, fontWeight: 700, fontSize: 48, color: C.paper}}>
				New post → add <span style={{color: C.green}}>one row</span>
			</div>
			<Img src={staticFile('brand/pbd-lockup-A-padlock-on-dark.png')} style={{position: 'absolute', left: 96, top: 1480, height: 56}} />
		</AbsoluteFill>
	);
};
