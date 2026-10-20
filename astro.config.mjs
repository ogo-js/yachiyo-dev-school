// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	// GitHub Pages で公開する場所（https://ogo-js.github.io/yachiyo-dev-school/）
	site: 'https://ogo-js.github.io',
	base: '/yachiyo-dev-school',
	integrations: [
		starlight({
			title: 'Yachiyo Dev School',
			customCss: ['./src/styles/custom.css'],
			locales: {
				root: { label: '日本語', lang: 'ja' },
			},
			sidebar: [
				{ label: '目次', link: '/' },
				{ label: '第0部 準備', items: [{ autogenerate: { directory: '00-setup' } }] },
				{ label: '第1部 コマンドライン', items: [{ autogenerate: { directory: '01-command-line' } }] },
				{ label: '第2部 Git と GitHub', items: [{ autogenerate: { directory: '02-git' } }] },
				{ label: '第3部 Web の仕組み', items: [{ autogenerate: { directory: '03-web' } }] },
				{ label: '第4部 Docker', items: [{ autogenerate: { directory: '04-docker' } }] },
				{ label: '第5部 データベース', items: [{ autogenerate: { directory: '05-database' } }] },
				{ label: '第6部 TypeScript', items: [{ autogenerate: { directory: '06-typescript' } }] },
				{ label: '第7部 React と React Router', items: [{ autogenerate: { directory: '07-react' } }] },
				{ label: '第8部 C# と ASP.NET Core', items: [{ autogenerate: { directory: '08-csharp' } }] },
				{ label: '第9部 テスト', items: [{ autogenerate: { directory: '09-test' } }] },
				{ label: '第10部 総仕上げ', items: [{ autogenerate: { directory: '10-final' } }] },
				{ label: '付録 Claude Code', items: [{ autogenerate: { directory: 'appendix-claude' } }] },
				{ label: 'さらに学ぶ', link: '/next-steps/' },
			],
		}),
	],
});
