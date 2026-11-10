---
id: std-public-web-discoverability-baseline
kind: standard
status: active
owner: engineering
version: "0.3"
applies_to:
  - public-marketing-websites
  - indexable-product-vertical-pages
  - client-business-websites
  - public-documentation-and-apis
  - public-agent-services
sources:
  - src-google-seo-starter-guide
  - src-google-block-indexing
  - src-google-sitemaps
  - src-google-site-names
  - src-google-favicon-search
  - src-google-organization-structured-data
  - src-open-graph-protocol
  - src-google-ai-features
  - src-rfc-8288
  - src-rfc-9110
  - src-rfc-9727
  - src-iana-link-relations
  - src-cloudflare-markdown-agents
  - src-rfc-9460
  - src-ietf-dns-aid-draft
last_verified: 2026-11-10
review_due: 2027-02-10
---

# Public Web Discoverability & Search Brand Baseline

## Purpose, scope and authority

Define an evidence-based quality floor for **public websites intentionally eligible for organic discovery**, including MelodIQ Systems corporate surfaces, public landing pages for product verticals (Ops OS, Dental OS, Church OS, etc.) and websites delivered to individual businesses/leads.

This Standard governs **the technical and truthful prerequisites we control**: indexability policy, crawl/metadata consistency, identity, structured data, visual previews, trust and verification. Search ranking, featured answers, site names, knowledge panels, chosen snippets, sitelinks and AI-generated summaries remain decisions of the search engine and **MUST NOT** be promised as guaranteed deliverables.

Use `pb-public-web-discoverability-launch` for the implementation/operational sequence. Use `std-ui-ux-quality-baseline` for the actual public page, `pat-design-context-layering` for brand-specific systems and `pat-visual-evidence-integrity` for rendered evidence. The client/site repository retains its own business identity, route inventory, legal obligations, launch approval, framework details, deployment configuration, owner and visual art direction. A corporate example never becomes default branding for client sites.

### In scope and intentional exclusions

| Surface | Default policy | Boundary |
| --- | --- | --- |
| Live corporate marketing site | Indexable **after** its repo-specific release approval | Legal/public identity and operational claims must be publishable |
| Public vertical product/service landing | Indexable when accurate, useful and genuinely released | Do not imply that an unfinished SaaS module is available |
| Client or lead website published under its brand | Indexable after the client's authorized publication gate | Client owns its business facts; use client domain/name/assets, not MelodIQ's entity |
| Demo, preview, staging or draft | Explicitly non-indexable by default; auth if confidential | A public preview link is not approval to index |
| Authenticated CRM, tenant data, admin, API, restricted files | Excluded from public search inventory | `robots.txt`/`noindex` are not access controls: protect sensitive resources at their actual security boundary |

Intentional non-indexation is a valid product state, **not automatically a defect**. Opening a closed site to crawlers, enabling collection forms, changing client DNS or connecting analytics/third-party services is a separate, authorized release decision, not a cosmetic SEO fix.

## 1. Ownership and discoverability contract

For every release/major redesign that changes public discovery, the owning repository MUST identify:

1. Real public entity and its **verified** published business name (and permitted variations), canonical origin and domain operator.
2. Route classes: indexable public, public-but-excluded, private/authenticated, preview/draft, redirect and removed.
3. Explicit launch/indexability state and decision owner; repo-specific legal, privacy, consent, contact and availability blockers.
4. Target audience/intention, language/locales and the action a visitor can genuinely perform on each important destination.
5. Assets and external profiles the owner has rights to publish; client approvals and delegated Google Search Console/DNS access if applicable.

The contract MAY live in the repo's existing launch checklist/operational spec; **do not create a second competing tracker**. A reusable website template MAY offer a safe initial non-indexable profile, but MUST require an explicit publication decision per customer and domain.

## 2. Crawl, indexing and canonical coherence

For a site deliberately opened to search:

- `robots.txt`, meta robots, `X-Robots-Tag`, canonical links, HTTP status, redirects and sitemap MUST express a coherent route policy. A broad `Disallow: /` or global `noindex` MUST NOT remain accidentally active after launch.
- A `noindex` directive MUST be crawlable by engines expected to honor it. Blocking that URL in robots may prevent the crawler from seeing `noindex`; relying on both at once is not an effective removal strategy. No robots directive substitutes for authentication/authorization.
- Pages selected as canonical SHOULD return normal successful HTML at their final canonical host/protocol; alternate www/apex, HTTP/HTTPS or trailing-slash variants SHOULD resolve consistently rather than produce competing identities.
- A published sitemap SHOULD reflect the **actual intentionally indexable canonical URLs**, excluding demos, login, admin, API, unpublished clients, search/filter variants, broken pages and redirects. Use genuine modification timestamps when supplied; omit fabricated `lastmod`.
- For multilingual content, advertise only real maintained locale versions and use consistent canonicals and `hreflang` when warranted. Do not create empty/duplicate localized or service-area doorway pages.
- Missing, retired or nonexistent routes MUST return honest 404/410 or appropriate redirects, not generic 200 landing pages that imply content exists.

