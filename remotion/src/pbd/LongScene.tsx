// One 16:9 scene of a long-form video, chosen by `kind`. Rendered one scene at a time by render-scenes.mjs;
// ffmpeg joins the scenes and adds the voice.
import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {Label, LabelView, ScreenScene} from './ScreenScene';
import {ClaudePrompt, ClaudeResponse} from './ClaudeUI';
import {ChapterCard, Checklist, CodeStack, Outro, PromptCard, SeriesCard, StepList} from './Cards';

export type LongSceneProps = {kind: string; dur: number; [k: string]: unknown};

export const LongScene: React.FC<LongSceneProps> = (props) => {
	const t = useCurrentFrame() / useVideoConfig().fps;
	const labels = (props.labels as Label[] | undefined) ?? [];
	return (
		<AbsoluteFill>
			<Body {...props} />
			{props.kind !== 'screen' && labels.map((l, i) => <LabelView key={i} l={l} t={t} />)}
		</AbsoluteFill>
	);
};

const Body: React.FC<LongSceneProps> = ({kind, ...p}) => {
	const a = p as any;
	switch (kind) {
		case 'screen': return <ScreenScene {...a} />;
		case 'claudePrompt': return <ClaudePrompt {...a} />;
		case 'claudeResponse': return <ClaudeResponse {...a} />;
		case 'series': return <SeriesCard {...a} />;
		case 'chapter': return <ChapterCard {...a} />;
		case 'prompt': return <PromptCard {...a} />;
		case 'codeStack': return <CodeStack {...a} />;
		case 'checklist': return <Checklist {...a} />;
		case 'steps': return <StepList {...a} />;
		case 'outro': return <Outro />;
		default: throw new Error(`unknown scene kind ${kind}`);
	}
};
