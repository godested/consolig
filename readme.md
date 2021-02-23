# Consolig

Consolig is a version of Consolas that supports ligatures. Unlike other efforts, all ligatures in Consolig were made by hand from the original Consolas glyphs (they are not just copied from another ligature font).

Because Consolas cannot be redistributed, this project provides the tools to append the ligature glyphs and features to your personal copy of Consolas, generating a copy of Consolig.

**NOTE: Currently, all font styles use the same ligature glyphs. Making style-specific glyphs is on the roadmap.**

## How to build

1. Copy your Consolas font files into the Consolig `/input` directory. On Windows, your Consolas files are located in `/Windows/Fonts` on your OS drive. The valid filenames are:
   - `consola.ttf` - Regular
   - `consolab.ttf` - Bold
   - `consolai.ttf` - Italic
   - `consolaz.ttf` - Bold Italic
2. Make sure that you have Python 3 with PIP installed.
   - I have verified with the [Python 3.8 installation in the Windows Store](https://www.microsoft.com/store/productId/9MSSZTT1N39L).
3. Install the required Python libraries.<br>
   `pip install fontTools`
4. Execute the build script.
   `python build.py`
5. If everything goes well, you should now have Consolig font files in your `/build` directory.

## How to use

Check out the information about enabling ligatures provided by [FiraCode](https://github.com/tonsky/FiraCode) here:
[https://github.com/tonsky/FiraCode/wiki#how-to-enable-ligatures](https://github.com/tonsky/firacode/wiki#how-to-enable-ligatures)

This version of Consolig is comparable to version **5.2** of [FiraCode](https://github.com/tonsky/FiraCode). Consolig now does everything FiraCode can do, with the exception of their **Console UI** and **Math** features (yes, I know you guys want Powerline -- it's coming). However, that _does_ mean that Consolig now has alternative glyph styles.

- `ss01` adds a bottom serif to lowercase R and lowercase F
- `ss02` gives `<=` and `>=` an angled bottom bar (default is horizontal)
- `ss03` swaps the traditional Consolas ampersand for a programming alternate
- `ss04` removes the middle bar from the traditional Consolas dollar sign
- `ss05` swaps the traditional Consolas "at symbol" for a version with a partial loop
- `ss06` enables a thin backslash for escape characters
- `ss07` enables regexp matching
- `ss08` enables alternate double/triple equals with gaps (versus the triple bar)
- `zero` enables a dotted zero
- `onum` enables old-style numeric glyphs

## Credits

- Glyph substitution logic was taken from [FiraCode](https://github.com/tonsky/FiraCode).
