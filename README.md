# Shopmaster Catalog Workbench — admin script source

`src/admin.js` is the single source for the plugin's admin JavaScript. It is
plain, unminified JavaScript — nothing here is compiled, minified or
obfuscated.

The code only the paid version uses is wrapped in markers:

```js
/*! <fs_premium_only> */  ...  /*! </fs_premium_only> */
```

## Build

Requires Python 3. From the root of this repository:

```
python scripts/build-js.py
```

It writes two files, with no markers left in either:

| File | Contents |
|---|---|
| `admin-pro.js` | everything — loaded when the site can use paid code |
| `admin.js`     | the marked parts taken out — loaded otherwise |

`python scripts/build-js.py --check` exits non-zero if either file is out of
date, which is how the release build makes sure the shipped files match this
source.

The script writes into the plugin's own `assets/` folder, so run it from a
checkout that sits beside the plugin, or point `ASSETS` at wherever you want
the two files.

## Licence

GPL-2.0-or-later, the same as the plugin.
