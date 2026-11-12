# imoves.com website - briefing for Claude v0.2

v0.1 by David Laycock, 11 November 2026. v0.2 updated by Claude for Ian Pickles, 12 November 2026: new hosting, development view lock, logo rule and brand rules.

## What this is

This briefing tells Claude how to maintain the imoves.com sales website on behalf of Ian Pickles and Imogen, the owners of imoves. Every change goes to a development view first and reaches the live site only after Ian or Imogen approves it.

David Laycock rebuilt the site in October and November 2026 as a static copy of the old Bespoke-hosted site and moved it to Cloudflare. He has handed it over to Ian. Treat this document as standing instructions.

Before the first change in a session, read `README.md` (the Versions list) and `tools/issues-log.md`. The Claude Project "imoves sales website" also holds the brand rules (`imoves brand rules for Claude`) and the handover plan (`Website handover - step by step plan`).

## How the site is hosted

The site is plain static HTML in a GitHub repository. GitHub Actions builds it and uploads it to Cloudflare Pages. A push to GitHub is the only way anything is published.

| Item | Detail |
| --- | --- |
| Repository | [github.com/imoves-ian/imoves-website](https://github.com/imoves-ian/imoves-website), owned by Ian (public, so never commit secrets). The old address github.com/dmlaycock/imoves-website forwards to it |
| Site structure | One folder per page, each with an `index.html`. No framework, no CMS. Header, menu and footer are repeated inside every page file |
| Publishing | `.github/workflows/deploy-cloudflare.yml` runs `python3 tools/build-dist.py dist` and uploads `dist` with wrangler to the Cloudflare Pages project **`imoves-site`** (a direct-upload project, not Git-linked). It needs the repository secrets `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` |
| What the build does | Leaves out `tools`, `brand`, the frozen `version-*` folders and other non-site files; switches absolute links to https://imoves.com; regenerates `sitemap.xml` from the published pages; writes the Cloudflare `_redirects` file from the redirect stub pages; fails if any file exceeds 25 MiB |
| Live branch | `production` publishes to [imoves.com](https://imoves.com) and www.imoves.com (custom domains of `imoves-site`) |
| Development branch | `main` publishes to [main.imoves-site.pages.dev](https://main.imoves-site.pages.dev) |
| Manual run | Actions tab, "Deploy to Cloudflare Pages", "Run workflow" rebuilds and redeploys the `production` branch exactly as it stands. Nothing in git changes |
| Development view lock | Every preview address `*.imoves-site.pages.dev` is protected by Cloudflare Access. Only Ian's imoves.com address and David's address can get in; they are emailed a one-time code and stay signed in for 24 hours. Claude cannot open the development view on its own: it checks it in Ian's built-in browser after Ian has signed in. Ian enters the code himself and never shares it. imoves.com and imoves-site.pages.dev are public |
| Frozen branches | `version-a`, `version-b`, `version-c`, `version-d` are locked reference copies |
| Playground | Branch `playground`, published by its own workflow to the separate, password-protected Pages project `imoves-playground` (imoves-playground.pages.dev). Not part of imoves.com; never merge it into `main` unless Ian asks |
| Old project | Cloudflare Pages project `imoves-website` (imoves-website.pages.dev), frozen at v0.23. It no longer serves imoves.com and its Git link is broken. Kept as a fallback until Ian retires it |
| GitHub Pages | Still builds a public copy from `main` ("pages build and deployment"). Leave it alone unless Ian asks |
| Current version | See the Versions list in `README.md` |
| Videos | Cloudflare Stream, played by the site's own player (`video/cf-player.js`, `video/cf-player.css`). The list of videos is `tools/video-stream-map.json` |
| Booking and forms | LeadConnector (Genie) booking widget. Google Tag Manager container GTM-W5KKLGQ |
| Login, sign-up, checkout | Not on this site. Links go to platform.imoves.com |
| DNS | Cloudflare zone imoves.com, in the imoves Cloudflare account. The domain is registered with Exact Hosting |

## The update workflow

Every change follows the same eight steps: change on `main`, review on the development view, approve, then promote to `production`.

1. **Start clean.** Check out `main` and pull the latest. Confirm `main` and `production` point at the same commit. If they differ, tell Ian what is waiting on `main` before starting.
2. **Make the change on `main`.** For larger or experimental work, use a separate branch and merge it into `main` when Ian is happy. Note that only `main` and `production` are published by the workflow; another branch gets no preview unless the workflow is extended.
3. **Give it a version number.** Add an entry to the Versions list in `README.md` with the date, what changed and which pages. Start the commit message with the version number.
4. **Push `main`.** GitHub Actions publishes the development view in a few minutes at [main.imoves-site.pages.dev](https://main.imoves-site.pages.dev).
5. **Check the development view yourself.** Confirm the Actions run succeeded. Then, in Ian's built-in browser once he has signed in, look at every changed page at desktop and phone width, plus the homepage. Fix anything wrong as a new version.
6. **Ask for approval and stop.** Tell Ian the version number, what changed, and give a link to each changed page on the development view. Do nothing further until Ian or Imogen says, in so many words, that this version is approved to go live.
7. **Promote.** Fast-forward `production` to the approved commit and push:
   - `git checkout production`
   - `git merge --ff-only <approved commit>`
   - `git push origin production`
8. **Check the live site.** Once the Actions run finishes, open the changed pages on [imoves.com](https://imoves.com) and report back.

If the fast-forward fails, stop and tell Ian. It means `production` holds something `main` does not, and somebody has broken the workflow.

## Rules

These rules hold for every request, however small.

**Publishing**

- Never commit directly to `production`. It moves only by fast-forward to an approved commit on `main`.
- Never promote without explicit approval of that specific version from Ian or Imogen in the current conversation. Approval of one version does not carry to the next.
- Never force push, amend or rewrite history that is already on GitHub.
- Never touch the `version-a` to `version-d` branches.

**Versions**

- Every change, however small, gets a new version number and a `README.md` entry.
- Never rebuild and overwrite a version that Ian has already seen. A correction is a new version.

**Content and design**

- Change only what Ian asked for. Leave every other word, image and layout as it is. No redesigns or tidy-ups unless asked.
- Write in UK English.
- Follow the imoves brand rules (Claude Project doc `imoves brand rules for Claude`; brand files in `brand/`). Use only the approved colours, Baloo Primary and the supplied logo and brush files. Never redraw a logo or brush shape. If Ian asks for something off-brand, flag it and get his confirmation first.
- The imoves logo is the full "imoves" wordmark: the purple version on white, the white version on purple and other brand colours. The "im" mark is the favicon and social media logo. The old blue-and-pink "imoves" wordmark is retired, and using it anywhere is an error.
- The top-left header logo changes every month to a themed version Ian supplies. The header is purple, so it always takes the **white** version. It lives at `images/300x0/0x0-0x0/logos/<month>-white-logo.png` (300 x 84 px, shown at 150px wide) and is referenced in every page file, so swapping it is a site-wide scripted change.
- imoves sells five school packages: Active Blasts, Active Learning, Dance, PE and Active School. Do not add buy buttons or prices for anything else. Gymnastics and Mental Wellbeing are content inside packages, not products.
- Add no new third-party scripts, trackers or embeds without Ian's approval.

**Technical**

- Do not hand-edit generated content. The comparison table on the homepage and `/pricing` comes from `tools/versiond-compare.py`. The sitemap comes from the build.
- A menu, header or footer change touches every page file. Make it with a script and check a sample of pages.
- Keep every file under 25 MiB. Give any image over 150 KB a WebP version, following the existing `<picture>` pattern.
- When a page goes, forward its address rather than leaving a dead link. Read `tools/build-dist.py` and `tools/redirects.json` and follow the existing pattern.
- Log every stop-gap in `tools/issues-log.md` with the date, how it is handled now, and the proper fix.
- Check what the live site actually shows rather than trusting written notes about it.

**Accounts, Cloudflare and DNS**

- Never ask for, read out or type passwords, sign-in codes or API tokens. Ian signs in himself.
- Do not change DNS records, nameservers or Cloudflare settings as part of a website change. If Ian asks for one, explain the effect and confirm before acting.
- Only imoves.com and www.imoves.com are proxied (orange cloud), pointing at `imoves-site`. Every other DNS record must stay "DNS only" (grey cloud). The platform, the Genie pages and email depend on it.

**When unsure**

- Ask Ian one clear question rather than guess.

## Brand files

`brand/` holds the approved brand files. The build leaves it out, so none of it is published on imoves.com.

| Folder | Contents |
| --- | --- |
| `brand/fonts` | Baloo Primary Regular, Medium, SemiBold, Bold and ExtraBold (.ttf, SIL Open Font License 1.1). Approved weights: Regular to Bold. ExtraBold is not used unless Ian says so |
| `brand/logos` | The logo pack as supplied: main logo (purple, white, black; RGB and CMYK), strapline logos, "im" social media logo, favicon, animation artwork |
| `brand/logos/monthly` | Monthly header logos at full size, as supplied by Ian |
| `brand/brush-graphics` | The 20 brush shapes: PNG and EPS in Purple, Red, Pink, Orange and Blue, plus single-colour SVG masters (no fill set, so any brand colour can be applied with CSS) |

## Common tasks and known stop-gaps

| Task | How |
| --- | --- |
| Change wording or an image on a page | Edit that page's `index.html`. Keep the page title, description and social tags in step if the subject changes |
| Change a price or a feature in the comparison table | Edit the data block in `tools/versiond-compare.py` and run it. It rewrites the homepage and `/pricing` together. Remind Ian that the same price must also change in Quickbase |
| Monthly header logo | Save Ian's white logo in `brand/logos/monthly`, make a 300 x 84 PNG at `images/300x0/0x0-0x0/logos/<month>-white-logo.png`, and update the `src` and `alt` in every page file with a script |
| Add a video | Upload it to Cloudflare Stream, add it to `tools/video-stream-map.json`, add a thumbnail to `video/thumbs`, and copy the player markup from an existing page |
| Add a page | Copy the closest existing page folder. Update the title, description, canonical and social tags. Add menu links only if Ian asks |
| Remove a page | Forward its address (see Rules). The build drops forwarded pages from the sitemap |
| Check whether someone edited the old site | Run `tools/live-drift.py`. It will always list `/active-advent`, which is expected. It stops being useful once the old Bespoke site is switched off |
| Compare before and after | The Playwright scripts in `tools/` (`compare.js`, `compare-all.js`) screenshot and compare pages |

**Known stop-gaps** (full detail in `tools/issues-log.md`):

- The `/pricing` page is a static snapshot. The prices live in Quickbase, so a price change needs making in both places until the platform rebuild replaces it.
- `/jointheimovement` carries a form that submits nowhere. The page is unlinked.
- `/march-half-price-offer` has dead Paddle buy buttons. The page is unlinked and due to be dropped.
- 61 page titles run over 60 characters and await imoves' review.
- The feature rows in the comparison table await imoves' content review.
- The "After School Resources" menu link to aac.imoves.com awaits Ian's decision.
- The old Cloudflare project `imoves-website` awaits retirement (issue 17).

## Rollback and scope

**If a live release is wrong**, the fastest fix is in Cloudflare: Workers and Pages, **`imoves-site`**, Deployments, then roll back to the previous production deployment. Ian does this himself in the dashboard. Afterwards, revert the change on `main` as a new version and run the normal workflow so the repository matches what is live.

**If `imoves-site` itself fails**, the old project `imoves-website` still holds v0.23. Moving the imoves.com and www.imoves.com custom domains back to it restores that version. Ian does this, with Claude explaining each step first.

**Out of scope for this briefing.** Do not change any of these as part of website work:

- platform.imoves.com (the teaching platform) and its code
- Quickbase and Zapier
- The Genie (GoHighLevel) pages and funnels on subdomains such as aac.imoves.com
- Email settings and DNS records
- The old Bespoke-hosted site and its CMS

A wider rebuild of the platform is in progress separately. Each part arrives with its own documentation at handover.
