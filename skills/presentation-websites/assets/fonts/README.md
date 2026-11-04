# Brand fonts go here

Drop the brand's `woff2` (preferred) or `ttf` files in this folder, then list them in `FONTS` in `../../embed-fonts.py` with their weight and style. `FONT_FAMILY` must match the first family in `--font-brand` in the page's `:root`.

This folder is intentionally empty in the repository. Brand fonts are almost always licensed, so check that the licence covers embedding the font in a distributed HTML file, and **never commit licensed font files to a public repository**. A `.gitignore` here keeps them out of git.
