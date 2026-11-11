# imoves.com website - briefing for Claude v0.1

Nov 11, 2026 · @David Laycock

## What this is

This briefing tells Claude how to maintain the imoves.com sales website on behalf of Ian Pickles and Imogen, the owners of imoves. Every change goes to a development view first and reaches the live site only after Ian or Imogen approves it.

David Laycock rebuilt the site in October and November 2026 as a static copy of the old Bespoke-hosted site and moved it to Cloudflare. He is handing it over. Treat this document as standing instructions.

**Setting up (Ian, once):**

1. Create a Claude Project called "imoves website" and upload this document to it.
2. Connect Claude to the GitHub repository `dmlaycock/imoves-website`. Ian's GitHub account needs write access to it.
3. Ask Claude to read `README.md`, `tools/issues-log.md`, `tools/SPEC-version-a.md` and `tools/SPEC-version-b.md` before its first change.
4. Ask Claude to save this briefing in the repository as `CLAUDE.md`, as its first change, using the workflow below. The repository has no `CLAUDE.md` today.

## How the site is hosted

The site is plain static HTML in a GitHub repository, built and served by Cloudflare Pages. A push to GitHub is the only way anything is published.

| Item | Detail |
| --- | --- |
| Repository | [github.com/dmlaycock/imoves-website](https://github.com/dmlaycock/imoves-website) (public, so never commit secrets) |
| Site structure | One folder per page, each with an `index.html`. No framework, no CMS. Header, menu and footer are repeated inside every page file |
| Hosting | Cloudflare Pages project `imoves-website` in the imoves Cloudflare account, connected to the repository through the Cloudflare Workers and Pages GitHub app |
| Build | Cloudflare runs `python3 tools/build-dist.py dist` and publishes the `dist` folder |
| What the build does | Switches absolute links to https://imoves.com, regenerates `sitemap.xml` from the published pages, writes the Cloudflare `_redirects` file from the redirect stub pages, and fails if any file exceeds 25 MiB |
| Live branch | `production` publishes to [imoves.com](https://imoves.com) |
| Development branch | `main` publishes to [main.imoves-website.pages.dev](https://main.imoves-website.pages.dev) |
| Other branches | Any other branch builds its own preview at `<branch-name>.imoves-website.pages.dev` |
| Frozen branches | `version-a`, `version-b`, `version-c`, `version-d` are locked reference copies |
| Current version | v0.23 on both `main` and `production` (5 November 2026) |
| Videos | Cloudflare Stream, played by the site's own player (`video/cf-player.js`, `video/cf-player.css`). The list of videos is `tools/video-stream-map.json` |
| Booking and forms | LeadConnector (Genie) booking widget. Google Tag Manager container GTM-W5KKLGQ |
| Login, sign-up, checkout | Not on this site. Links go to platform.imoves.com |
| DNS | Cloudflare zone imoves.com. The domain is registered with Exact Hosting |

## The update workflow

Every change follows the same eight steps: change on `main`, review on the development view, approve, then promote to `production`.

1. **Start clean.** Check out `main` and pull the latest. Confirm `main` and `production` point at the same commit. If they differ, tell Ian what is waiting on `main` before starting.
2. **Make the change on `main`.** For larger or experimental work, use a separate branch, which gets its own preview address, and merge it into `main` when Ian is happy.
3. **Give it a version number.** Add an entry to the Versions list in `README.md` (next is v0.24) with the date, what changed and which pages. Start the commit message with the version number.
4. **Push `main`.** Cloudflare builds the development view in a few minutes at [main.imoves-website.pages.dev](https://main.imoves-website.pages.dev).
5. **Check the development view yourself.** Look at every changed page at desktop and phone width, plus the homepage. Confirm the Cloudflare build succeeded. Fix anything wrong as a new version.
6. **Ask for approval and stop.** Tell Ian the version number, what changed, and give a link to each changed page on the development view. Do nothing further until Ian or Imogen says, in so many words, that this version is approved to go live.
7. **Promote.** Fast-forward `production` to the approved commit and push:
   - `git checkout production`
   - `git merge --ff-only main`
   - `git push origin production`
8. **Check the live site.** Open the changed pages on [imoves.com](https://imoves.com) once Cloudflare finishes, and report back.

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
- The imoves logo is the white "im" mark on purple. The old blue-and-pink "imoves" wordmark is retired, and using it anywhere is an error.
- imoves sells five school packages: Active Blasts, Active Learning, Dance, PE and Active School. Do not add buy buttons or prices for anything else. Gymnastics and Mental Wellbeing are content inside packages, not products.
- Add no new third-party scripts, trackers or embeds without Ian's approval.

**Technical**

- Do not hand-edit generated content. The comparison table on the homepage and `/pricing` comes from `tools/versiond-compare.py`. The sitemap comes from the build.
- A menu, header or footer change touches every page file. Make it with a script and check a sample of pages.
- Keep every file under 25 MiB. Give any image over 150 KB a WebP version, following the existing `<picture>` pattern.
- When a page goes, forward its address rather than leaving a dead link. Read `tools/build-dist.py` and `tools/redirects.json` and follow the existing pattern.
- Log every stop-gap in `tools/issues-log.md` with the date, how it is handled now, and the proper fix.

**Cloudflare and DNS**

- Do not change DNS records, nameservers or Cloudflare settings as part of a website change. If Ian asks for one, explain the effect and confirm before acting.
- Every DNS record except the website's own must stay "DNS only" (grey cloud). The Genie pages and email depend on it.

**When unsure**

- Ask Ian one clear question rather than guess.

## Common tasks and known stop-gaps

| Task | How |
| --- | --- |
| Change wording or an image on a page | Edit that page's `index.html`. Keep the page title, description and social tags in step if the subject changes |
| Change a price or a feature in the comparison table | Edit the data block in `tools/versiond-compare.py` and run it. It rewrites the homepage and `/pricing` together. Remind Ian that the same price must also change in Quickbase |
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

## Rollback and scope

**If a live release is wrong**, the fastest fix is in Cloudflare: Workers and Pages, `imoves-website`, Deployments, then roll back to the previous production deployment. Ian does this himself in the dashboard. Afterwards, revert the change on `main` as a new version and run the normal workflow so the repository matches what is live.

**Out of scope for this briefing.** Do not change any of these as part of website work:

- platform.imoves.com (the teaching platform) and its code
- Quickbase and Zapier
- The Genie (GoHighLevel) pages and funnels on subdomains such as aac.imoves.com
- Email settings and DNS records
- The old Bespoke-hosted site and its CMS

A wider rebuild of the platform is in progress separately. Each part arrives with its own documentation at handover.
