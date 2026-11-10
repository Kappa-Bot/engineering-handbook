---
id: pb-public-web-discoverability-launch
kind: playbook
status: active
owner: engineering
version: "0.4"
applies_to:
  - public-marketing-websites
  - product-vertical-public-pages
  - client-business-websites
  - seo-brand-audits
sources:
  - src-google-seo-starter-guide
  - src-google-block-indexing
  - src-google-sitemaps
  - src-google-site-names
  - src-google-favicon-search
  - src-google-organization-structured-data
  - src-open-graph-protocol
  - src-google-ai-features
  - src-google-business-profile-edit
  - src-bing-webmaster-site-verification
  - src-bing-webmaster-sitemaps
  - src-bing-places-business
  - src-indexnow-protocol
  - src-marketingskills
last_verified: 2026-11-10
review_due: 2027-02-10
---

# Public Web Search Presence & Brand Launch Playbook

## Why this exists

Repeat the most valuable part of an SEO/brand discovery improvement **for every eligible business website** without copying the same design, hard-coding a sector or promising a Google result. The goal is a technically accessible, trustworthy, visually recognisable and useful presence for real brand and service searches.

This is the **how**. The canonical requirements are in `std-public-web-discoverability-baseline`; page quality in `std-ui-ux-quality-baseline`, visual review in `pb-frontend-quality-review`, design ownership in `pat-design-context-layering`, evidence in `pat-visual-evidence-integrity`, and release truth in `pol-verification-definition-of-done`. Repo-local `AGENTS.md`, legal/launch decisions and product status override inferred assumptions. This playbook neither ships an implementation nor authorizes publishing a previously gated website.

