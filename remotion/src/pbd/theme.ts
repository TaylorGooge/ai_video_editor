// Public by Default brand tokens (edit-spec-v1 §1). Shared by every component.
import {loadFont as loadInter} from '@remotion/google-fonts/Inter';
import {loadFont as loadMono} from '@remotion/google-fonts/JetBrainsMono';

export const C = {
	ink: '#0D1117',
	panel: '#161B22',
	border: '#30363D',
	paper: '#E6EDF3',
	muted: '#8B949E',
	green: '#3FB950',
	red: '#F85149',
	amber: '#D29922',
};

export const INTER = loadInter('normal', {weights: ['400', '500', '700'], subsets: ['latin']}).fontFamily;
export const MONO = loadMono('normal', {weights: ['400', '700'], subsets: ['latin']}).fontFamily;

// Faint grid used behind designed scenes (no gradients/glows per spec).
export const gridBg: React.CSSProperties = {
	backgroundColor: C.ink,
	backgroundImage: `linear-gradient(${C.border}33 1px, transparent 1px), linear-gradient(90deg, ${C.border}33 1px, transparent 1px)`,
	backgroundSize: '60px 60px',
};

export const labelStyle: React.CSSProperties = {
	fontFamily: INTER,
	fontWeight: 700,
	fontSize: 28,
	letterSpacing: '0.14em',
	textTransform: 'uppercase',
	color: C.green,
};