Scope matters: a one-page brochure may not need an elaborate sitemap generator, but it still requires explicit indexability/canonical behavior. Never force PWA/offline, CMS, SEO SDKs, cookies, analytics or automated page factories for the sake of a checklist.

## 3. Page metadata and genuinely useful information

Each important indexable page SHOULD provide:

- A concise, purpose-specific HTML title, non-spammy meta description, correct language and one meaningful primary page heading.
- A self-consistent canonical URL and crawlable, semantic HTML content/navigational links. Key brand/service information must not exist *only* in client-side state inaccessible to crawlers.
- Distinct copy matching the real visitor question: service offered, audience, scope, location **only when true**, differentiating evidence and next action. Never copy the same generic AI-written pitch across clients or create pages solely for variants of a keyword.
- Internal links with comprehensible labels to relevant real pages; important pages should be reachable without speculative sitemap or UI-only navigation.

The search engine may rewrite the displayed title or snippet. A provided description is a useful input, **not a control over Google's final text**. A click-through destination MUST substantiate what the search preview and CTA promise.

For Google AI features, the current official guidance introduces no extra AI-only eligibility requirement beyond normal search foundations. Do not claim that a special file, schema or wording guarantees inclusion/citation. Other engines' behavior requires their own current primary evidence; speculative tactics do not override this Standard or the site's publication decision. Commercial context and proof are maintained through `pb-marketing-context-and-content`, not a second SEO brief.

## 4. Entity, structured data and local business truth

Structured data MUST reflect publicly visible facts the site owner has verified.

- `WebSite` on the homepage MAY supply preferred site name and canonical URL; avoid duplicate, contradictory `WebSite` entities. Site-name choice is automated and domain/subdomain-scoped, **not freely selectable per subdirectory**.
- `Organization`, an eligible `LocalBusiness` subtype, `BreadcrumbList` or other schema MAY be used only where supported by the real content and primary search-engine documentation. Type selection should follow the actual entity, not perceived rich-result value.
- Published `legalName`, address, company form, registration/tax identifiers, phone, email, service area, opening hours, `sameAs`, logo, `priceRange`, reviews, ratings and offers MUST NOT be fabricated, inferred from unrelated businesses or copied from the web agency into a client's entity.
- `sameAs` links require controlled/verified official profiles. Public client testimonials/case studies require genuine evidence and publication rights; review markup must follow the target engine's current eligibility rules.
- JSON-LD MUST be serialized safely (including escaping markup-breaking characters when embedded in HTML), free of duplicate IDs/contradictory canonical hosts, and checked against the actual served DOM. Schema validators test syntax/eligibility, **not** guaranteed visual features.
- Local business listings and Google Business Profile require the business to meet applicable eligibility criteria; do not register fictitious offices, virtual locations or duplicate profiles for acquisition advantage.

One agency may manage implementation, but the client’s entity, name, domain, legal details and listing ownership remain the client's unless a real agreement states otherwise.

## 5. Search and social visual quality

A technically correct site with a generic globe icon, broken social card or misleading brand treatment has not met the intended brand-discovery outcome.

- Each live site SHOULD ship a **genuine**, recognisable, crawlable favicon on a stable URL, square and legible at small sizes, matching that site's authorized identity. For Google search, follow current favicon size/crawl rules (the present guide recommends larger than 48×48 while requiring at least 8×8); verify the served file rather than only the asset manifest.
- Company/logo structured-data assets, if present, MUST be genuine and available over the declared canonical origin; validate the current engine's resolution/crawl requirements separately from favicon requirements.
- Public page previews SHOULD have coherent Open Graph metadata (`og:title`, `og:type`, `og:image`, `og:url`) and relevant social descriptions. A 1200×630 landscape composition is a useful **design target**, not a universal protocol requirement or promise about Google organic images.
- Visual review SHOULD cover: 16–48px favicon rendering, light/dark search backgrounds, full and cropped social previews, mobile/desktop landing, typography/contrast/legibility, accessible text alternatives, image weight/performance and fidelity to client/vertical brand.
- Where stronger art direction is warranted, explore purposeful creative alternatives (e.g. restrained brand, editorial offer, authentic sector context). **Do not turn visual consistency into identical agency templates**, synthetic logos, unlicensed client assets, AI-slop decoration, fake screenshots or invented achievements.
- SERP and AI-result mockups MUST be labeled as *proposals*. Real search results and social cards require actual observed screenshots with query/date/locale/device and source provenance; apply `pat-visual-evidence-integrity`.

