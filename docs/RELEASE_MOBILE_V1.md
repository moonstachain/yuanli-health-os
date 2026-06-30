# Release Mobile v1

## iOS adaptive mobile page

Mobile v1 adds a thumb-first iPhone web version of Yuanli Health OS.

## New files

```txt
mobile.html
src/mobile-agent-core.js
docs/MOBILE_IOS_DESIGN.md
docs/RELEASE_MOBILE_V1.md
```

## Implemented

### 1. Mobile page

`mobile.html` provides:

- iOS safe-area adaptation.
- Sticky top status.
- Bottom tab bar.
- Dark iOS-style cards.
- Large tap targets.

### 2. Mobile Agent core

`src/mobile-agent-core.js` reads `data/demo-health.json` and renders:

- Today state.
- Three daily actions.
- Weekly rhythm.
- Zone2 coach.
- Sleep checklist.
- Trend cards.
- 14-day experiment calendar.
- Records and doctor communication copy.

### 3. Public/local compatibility

Public GitHub Pages uses `data/demo-health.json`.

Local runtime can serve private merged data from `private/health.local.json` through the same `data/demo-health.json` request path.

## URLs

Public:

```txt
https://moonstachain.github.io/yuanli-health-os/mobile.html
```

Local:

```txt
http://127.0.0.1:8787/mobile.html
```

## UX principle

The mobile version is not a smaller cockpit. It is a随身健康教练: today-first, one-tap actions, short explanations, and low cognitive load.

## Next version

Mobile v1.1 should add PWA metadata, home-screen icon support, and improved offline fallback.
