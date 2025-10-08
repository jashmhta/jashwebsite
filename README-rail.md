# Rail.io Website Clone

## Overview
Static HTML clone of https://rail.io - A global B2B payments platform built with Webflow.

## Tech Stack
- Framework: Webflow (static export)
- Styling: External CSS from Webflow CDN
- Scripts: jQuery 3.5.1 + Webflow custom scripts
- Assets: Hosted on cdn.prod.website-files.com

## Structure
- `rail-io.html` - Single-page website with all sections
- Sections: Navigation, Hero, Stats, Map, Carousel, Use Cases, Scroll Animation, CTA, Footer

## Key Components
- Webflow classes: `.w-*` with data attributes
- Lottie animations for hero section
- Video backgrounds in carousel
- Interactive map with country pins
- Responsive design (mobile/tablet/desktop)

## Build/Lint/Test Commands
- No build process; static HTML with external assets
- Serve: `python -m http.server 8000` or `npx serve .`
- Test: Open `rail-io.html` in browser and verify sections load

## Assets
All assets (CSS, JS, images, videos) are loaded from Webflow CDN:
- CSS: https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/css/
- JS: https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/js/
- Images: https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/
- Videos: Embedded background videos for carousel

## Notes
- Fully functional clone with all external dependencies
- Lottie animations and video backgrounds included
- All navigation links preserved (some link to subpages)
- Tracking scripts (Google Analytics, LinkedIn) included in source
