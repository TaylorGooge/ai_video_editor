// 9:16 end card with a call to action (matches brand/shorts-endcards style #2).
import React from 'react';
import {AbsoluteFill, Img, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, INTER, MONO, gridBg} from './theme';

export type EndCardProps = {
	headline?: string;
	line?: string;
	cta?: string;
	handle?: string;
};

export const EndCard: React.FC<EndCardProps> = ({
	headline = 'Want the full fix?',
	line = 'The step-by-step video is on the channel.',
	cta = 'Learn more on the channel',
	handle = '@publicbydefault',
}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const pop = spring({frame: frame - 4, fps, config: {damping: 200}, durationInFrames: 14});

	return (
		<AbsoluteFill style={{...gridBg, alignItems: 'center'}}>
			<Img src={staticFile('brand/pbd-mark-A-padlock-on-dark.png')} style={{position: 'absolute', top: 380, width: 200, height: 200}} />
			<div style={{position: 'absolute', top: 620, left: 96, right: 96, textAlign: 'center'}}>
				<div style={{fontFamily: INTER, fontWeight: 700, fontSize: 72, color: C.paper}}>{headline}</div>
				<div style={{fontFamily: INTER, fontWeight: 500, fontSize: 40, color: C.muted, marginTop: 20, lineHeight: 1.3}}>{line}</div>
				<div
					style={{
						display: 'inline-block',
						marginTop: 56,
						padding: '22px 44px',
						borderRadius: 999,
						backgroundColor: C.green,
						color: C.ink,
						fontFamily: INTER,
						fontWeight: 700,
						fontSize: 44,
						opacity: pop,
						transform: `scale(${0.92 + 0.08 * pop})`,
					}}
				>
					{cta}
				</div>
				<div style={{fontFamily: MONO, fontSize: 38, color: C.muted, marginTop: 32}}>{handle}</div>
			</div>
			<div style={{position: 'absolute', top: 1180, fontFamily: INTER, fontWeight: 700, fontSize: 52}}>
				<span style={{color: C.green}}>Public</span> <span style={{color: C.paper}}>by Default</span>
			</div>
		</AbsoluteFill>
	);
};
