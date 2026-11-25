# The Daily Globe — 25 November 2026

[![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Agen997/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Agen997/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

A one-page newspaper front page summing up the world's news of
**Wednesday, 25 November 2026**, drawn programmatically with Python
and Pillow. Lead story: the Israeli strike that killed a second senior
Hamas security official in Gaza in a day. Also: the Cartagena
supermarket hostage siege, Pakistan's first astronaut reaching China's
space station, the Houthis' claims against Saudi Arabia, plus briefs
from DR Congo, Indonesia, Spain and the Pacific — and the day's
markets.

## How it works

`draw.py` draws the 1024×1024 front page (`entry.png`) from the
verified stories of the day. `main.py` copies that baked image to
`/output/entry.png`. The program runs twice with byte-identical
output, uses no network, and needs only the Python standard library
plus Pillow at build time (the entry itself is just the copy).

## Run it

```sh
python3 draw.py            # redraw entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see LICENSE.