Origin case (implementation-specific, **not** the transferable norm): [MelodIQ-Web SEO-01 brand/search plan](https://github.com/Kappa-Bot/MelodIQ-Web/blob/main/docs/superpowers/plans/2026-10-27-seo-brand-search.md).

## Pick the work mode first

| Scenario | What to optimize first | Specific gate |
| --- | --- | --- |
| MelodIQ corporate presence | Branded search disambiguation, entity/name, professional previews and real web/CRM offer | Preserve existing SEO-01/legal/contact blockers until authorized |
| Public landing for a vertical | Search intention of that industry; honest product stage, demos, CTA | Never expose tenant CRM, internal APIs, private screenshots or unready features |
| Existing business/lead client website | Client's company/service/local intent and own recognizable identity | Explicit owner permission to use assets/facts and publish/alter domain/analytics |
| Speculative sample/demo for a lead | Sell/show concept with accurate labels and professional design | Keep confidential assets protected and indexation off until acceptance |
| Existing released site with poor Google snippets | Triage title/snippet/icon/canonical/routing and observation | Differentiate actual crawling issue from Google's autonomous presentation |

**No universal SEO settings copied between domains.** Especially do not attach the agency's `Organization`, social URLs, logos or Search Console property to a client's domain. A subdirectory within a larger domain may not be able to set an independent Google site name/favicon.

## T0 — Intake and evidence: establish what is true

Read the repository's `AGENTS.md`, brand/design sources, current route map, known client consent/legal facts, current deployment strategy and canonical launch/checklist. Capture **observed**, not assumed:

- Browser/date/locale/query, Google mobile/desktop screenshot (if available), brand spelling variants and disambiguation problems. Screenshots from search engines are observations at a point in time, not durable promises.
- Final canonical host and redirects (`https`, `www`/apex, lowercase/slashes), HTTP status and served HTML from the public URL.
- `robots.txt`, robots meta, `X-Robots-Tag`, `rel=canonical`, `sitemap.xml`, page title/description, H1 and rendered visible content for each priority route.
- Favicon/icon endpoint and actual bytes, `WebSite`/`Organization` JSON-LD, OG/social meta, current social share preview when accessible.
- Real Search Console owner/property/coverage only when the necessary account is already authorized. Record inaccessible tools as `NOT RUN`.
- The **separate** Google Search Console, Bing Webmaster Tools, Google Business Profile (if eligible), Bing Places for Business (if eligible) and IndexNow status. Record ownership, the canonical business website in each profile, accessible diagnostics and manual owner steps even if they cannot be completed during this run.
- Which pages are truly public, indexable, intentionally excluded, staging, auth, preview, deleted or redirects.

Suggested browser/HTTP spot checks (substitute approved site domain and page; examples are **read-only**):

```bash
curl -IL https://www.example.com/
curl -fsS https://www.example.com/robots.txt
curl -fsS https://www.example.com/sitemap.xml
curl -fsS https://www.example.com/
```

Compare server response with what is visible in browser and with Search Console when available. A correct source component does not prove that the deployed HTML contains it. Preserve baseline observations and the exact release SHA.

**Audit triage:** reuse the local commercial context (`pb-marketing-context-and-content`) and search evidence. Prioritize release/access constraints, crawl/index/canonical failures, wrong entity or unsupported claims, unusable destinations, then useful content/internal links and lower-impact polish. For each finding report inspected URL/layer, evidence/date, user impact, confidence and bounded fix. “Not seen in a static fetch” is not proof that rendered JSON-LD or content is absent; inspect the served HTML, rendered DOM and authorized engine inspection as relevant. Do not remove valid dynamic markup on a static-only observation.

**Stop opening indexation** if the project has a live SEO/legal/contact/client approval gate. Continue only independent non-public preparations until those gates are closed or explicitly amended by owner decision.

## T1 — Decide the indexability and ownership matrix

Write a small repo-local route table before changing code:

| Route family | Search policy | Canonical/owner | Acceptance concern |
| --- | --- | --- | --- |
| Home/about/services/case page truly published | Candidate indexable | Exact final host | Facts and claims verified |
| Individual sector/vertical landing | Candidate indexable if it offers real useful information | Its real public route | Product maturity and user intent |
| Service/area page for client | Candidate only with distinct useful factual content | Client-owned domain | True location, service area, rights/consent |
| Demo/preview/private dashboard/tenant/API | Excluded; protect confidential data at access boundary | No public marketing canonical | Negative tests ensure no exposure |
| Redirect/deleted/404 | Never in indexable sitemap | 3xx/404/410 as appropriate | No soft-404 or broken loops |

Determine who owns domain/DNS, Search Console, brand pack, copy, business facts and acceptance. For a live customer, agree on who gets ongoing Search Console access and documentation. For a lead prototype, do not infer ownership/permission from having found the business online.

Implement the repo-specific **single source** for host + route eligibility. In Next.js this may use route metadata, `robots.ts` and `sitemap.ts`; in another stack use its native equivalents. Do not refactor a working architecture merely to centralize a small metadata list.

## T2 — Fix the crawl/index layer with tests

Before implementation, create focused tests/fixtures for real regressions:

1. A gated site retains its approved `noindex`/crawler policy; no unreviewed change makes it indexable.
2. An approved live route has no accidental global `noindex` or broad `Disallow: /`, and HTTP and canonical point to the agreed host.
3. Sitemap entries resolve to public final canonical URLs only, with no demo/auth/staging/deleted/redirect entries or fabricated timestamps.
4. Robots, headers, canonical, JSON-LD and sitemap don't contradict each other on www/apex and representative deep routes.
5. An unknown route does not quietly receive marketing metadata and 200 if it is not a real public page.
6. A private route/resource stays protected independently of robots and metadata.

Follow the consumer repo's real test framework and TDD discipline for code changes. **Do not defeat the test by making a noindex page blocked from crawling** when expecting the engine to observe noindex. Once the owner's release gate is approved, update crawl/index directives together, verify the actual HTTP/HTML, and never guess if publication occurred.

## T3 — Give search engines the right identity and editorial signals

- Keep a single preferred business/site name consistent across Home, about, logo alt, visible footer/header, Open Graph site name and `WebSite` schema.
- Make each priority page's title/description answer its actual search intent. Prioritize accurate service/benefit/region over repetitive keyword strings. H1 and first-screen copy must explain the same promise.
- Add or correct `WebSite` and truthful `Organization`/`LocalBusiness` only where appropriate and verified. Avoid duplicate JSON-LD, dangerous unescaped strings, invented phone/address/tax ID/staff/client base and borrowed social profiles.
- Don't publish unapproved reviews, fabricated metrics or "we serve City X" pages for places the business doesn't actually serve. Use location signals only if true.
- Connect the most helpful real internal routes via semantic navigation and contextual links; add FAQ content only when it helps real readers, never merely to chase rich-result markup.
- For site architecture, inventory useful existing URLs, map visitor questions to distinct destinations and preserve valuable deep links/redirects. Do not impose a fixed menu size or click depth from an external template.
- For public verticals, distinguish *what the agency can develop*, *what has actually shipped* and *what a demo shows*. Private application screens never become public SEO landing pages by accident.

**Editorial quality check:** Could a first-time visitor identify the business, service, who it helps and the next real action in one short read? Does the page feel specific to that actual business/sector, not text generated for 50 similar domains?

**AI search / answer-engine work:** apply the existing discoverability baseline. Google's official AI-features guidance requires no special AI-only optimization or machine-readable file/schema beyond normal eligible search content. Do not turn `llms.txt`, mention counts or a vendor study into a release requirement or guaranteed citation. Verify each target engine's current primary guidance separately. Record query, engine/version if visible, date, locale and account/personalization limits for observations; one generated answer is not stable visibility or proof of attribution. Noindex/private boundaries remain unchanged.

## T4 — Visual brand sprint: beyond a URL in search

Treat four distinct delivery surfaces; choose art direction from approved identity and audience.

### A. Search-result presentation (proposal vs observation)

- Preferred site name, clear title/description, clean canonical URL and favicon recognisable without the full wordmark.
- Create a side-by-side **labelled mockup** of candidate brand and service results for editorial review. Contrast it explicitly with real dated Google screenshots; never present the proposal as a guaranteed Google render.
- Inspect small-size favicon at roughly 16/32/48 CSS px, on light and dark backgrounds. Check 1:1 square, stability of URL, server availability, correct client ownership and original asset quality.
- For schema logo (a different role from favicon), follow current Google Organization documentation and ensure large enough clean representation (currently minimum 112×112), crawlable and distinct from a fabricated wordmark.

### B. Social preview / Open Graph

- Consider up to **three purposeful directions** for the actual image, using the repo's real logo/brand tokens: (1) calm, premium symbol and one proposition; (2) editorial typography with service outcome; (3) authentic context for the sector, only with permitted photography/illustration.
- Pick the strongest direction, not a permanent library of near-identical cards. Target legible landscape (often 1200×630), generous safe margins for crops/miniature previews, accessible contrast, correct alt/title/meta and reasonable asset weight.
- Inspect actual OG URLs, status/content type, shares/previews on relevant supported platforms, and mobile crops. OG images do **not** make Google display an image in every organic result.

### C. Search → landing continuity

- Test that the arriving visitor sees the promise from the snippet, on-brand above-the-fold content, usable navigation and **truthful functioning CTA**.
- Inspect mobile/desktop layout, keyboard and 200% text zoom, reduced motion, loading, images, link integrity, Core Web Vitals/performance evidence and relevant accessibility states.
- Refine composition/typography/motion deliberately for the product/client; remove generic decorative gradient/copy clutter and unused shiny components. Do **not** globally redesign an accepted website for a snippet fix.

### D. Trust outside the site

- Check verifiable managed brand profiles, consistent names and actual cases/mentions with permission. For eligible local businesses, legitimate location and listing/Business Profile management may help; ownership must be agreed with client.
- Do not buy/manufacture reviews, backlinks, press, listings, social proof or geo-addresses. Never create client accounts or edit DNS without authorized scope.

**Evidence format for a material visual decision:** real screenshot + route/URL + viewport/device + browser/source + date + release SHA where applicable + observed versus proposed. Apply `pat-visual-evidence-integrity` and `pb-frontend-quality-review`. The handbook does not prescribe a palette or generic marketing template.

## T5 — Implement only the relevant repo changes

Possible components depend on current stack and observed gaps:

- host/canonical and redirects;
- per-route metadata and language;
- crawler policy and sitemap;
- verified entity schema;
- existing favicon/logo assets and Open Graph renderer;
- content/navigation/heading fixes;
- route guard or exclusion tests;
- repo-local checklist and verification evidence.

For Agent Discoverability, record the approved content routes and exclusions
from the Standard §8. Reuse the canonical page/content pipeline. Keep generated
Markdown with the same build and keep form confirmations, authenticated data,
private APIs and gated demos out. Do not add DNS records for a brochure.

Never duplicate a working metadata system, invent new dependencies, install analytics without consent, change product architecture, collect new lead data or enable an intentionally disabled contact form to call a task "SEO done". The corporate MelodIQ-Web implementation details (e.g. `SEO-01` or its current `CONTACT_MODE`) are **example-specific**.

For materially visual changes, inspect the rendered pages before accepting. Record exact tests actually run, especially negative route/schema/claim tests. Security, performance, accessibility and legal/privacy remain first-order requirements, not secondary polish.

## T6 — Ship on the project's authorized path, then observe

Pre-release: confirm owner approval, factual/legal readiness, client sign-off if needed, tests/build, browser and asset checks. Use the site's **existing deployment path**; do not create a duplicate pipeline or publish across an unrelated project.

Post-release verification matrix:

| Check | Proof to retain | Failure to prevent |
| --- | --- | --- |
| Canonical/redirect | HTTP headers and final HTML of canonical + alternate hosts | Duplicate entity, endless redirect |
| Index/noindex/robots | HTTP/HTML per route + sitemap.xml | Gated preview exposed or live home left noindex |
| Identity/schema | DOM/JSON-LD validation, verified business source | Borrowed agency entity or false contact |
| Search/social visuals | Actual favicon/OG asset URL and rendered platform/browser screenshots | Globe icon, broken card, illegible mobile crop |
| User destination | Mobile/desktop/browser walkthrough, CTA and accessibility | Snippet promises unsupported feature or dead form |
| Build/deployment | Exact commit/release ID, production alias/date | Code verified locally but not published |
| Search ownership | Search Console property, sitemap/inspection outcome when authorized | Indexable claim based solely on a code diff |
| Multi-engine discovery | Bing Webmaster property/import, sitemap status, IndexNow applicability and submitted URL evidence | Assuming Google verification automatically covers Bing or that HTTP 200 means indexed |
| Local business profiles, when eligible | Google Business Profile and Bing Places business/owner/website consistency | Confusing a Maps listing with webmaster verification; stale business URLs |
| Agent discovery, when applicable | Real Link targets, repeated HTML/Markdown GET and HEAD with Accept quality values, Vary, cache and private negatives | Renamed HTML, mixed cache variants or private publication |
| DNS-AID, when applicable | Parent NS, authoritative and recursive SVCB answer, parameters, TLS and real advertised index/service | Mistaking an undelegated dashboard record or a brochure for a reachable agent |

### Search-engine and local-listing handoff — required for an approved indexable launch

Create one compact, repo-local onboarding status matrix **during intake** and finish it at release. Use the existing launch record rather than another tracker. The implementer proactively checks the following; each line records `DONE`, `OWNER ACTION`, `BLOCKED`, `NOT RUN` or `NOT APPLICABLE`, a responsible owner, observed result and next action:

| Surface | Implementer/agent work | Owner-only boundary and acceptance evidence |
| --- | --- | --- |
| Google Search Console | Confirm canonical domain/property, sitemap, robots, URL inspection of representative pages, errors and coverage | Owner authorizes verification/delegated access; a sitemap received by Google is not indexing |
| Bing Webmaster Tools | **Offer import from verified Google Search Console** when practical; otherwise guide independent site verification. Inspect Bing sitemap, index coverage/errors and optional Site Scan. | Owner authorizes the Microsoft/Google account connection or DNS/file verification; do not equate Bing acceptance with ranking |
| Google Business Profile, eligible businesses only | Confirm claimed real entity, current canonical website, name, service area, phone, hours and accessible link to site | Claim/update only with authorized owner; Google Maps presence does not verify Bing or Search Console |
| Bing Places for Business, eligible businesses only | Look for an existing listing and check claim status, website URL and consistent approved business facts; avoid duplicates | Authorized business owner claims/updates separately from Bing Webmaster Tools |
| IndexNow, participating engines only | Check if hosting/CMS already supports it. Where useful, configure **one** post-publication path for changed/added/deleted public canonical URLs, host-key verification and a safe delivery log; keep private/demo/preview routes excluded. | Domain/hosting owner approves key/configuration. Verify actual receipt; IndexNow does not cover Google and does not guarantee crawl/indexing |
| Other citations and directories | Identify owner-controlled profiles pointing to outdated domains, broken contact links or conflicting names; prioritize legitimate corrections and safe redirects from domains actually controlled | Do not claim rights to edit third-party sites or transfer an old domain without authorization |

### IndexNow: reusable post-publication implementation recipe

When approved for an indexable **production** website, treat IndexNow as an optional independent channel for participating engines. The implementation is part of the site delivery lifecycle, not a manual afterthought:

1. **Detect the existing provider.** Check hosting/CDN/CMS IndexNow support and whether it actually operates in the chosen traffic path. Enable just one notification channel, or implement a small repo-local notifier if the provider path cannot work. Do not switch proxy/DNS or add a service just for this feature.
2. **Prove host control.** Generate a random, site-specific protocol key; publish its exact value at the documented same-host HTTPS `<key>.txt` location (or an explicitly supported custom `keyLocation`). A public IndexNow proof key is not a credential. After release verify the live file is plain text with the expected body, not a 200 HTML fallback. Keep its ownership with the client's canonical domain.
3. **Select truthful URLs.** From the authoritative public sitemap and a diff/change feed between actual published versions, submit canonical same-origin URLs added, substantially updated or removed. A shared public layout/content change may affect multiple pages; a single page edit should not send the entire site. Handle deleted pages separately if no longer in the current sitemap. Exclude `noindex`, demos, auth/CRM, APIs, staging, redirects, unrelated assets and unchanged URLs. Do not blindly submit the sitemap at every build.
4. **Bind notification to the live release.** After the existing production gate passes, check that the **real public domain** is mapped to the exact verified release. On Vercel with explicit alias handoffs, a READY deployment is not proof of a mapped custom domain; check its live alias and use a retry tied to the successful release after delayed handoff. A release workflow can notify automatically only when that check passes. Never open indexing or create a deployment as a side effect of IndexNow.
5. **Send and observe.** Use the official IndexNow POST JSON format with `host`, `key`, `keyLocation` and `urlList` and bounded network timeouts. Treat 200/202 as accepted for processing; report 400/403/429/5xx and network failures without claiming success. Retain a compact timestamp, released SHA/deployment, affected URL count and response, and cross-check Bing Webmaster's IndexNow report if authorized. No requests to Google via IndexNow.
6. **Test before enabling.** Unit-test exact canonical URL selection, no private/cross-host URLs, single-route vs shared changes, deleted page handling, no request before a live alias, key verification failure and rejected POST. Validate live key, sitemap, alias and actual workflow result after the approved release. Distinguish `NOT RUN`, `NOT PUBLISHED`, `NO PUBLIC CHANGES`, `SUBMITTED` and `ERROR` in the handoff.

**Repo-local reference, not a cross-client template:** the Mudanzas Agurto implementation in `Kappa-Bot/Ops-OS` uses `scripts/public/indexnow.mjs`, `.github/workflows/indexnow.yml` and `docs/operations/AGURTO_INDEXNOW.md`. It consumes the successful existing Release artifact, checks the exact Vercel public alias, and allows a verified-release retry if the alias moves later. Adapt the trigger to each client's hosting process; never copy Agurto's host, key, provider IDs or private/business deployment gates. This playbook does not grant a new production release authority.

**Dependency ordering:** record delegated/account-access steps at T0, not after announcing the website is finished. The agent should handle the technical setup and verifiable checks whenever authorized access exists; where an OAuth, DNS, business claim or legal approval is genuinely owner-only, give a short precise handoff (service, account, action, expected confirmation) and retain an open status. Avoid making the client discover Bing, Places or a second search console independently.

**Post-release:** schedule no background automation without authorization, but recommend observable reviews around 2/4/8 weeks using both search engines' actual query/impression/index coverage data, branded vs. nonbranded discovery, canonical host and local profile consistency. Triage results into `submitted`, `discovered`, `crawled`, `indexed` and `shown/recommended` rather than collapsing them into one false `SEO done`. Never guarantee sitelinks, ranking, or an AI citation. Agent Link headers/Markdown/DNS discovery are complementary technical surfaces, **not substitutes** for search-engine registration, local reputation and relevant human-readable content.

### Reusable HTTP check

Run the dependency-free probe against the built server and again on the exact
authorized public release. Add the actual eligible pages and expected
exclusions; the fixture below is illustrative, not a universal route contract.

```sh
python automation/handbook/verify-agent-discovery.py --origin https://example.com \
  --page / --page /services --exclude /private=401
```

It exits nonzero for variant/status, Vary, missing/duplicate or failed
same-origin discovery links, or private exposure failures. It does not
follow redirects, fetch cross-origin links or use credentials. Verify intended
external targets, content fidelity, security/SEO header parity, provider cache
behavior and alias/deployment provenance separately. In CI run it after the
representative build or in a release smoke, not on every unrelated change.

For an approved DNS-AID deployment, sample `dig +trace <domain> NS`,
`dig @<authoritative-ns> _index._agents.<domain> TYPE64` and the same SVCB
query through a public recursive resolver; then verify the protocol and TLS
service named by the answer. Record the draft revision and distinguish a
positive answer from a valid reachable agent index. Do not alter DNS as part
of the HTTP probe.

When authorized and after indexable release, request relevant URL inspection and submit the sitemap through Search Console **and Bing Webmaster Tools where applicable**; preserve the **client's account/ownership** in lead-site projects. Record findings and errors; requesting a crawl is not equivalent to indexing.

When monitoring is separately authorized, comparison points around 2, 4, and 8 weeks (or the available traffic cycle) can inform branded/service queries, clicks/impressions/coverage, selected canonical, usability and truthful editorial improvements. This suggestion creates no scheduler. Use `pb-conversion-measurement-and-experiments` for consent-aware actual outcomes, not click-as-lead claims. Never guarantee date, rank, sitelinks, knowledge panel or AI Overview content.

## Common failure diagnosis

| Symptom | Investigate first | Do not assume |
| --- | --- | --- |
| Only bare URL/no snippet | Robots/noindex/crawl accessibility, sitemap/canonical, rendered useful content | Meta description missing until HTML checked |
| Wrong entity or unrelated AI answer | Consistent actual business identity, crawlable home, authentic citations/official profiles | AI Overview controllable by `JSON-LD` |
| Generic globe instead of icon | Favicon endpoint, file, URL stability/crawl, search engine recrawl | Icon file exists in repo means Google uses it |
| Broken social image/attachment | `og:image` URL, HTTP/content type, dimensions, preview cache, permissions | Browser page design dictates social renderer |
| Wrong page ranks/canonical | Redirects, duplication, thin content, internal links, Search Console selection | Sitemap forces ranking |
| Local business not found | Legitimate eligibility, accurate service/location, verified owner/business profile | Fabricating an office is acceptable |
| Mobile visual looks cheap | Real page, crop, hierarchy, typography, contrast, brand asset, real-use QA | Add more gradients, cards or animations |
| Search looks good, no leads | Honest offer/CTA, contact functioning and privacy-compliant funnel | More keywords fix a broken form |

## Handoff artifact per website

Attach an intentionally small, repo-local search presence record (in an existing release checklist if available):

- Site/customer, authorized owner, canonical origin, final publication approval.
- Route matrix + exceptions (`indexable`, `noindex`, `private`, `preview`).
- Verified entity/brand fact sources and asset ownership (links, never secrets).
- Status of SEO technical checks, Google Search Console, Bing Webmaster Tools, eligible Google/Bing local business profiles, IndexNow and each owner's access/action.
- Exact release SHA/URL, date, tests run and `NOT RUN` gates.
- Search-result observations separate from mockups; screenshot/device/provenance.
- Next review date, outstanding issues, no ranking/AI-generated-answer promises.

This creates repeatability for dozens of vertical or lead websites **without centralizing sensitive client data** or imposing MelodIQ's design identity on other businesses.

## Definition of done

The work is complete when the approved release state and technical search signals agree, the site depicts the right real entity with usable branded visual previews, the landing delivers what the snippet promises, and deployment/verification evidence is recorded. External ranking/indexation/AI summary evolution remains monitored, not asserted.