The landing page itself MUST meet `std-ui-ux-quality-baseline`: responsive navigation, keyboard and WCAG accessibility, clear offer/next step, reliable forms/links when advertised, and a measured rather than imagined performance story.

## 6. Release safety, privacy and verifiability

- **No silent indexing unlock:** public launch approval MUST precede opening previously withheld routes. If the release gate is blocked by incomplete identity, legal notices, unsupported claims, nonfunctional contact, privacy/security work or client sign-off, retain the approved exclusion while completing independent safe tasks.
- **No sensitive publication:** check rendered metadata, sitemaps, robots, social tags and JSON-LD for unreleased customer names, personal data, private URLs, bearer links, demo payloads and staging hosts. SEO is never a reason to expose a resource that should require authorization.
- **No covert marketing instrumentation:** analytics, maps, embedded media, retargeting, marketing SDKs and cookie/consent flows require the repo/client's approved legal and privacy decision; discoverability does not require tracking.
- **No deceptive growth:** no fake reviews, backlinks, addresses, offices, pages, deadlines, rankings, AI answers, citations, client names, prices or product maturity. Do not purchase link schemes or promise first position.
- **Proof corresponds to release:** verify exact code/config/deployment revision, HTTP/HTML served on both the canonical and redirect host, asset responses, route inclusion/exclusion, Search Console where authorized, browser previews and actual rendered pages. Record `PASS` / `FAIL` / `NOT RUN` separately. CI alone does not prove Google indexed the site.
- **Monitor after publishing:** track coverage, selected canonicals, search queries, branded disambiguation, user click-through, real conversions when lawfully measured, Core Web Vitals/performance and mobile UX. Sample checkpoints at 2/4/8 weeks are operational suggestions, not guaranteed indexing windows.

When browsers, domains, client approval or Search Console are inaccessible, disclose the blocker and keep claims limited to what was observed.

## 7. Adoption across the portfolio

| Consumer | Apply | Keep local |
| --- | --- | --- |
| MelodIQ Systems corporate | Entity clarity, branded SERP, internal linking, OG/favicon, launch SEO gate | Exact public/legal identity, CONTACT_MODE, approved brand pack, source repo's SEO-01 decision |
| Ops OS / Dental OS / Church OS | Public solution/sector landing discoverable by real problem and service; app/dashboard excluded | Release maturity, product claims, tenant routing, auth boundary, visual identity of each vertical |
| Client/lead website | Real customer entity, real services/location, explicit domain/indexability handoff, lead-contact conversion | Customer brand, consent, photos/reviews, service area, ownership of DNS/Search Console, copy and legal facts |

**Migration note:** Existing repositories are not authorized for automated SEO reconfiguration by publication of this Standard. First classify routes and original launch decisions; then adopt via `pb-public-web-discoverability-launch` as a scoped change. A deliberately `noindex` project remains so until its release owner explicitly approves opening it.

## 8. Agent Discoverability

Apply this contract when creating, auditing or materially changing an
intentionally public surface. Start with the route classification in §1.
An alternate representation is another publication boundary, not new access.

| Surface | Default | Exception or limit |
| --- | --- | --- |
| Public commercial site | Useful HTTP Link relations and negotiated Markdown for eligible content pages | Document a scoped safety, fidelity, cost or platform exception; keep ordinary HTML |
| Public documentation | Advertise real documentation and offer its maintained Markdown representation | Reuse the existing content pipeline instead of introducing another copy |
| Private CRM, admin, tenant API, gated demo | Do not advertise or convert restricted content as public Markdown | Preserve authorization and exclusion under every Accept value |
| Published API or agent service | Advertise maintained documentation; use a real RFC 9727 catalog and/or DNS-AID only where applicable | An internal endpoint, brochure or content index is not a public API or agent registry |

**HTTP Link.** Use RFC 8288 syntax and IANA relation semantics. For example,
`describedby` may identify a genuine site/content description, and `alternate`
with `type="text/markdown"` may identify the same negotiated document. Verify the
actual targets and deduplicate values without discarding existing canonical or
preload links. `api-catalog`, `service-doc` and `service-desc` require the real
resources they imply. An optional `/llms.txt` should have a maintained source,
valid public links and useful content; it is not an SEO ranking prerequisite.

