// 9:16 title card (edit-spec-v1 §6 "Title card", adapted for Shorts).
import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {C, INTER, MONO, gridBg, labelStyle} from './theme';

export type VerticalTitleCardProps = {
	label: string;
	titleGreen: string;
	titlePaper: string;
	codeLine?: string;
};

export const VerticalTitleCard: React.FC<VerticalTitleCardProps> = ({label, titleGreen, titlePaper, codeLine}) => (
	<AbsoluteFill style={gridBg}>
		<Img src={staticFile('brand/pbd-lockup-A-padlock-on-dark.png')} style={{position: 'absolute', left: 96, top: 140, height: 56}} />
		<div style={{position: 'absolute', left: 96, right: 96, top: 520}}>
			<div style={labelStyle}>{label}</div>
			<div style={{fontFamily: INTER, fontWeight: 700, fontSize: 104, lineHeight: 1.05, marginTop: 28}}>
				<div style={{color: C.green}}>{titleGreen}</div>
				<div style={{color: C.paper}}>{titlePaper}</div>
			</div>
			{codeLine ? (
				<div
					style={{
						display: 'inline-block',
						marginTop: 48,
						padding: '16px 24px',
						backgroundColor: C.panel,
						borderLeft: `4px solid ${C.green}`,
						borderRadius: 12,
						fontFamily: MONO,
						fontSize: 34,
						color: C.paper,
					}}
				>
					{codeLine}
				</div>
			) : null}
		</div>
	</AbsoluteFill>
);
