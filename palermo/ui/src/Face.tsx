import css from './Face.module.css';

// avatars live at the server root (palermo/avatars); "gm" is the narrator
export const avatar = (name: string) => `avatars/${name}.png`;

// the small portrait next to every name in running text; sized in em so it follows the text it sits in.
// decoding="sync" everywhere: async decodes made a still frame differ by a few edge pixels between renders
export const Face = ({ name }: { name: string }) => <img decoding="sync" className={css.face} src={avatar(name)} alt="" />;
