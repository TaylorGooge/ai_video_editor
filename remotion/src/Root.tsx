import React from 'react';
import {Composition} from 'remotion';
import {ShortOverlay, ShortOverlayProps} from './pbd/ShortOverlay';
import {LongScene, LongSceneProps} from './pbd/LongScene';

const defaults: ShortOverlayProps = {
	durationInFrames: 150,
	header: {label: 'Fix video · Supabase', title: 'Example Short'},
	words: [
		{w: 'Hidden', start: 0.2, end: 0.5},
		{w: 'is', start: 0.5, end: 0.6},
		{w: 'not', start: 0.6, end: 0.9},
		{w: 'private.', start: 0.9, end: 1.4},
	],
	cards: [{kind: 'rows', from: 2, to: 5}],
	labels: [],
};

export const Root: React.FC = () => (
	<>
		<Composition
			id="LongScene"
			component={LongScene}
			width={1920}
			height={1080}
			fps={30}
			durationInFrames={60}
			defaultProps={{kind: 'outro', dur: 2} as LongSceneProps}
			calculateMetadata={({props}) => ({durationInFrames: Math.max(1, Math.round(props.dur * 30))})}
		/>
		<Composition
			id="ShortOverlay"
			component={ShortOverlay}
			width={1080}
			height={1920}
			fps={30}
			durationInFrames={defaults.durationInFrames}
			defaultProps={defaults}
			calculateMetadata={({props}) => ({durationInFrames: props.durationInFrames})}
		/>
	</>
);
