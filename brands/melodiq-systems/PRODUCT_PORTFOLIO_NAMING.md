---
id: brand-melodiq-systems-product-portfolio-naming
kind: brand-naming-contract
status: owner-approved-naming-direction
owner: brand-owner
last_updated: 2026-10-09
applies_to:
  - melodiq-product-portfolio
---

# MelodIQ Systems — product portfolio naming

The owner chose a coherent **MelodIQ [Vertical] OS** naming system on 2026-10-09. This is a portfolio product-name decision, **not trademark clearance**, a legal-entity change, a universal design theme, or authorization to break production infrastructure.

## Canonical product names

| Product full name | Short UI/product name | Former working names | Known current repository | Status |
|---|---|---|---|---|
| **MelodIQ Ops OS** | **Ops OS** | JobOps OS, MovOps OS, Operations OS | `Kappa-Bot/movops-os` | Existing product; identity migration pending release safety gates |
| **MelodIQ Church OS** | **Church OS** | ChurchOS | `Kappa-Bot/churchos` | Existing product; identity migration pending dependency audit |
| **MelodIQ Dental OS** | **Dental OS** | DentalOS | `Kappa-Bot/DentalOS` | Existing product/prototype; identity migration pending |
| **MelodIQ Style OS** | **Style OS** | Style OS | No dedicated repository identified in the October 9 inventory | Naming approved; do not create a product or claim implementation |
| **MelodIQ [Vertical] OS** | **[Vertical] OS** | Existing working label, if any | Discover individually | Apply only to existing or explicitly approved future products |

The brand casing is precisely **MelodIQ** (capital M, capital IQ). Write full product names with spaces as above. Do not abbreviate `MelodIQ` to `MelodiQ`, `Melodiq`, `MeloDIQ`, or `MIQ`.

### Corporate and customer identities

- **MelodIQ Systems** is the developer/company brand and remains the attribution in product About sections, footers, proposals, and legal text when factually correct. Do not invent `S.L.U.` or registration claims.
- **MelodIQ [Vertical] OS** is the product brand.
- **[Vertical] OS** is a short, context-appropriate product display name when the full vendor name would create unnecessary repetition.
- **Tenant/customer brand** is independent. For example, Agurto may display `Agurto · Ops OS` in its private application. The public Agurto website stays Agurto.
- `Platform Core` and `Platform Admin` are technical/control-plane products, not automatically rebranded into invented customer verticals.

## Distinction between naming and code vocabulary

Product naming changes must NOT indiscriminately rename:

- `Job`, `jobs`, `jobId`, or persisted service keys such as `move`, `transport`, and `assembly`;
- provider IDs, database project refs, tenant UUIDs, connection strings, OAuth callback URLs, secrets, access tokens, and cookie names;
- historical commits, migrations, release evidence, sent email, legal history or prior review verdicts.

Technical identifiers may be migrated separately **only where the current consumer inventory, compatibility path and release evidence justify it**.

## Implementation/cutover order

1. Discover affected current repos, branch/release state, deployments, DB project display names, CI integration names, connected Drive CRM, Apps Script, proposal masters and Gmail drafts. Read before write. No generic replacement across arbitrary repositories.
2. Update current master marketing copy and commercial presentation for the approved full names, preserving inline logo/identity assets. Never send an email as part of this naming migration.
3. In the CRM, user-facing labels can change before physical sheet titles. Current `ChurchOS` and `JobOps OS` sheet titles, `Config` keys and sheet IDs are active formula/automation contracts and must not be renamed until dependencies have been migrated/tested. Preserve all lead data and statuses.
4. Per product, make a bounded source PR for public/private display names, title/meta/PWA, About, downloadable documents, repository documentation and current commercial templates. Respect tenant and corporate design authorities; do not import the MelodIQ corporate theme into vertical products.
5. After the product's current QA/Production release is certified and no promotion PR is active, coordinate provider display-name changes: GitHub repository name, Vercel project display name and Supabase project display name. **Rename existing resources, never recreate them.** Preserve stable numeric IDs/project refs, backups, schema history, deployments and customer data.
6. Verify all references and integrations: Git remotes, branch protection/Actions, provider Git link, deployment/webhook URLs, deployment aliases, OAuth redirect allowlists, Vercel/Supabase secrets and environments, scripts, source maps and operational docs. Only change a stable URL if a verified redirect/cutover explicitly requires it.
7. Certify old-name search results by semantic category: current product/marketing (remove), technical compatibility (document), stable provider identity (retain until migrated), historical evidence (preserve). Validate exact QA and Production after relevant provider changes.
8. Remove temporary compatibility only when the current consumer is zero and the release test proves no breakage.

### Active release safety

As of the initial October 9 discovery, `Kappa-Bot/movops-os` still has a temporary Production promotion PR in progress. **Do not rename its GitHub/Vercel/Supabase resources or rewrite its release source while that PR or its Production smoke/release gate is active.** First finish and certify the running release. ChurchOS also has a live feature branch; preserve its work and integration references.

## Trademark/commercial clearance

These names are **approved working product names**, not demonstrated exclusive or registrable marks. In particular `Ops OS` / `OpsOS` and `Operations OS` overlap in ordinary software-market usage. Adding `MelodIQ` does not independently guarantee freedom to operate. Before broad public launch or trademark filing, verify the full names and confusingly similar signs in appropriate markets and Nice classes (especially software and SaaS) through OEPM/EUIPO and obtain specialist advice where warranted. No filing, legal fee or domain purchase is authorized by this document.

## Operational bookkeeping

