# Shopmaster Catalog Workbench — admin script source

`src/admin.js` is the single source for the plugin's admin JavaScript. It is
plain, unminified JavaScript — nothing here is compiled, minified or
obfuscated.

The code only the paid version uses is wrapped in markers:

```js
/*! <fs_premium_only> */  ...  /*! </fs_premium_only> */
```

## Build

Requires Python 3 and nothing else. From the root of this repository:

```
python scripts/build-js.py
```

It writes two files into `dist/`, with no markers left in either:

| File | Contents |
|---|---|
| `admin-pro.js` | everything — loaded when the site can use paid code |
| `admin.js`     | the marked parts taken out — loaded otherwise |

Those two files are byte for byte the ones shipped in the plugin's `assets/`
folder.

`python scripts/build-js.py --check` exits non-zero if either file is out of
date, which is how the release build makes sure what ships matches this source.

## Licence

GPL-2.0-or-later, the same as the plugin.
