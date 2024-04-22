// You can also use the generator at https://skeleton.dev/docs/generator to create these values for you
import type { CustomThemeConfig } from '@skeletonlabs/tw-plugin';
export const lavender: CustomThemeConfig = {
	name: 'lavender',
	properties: {
		// =~= Theme Properties =~=
		"--theme-font-family-base": `ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace`,
		"--theme-font-family-heading": `ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace`,
		"--theme-font-color-base": "0 0 0",
		"--theme-font-color-dark": "255 255 255",
		"--theme-rounded-base": "16px",
		"--theme-rounded-container": "6px",
		"--theme-border-base": "4px",
		// =~= Theme On-X Colors =~=
		"--on-primary": "0 0 0",
		"--on-secondary": "0 0 0",
		"--on-tertiary": "0 0 0",
		"--on-success": "255 255 255",
		"--on-warning": "0 0 0",
		"--on-error": "0 0 0",
		"--on-surface": "0 0 0",
		// =~= Theme Colors  =~=
		// primary | #69f419 
		"--color-primary-50": "233 253 221", // #e9fddd
		"--color-primary-100": "225 253 209", // #e1fdd1
		"--color-primary-200": "218 252 198", // #dafcc6
		"--color-primary-300": "195 251 163", // #c3fba3
		"--color-primary-400": "150 247 94", // #96f75e
		"--color-primary-500": "105 244 25", // #69f419
		"--color-primary-600": "95 220 23", // #5fdc17
		"--color-primary-700": "79 183 19", // #4fb713
		"--color-primary-800": "63 146 15", // #3f920f
		"--color-primary-900": "51 120 12", // #33780c
		// secondary | #eb6990 
		"--color-secondary-50": "252 233 238", // #fce9ee
		"--color-secondary-100": "251 225 233", // #fbe1e9
		"--color-secondary-200": "250 218 227", // #fadae3
		"--color-secondary-300": "247 195 211", // #f7c3d3
		"--color-secondary-400": "241 150 177", // #f196b1
		"--color-secondary-500": "235 105 144", // #eb6990
		"--color-secondary-600": "212 95 130", // #d45f82
		"--color-secondary-700": "176 79 108", // #b04f6c
		"--color-secondary-800": "141 63 86", // #8d3f56
		"--color-secondary-900": "115 51 71", // #733347
		// tertiary | #f5a365 
		"--color-tertiary-50": "254 241 232", // #fef1e8
		"--color-tertiary-100": "253 237 224", // #fdede0
		"--color-tertiary-200": "253 232 217", // #fde8d9
		"--color-tertiary-300": "251 218 193", // #fbdac1
		"--color-tertiary-400": "248 191 147", // #f8bf93
		"--color-tertiary-500": "245 163 101", // #f5a365
		"--color-tertiary-600": "221 147 91", // #dd935b
		"--color-tertiary-700": "184 122 76", // #b87a4c
		"--color-tertiary-800": "147 98 61", // #93623d
		"--color-tertiary-900": "120 80 49", // #785031
		// success | #2d02d0 
		"--color-success-50": "224 217 248", // #e0d9f8
		"--color-success-100": "213 204 246", // #d5ccf6
		"--color-success-200": "203 192 243", // #cbc0f3
		"--color-success-300": "171 154 236", // #ab9aec
		"--color-success-400": "108 78 222", // #6c4ede
		"--color-success-500": "45 2 208", // #2d02d0
		"--color-success-600": "41 2 187", // #2902bb
		"--color-success-700": "34 2 156", // #22029c
		"--color-success-800": "27 1 125", // #1b017d
		"--color-success-900": "22 1 102", // #160166
		// warning | #1be4b3 
		"--color-warning-50": "221 251 244", // #ddfbf4
		"--color-warning-100": "209 250 240", // #d1faf0
		"--color-warning-200": "198 248 236", // #c6f8ec
		"--color-warning-300": "164 244 225", // #a4f4e1
		"--color-warning-400": "95 236 202", // #5fecca
		"--color-warning-500": "27 228 179", // #1be4b3
		"--color-warning-600": "24 205 161", // #18cda1
		"--color-warning-700": "20 171 134", // #14ab86
		"--color-warning-800": "16 137 107", // #10896b
		"--color-warning-900": "13 112 88", // #0d7058
		// error | #0f894a 
		"--color-error-50": "219 237 228", // #dbede4
		"--color-error-100": "207 231 219", // #cfe7db
		"--color-error-200": "195 226 210", // #c3e2d2
		"--color-error-300": "159 208 183", // #9fd0b7
		"--color-error-400": "87 172 128", // #57ac80
		"--color-error-500": "15 137 74", // #0f894a
		"--color-error-600": "14 123 67", // #0e7b43
		"--color-error-700": "11 103 56", // #0b6738
		"--color-error-800": "9 82 44", // #09522c
		"--color-error-900": "7 67 36", // #074324
		// surface | #a362f0 
		"--color-surface-50": "241 231 253", // #f1e7fd
		"--color-surface-100": "237 224 252", // #ede0fc
		"--color-surface-200": "232 216 251", // #e8d8fb
		"--color-surface-300": "218 192 249", // #dac0f9
		"--color-surface-400": "191 145 245", // #bf91f5
		"--color-surface-500": "163 98 240", // #a362f0
		"--color-surface-600": "147 88 216", // #9358d8
		"--color-surface-700": "122 74 180", // #7a4ab4
		"--color-surface-800": "98 59 144", // #623b90
		"--color-surface-900": "80 48 118", // #503076
		
	}
}