**Markdown.** Negotiate `Accept: text/markdown` using RFC 9110 media ranges,
specificity and quality weights; preserve HTML by default for missing/wildcard
requests. Use `text/markdown; charset=utf-8` and merge `Vary: Accept` on all
variants, retaining framework variation and security/indexability headers. Verify
GET and HEAD, existing redirects/statuses, conditional/cache behavior and
alternating real HTML and Markdown requests. Generate the representation from
the same approved public source or rendered content. Keep meaningful headings,
text and links; omit scripts, UI chrome, serialized state and private or
personalized data. Do not perform network conversion of arbitrary request URLs.
Only emit `x-markdown-tokens` when a defined tokenizer actually measured it.

**Implementation and caching.** Prefer precomputed public representations for
static content; on Vercel or another origin, use an allowlisted route adapter and
verify the built output plus the deployed cache key. On an authorized Cloudflare
zone the managed transform is an alternative, not a prerequisite. Choose one
conversion owner. Test a provider transition before enabling another transform.
If variant separation is not proven, disable shared caching for the affected
variant or keep the capability disabled until the issue is resolved. Never
broaden private routing or change crawl, AI training or consent policy to pass
an agent-readiness scan.

**DNS-AID.** Treat `draft-mozleywilliams-dawn-dnsaid-00` as a changing Internet-Draft,
not an RFC; SVCB transport is specified by RFC 9460. Publish only for an approved,
real public agent service or registry. Confirm the latest draft and registered or
experimental parameter semantics. For an organizational `_index._agents` entry,
verify the intended index protocol, endpoint and TLS, positive ServiceMode
priority (use the lowest priority for the preferred service), target hostname,
and only parameters that describe what the target actually supports. Verify the
parent delegation, authoritative answer and recursive visibility independently
of a provider dashboard, then fetch the real public service/index. Record
`NOT APPLICABLE` when no service exists or `NOT ACTIVE` when an undelegated zone
contains the record. DNS write/registrar authority is separate from HTTP release.

## Verification / Definition of Done

For a **site being made indexable**, the relevant release record MUST evidence:

1. Authorized release/indexability scope; no blocked legal/client/availability gate silently bypassed.
2. Intended public routes and private/demo exclusions correct under rendered HTML, HTTP headers, robots, canonical and sitemap.
3. Titles/descriptions/primary content consistent and useful, no false brand or entity facts, safe verified schema (when implemented).
4. Correct site favicon/brand assets, OG links/rendering, destination usability/mobile/a11y/performance review proportionate to scope.
5. Build and deployment provenance + post-release smoke, Search Console submission/diagnosis if access exists, unresolved gates marked `NOT RUN`.
6. Explicit distinction between *eligible to be indexed* and *actually indexed/displayed by the search engine*.
7. Applicable Agent Discoverability coverage or justified exclusions (§8);
   verify negotiated variants and private negatives on the exact hosted revision.

Never mark ranking, featured SERP appearance, AI Overview wording or knowledge-panel inclusion as a technical acceptance guarantee.

## External evidence

Source IDs are registered centrally in `machine-readable/sources.yaml`. Technical behavior is drawn from the official Google Search Central guidance (SEO fundamentals, noindex, sitemap, site names, favicon and Organization schema) and the original Open Graph protocol. Authority does not bypass per-client applicability and external search engines may change presentation rules.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "public-discoverability-truth-and-exposure",
      "type": "constraint",
      "force": "must",
      "text": "Apply std-public-web-discoverability-baseline and pb-public-web-discoverability-launch. Preserve approved noindex/private/demo gates; robots is not access control. Verify routes, canonicals, visible truth and rendered evidence. On eligible public content, default to real Link relations and negotiated Markdown from one source. DNS-AID is conditional on a real public agent service and authorized DNS. Eligibility is not indexing or AI citation.",
      "source": "std-public-web-discoverability-baseline",
      "covers": ["search-exposure", "commercial-truth"],
      "activate_when": ["archetype:public-discoverability-change", "archetype:public-client-website"],
      "phase": ["planning", "implementation", "verification"],
      "priority": 92
    },
    {
      "id": "public-agent-discovery-http-evidence",
      "type": "verification",
      "force": "must",
      "text": "For applicable public discovery, verify the exact hosted HTML/Markdown Accept and HEAD matrix, Vary/cache, real Link destinations and private negative cases. Record exemptions and DNS-AID authoritative/service evidence separately. Use the launch playbook's reusable HTTP probe.",
      "source": "std-public-web-discoverability-baseline",
      "covers": ["search-exposure"],
      "activate_when": ["archetype:public-discoverability-change", "archetype:public-client-website"],
      "phase": ["verification"],
      "priority": 91
    }
  ]
}
```