- Registered product name decisions: approved.
- Commercial master template names in `Templates de Email — Copiar y pegar`: updated October 9, 2026.
- MelodIQ Leads CRM presentation labels: updated October 9, 2026. Technical tab names/IDs and taxonomy keys retained intentionally.
- Existing Gmail drafts and sent mail: not mass-modified by this document.
- Product source/repositories, GitHub repository names, Vercel/Supabase projects: not renamed by this document.
- Product UI metadata/release cutovers and legal clearance: pending independent execution/verification.

No unrelated portfolio app is renamed merely because it shares a GitHub organization.


## MELODIQ-NAME-1 — verified execution inventory (2026-10-09)

This section records the current owner-approved migration direction and **read-only provider inventory** for a future Codex/Work execution. It is **not evidence of a completed provider rename**. Re-query identities, live Git heads, pending PRs and deployments at the start of every cutover. Do not repeat prior discovery unless live state differs.

| Product | Existing GitHub repo | Proposed GitHub repo | Vercel project ID / current name | Supabase ref / current display name |
|---|---|---|---|---|
| MelodIQ Ops OS | `Kappa-Bot/movops-os` | `Kappa-Bot/melodiq-ops-os` | `prj_ijAKWddbGQnLTyFiSZLvc4I9aN2X` / `movops-agurto` | `xgtyuntpahegyjndwbmw` / `MovOps-OS` |
| MelodIQ Church OS | `Kappa-Bot/churchos` | `Kappa-Bot/melodiq-church-os` | `prj_9WpMVpjisFS1bC25939dpZs2DZan` / `churchos` | `rjfvvobpnxqmjqmlkkue` / `ChurchOS` |
| MelodIQ Dental OS | `Kappa-Bot/DentalOS` | `Kappa-Bot/melodiq-dental-os` | `prj_cz5M7VMwCNSFyrOrYUv112W5lSNf` / `dentalos` | `ykfejwxyxqcgycnwuzbu` / `DentalOS` |
| MelodIQ Style OS | No verified repo | None until a real product exists | No verified project | No verified project |

All three listed Supabase projects were ACTIVE_HEALTHY on the inventory read. Their refs and Vercel numeric IDs **must remain unchanged**. Current Vercel project target names to validate for uniqueness when ready: `ops-os-agurto`, `melodiq-church-os`, `melodiq-dental-os`. Do not change any pre-existing Production alias or app URL merely because the project display name changes.

### Confirmed release dependencies

- **Ops:** at read time, `main@e826828cd3c6cba9c431892baf1cc9a0d83e2074` and `qa@960a7540804b8838148f7698aac9f1827d9d5fd8`, with open Production promotion PR **#158** from `release/09a74236000a051ca7f077000daaf174a48fe944`. **Do not rename GitHub, Vercel, Supabase or cross-provider references until the PR is merged, the exact Production deployment and synthetic durable smoke pass, Production Release succeeds, and the release branch is disposed safely.** Preserve `qa`; do not close the release by renaming underneath it.
- **Church:** `main@f6b7c34cc14f0cf5c0d3f333a062997eea1fecc7` and in-flight `feat/platform-core-consumer-admission@10abf35b20dc0a7d279fe3aece9bd0c596a05229`. Inventory and preserve all references in the active Platform Core consumer branch before repository/provider renames.
- **Dental:** `main@fae52a642e7f4432ba312fa4517577f4a8d07718` and persistent `qa` exist; no open PR at read time. Product remains a synthetic prototype, not certified clinical Production. Do not imply real patient data or certifications.

### Per-product cutover definition

1. Baseline **current** repo/provider refs, branch protections, Git remotes, deployments, domain aliases, build/env/PWA, OAuth callback/redirect allowlists, webhook destinations, Supabase project name and public/private connection strings, Apps Script, Google Sheets and Gmail drafts. Record exact consumers. Do not expose secrets.
2. Make one bounded source PR for **display names and metadata only**, optionally plus compatible source code identifiers after consumer analysis. Do not rename domain types or stable keys by grep. Run full affected CI and rendered verification before merging.
3. Rename the **existing** GitHub repository only with repository admin authority; confirm former Git clone/HTTP links, Actions and Vercel Git source still work. A read-only connector or lack of admin access is a blocker, **not permission to recreate the repository**.
4. Rename existing Vercel project display name only using the stable numeric project ID, then re-read project/deployments, preserved Production aliases and Git integration. Redirect/hostname changes require separate explicit verification.
5. Rename only the Supabase **display name**, preserving the exact project ref/DB/history/storage and all grants. If a connected tool cannot edit this metadata, use an authorized admin path; do not create a replacement project or issue unreviewed SQL.
6. Verify end-to-end CI, Git/Vercel/Supabase connectivity, authentication/session continuity, public and private URLs, assets/PWA, logs/telemetry and customer isolation. Roll back an individual display-name change when supported and safe if a consumer breaks; never roll back data or force-push.
7. Update the MelodIQ CRM and Gmail **model templates only** by preserving Sheets technical tab IDs/formulas and email HTML/CID image relationships. Existing personalized drafts, sent mail, outreach automation state, lead data and user accounts are out of the mass-rename scope. The canonical document/template and CRM visible headings were already updated in a separate operation.
8. Commit exact before/after names, metadata, verification results, external limitations and residual historical compatibility under each product's local operations log. Close the cutover only when old names remain solely as provider compatibility or historical truth.

**Gates:** zero incremental monetary cost, no unrelated repository changes, no Product/Production claims without live evidence, no bulk image regeneration or corporate palette overwrite, and no unilateral trademark registration/public brand exclusivity claim.
