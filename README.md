# news-image-nov-23

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/wenjinqin/news-image-nov-23/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/wenjinqin/news-image-nov-23/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-page newspaper front page summing up the world news of Monday 23 November 2026, drawn with Pillow in `draw23.py` and delivered by `main.ts`.

## The six stories

- **Nvidia brings Jensen Huang back as chief executive** — 11 days after he resigned, and the shares jump about 33%.
- **Iran vows to use all available means against the US naval blockade** — Tehran says it shot down a US drone over the Persian Gulf, and Trump says US strikes could resume after the New Year if no deal is reached.
- **Ukraine sinks the Russian corvette Merkury at Benghazi port, Libya** — seven naval drones, hailed by Zelenskyy.
- **The EU proposes its 22nd sanctions package on Russia** — about 60 more banks cut from SWIFT, crypto platforms targeted, 70+ shadow-fleet vessels listed, plus sports and visa bans.
- **Bangladesh vows to arrest former prime minister Sheikh Hasina** if she returns from India.
- **India pledges €1.4 billion to help Nepal rebuild** after the August glacier floods, as Nepal PM Balendra Shah visits New Delhi.

Also in the ticker: US stocks rebound sharply after the AI sell-off (S&P 500 up 4.82%; Nikkei fell over 5%), the Houthis claim an attack on a Saudi oil refinery, and Germany's Merz calls on Russia to stop "dangerous provocations".

## Sources

Each story was verified against at least two published sources dated 23 November 2026: OneTurn, the Daily Mirror and the NYT (Nvidia); Just Security's Early Edition, OneTurn and Algemeiner (Iran); OneTurn and the Daily Mirror (Ukraine); Reuters, LB.ua, APA and UATV (EU sanctions); Just Security and the Daily Mirror (Bangladesh); OneTurn and Daily Summary of World (India–Nepal).

## Deliberately left out

These stories were not used because they happened or were first reported on earlier days: the COP31 collapse (22 Nov), the capture of "Chapo Isidro" (21 Nov), the Dymer apartment strike (22 Nov), the Democrats winning 258 House seats (22 Nov), the Trump–Xi–Putin Shenzhen summit (19–20 Nov), the Iranian strike on Bahrain (21 Nov), and the S&P 500 Friday fall (20 Nov).

## Run

```sh
python3 draw23.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`draw23.py` renders `entry.png` (1024×1024, under 1 MiB). `main.ts` validates the image (PNG magic, ≤1 MiB, ≤1024×1024, IEND present) and copies it byte-for-byte to `$MAKEFUN_OUTPUT_DIR/entry.png`, then reads the copy back to prove it is identical.

<sub>Entered on [make.fun](https://make.fun/?ref=d5a50dzy&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
