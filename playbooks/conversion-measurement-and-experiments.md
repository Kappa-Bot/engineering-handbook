---
id: pb-conversion-measurement-and-experiments
kind: playbook
status: active
owner: engineering
version: "0.1"
applies_to:
  - marketing-workflows
  - public-marketing-websites
  - analytics
sources:
  - src-marketingskills
  - src-eu-gdpr
  - src-aepd-cookie-guide
  - src-google-analytics-pii
last_verified: 2026-11-09
review_due: 2027-02-09
---

# Conversion measurement and experiments

## Scope and prerequisites

Use when defining or changing commercial outcome measurement, conversion tracking/attribution or A/B experiments. This procedure is provider-neutral: inspect existing application/native events, tag managers, server senders, consent control and destination owners before adding another sender or service. A public site does not need analytics merely to be discoverable. Adoption provenance and MIT notice: `ref-marketing-skills-adoption-assessment`.

Preserve the existing implementation and task authority. New vendors, accounts, ad spend, customer-data transfers, live submissions or outbound calls require explicit scope. Reuse `pol-truthful-engineering`, `pol-verification-definition-of-done`, the site's privacy/release decision and `pb-lead-qualification-and-handoff`; this document does not authorize rollout.

## 1. Define the outcome before the event

| Outcome | What the observation actually establishes |
| --- | --- |
| Phone/WhatsApp link clicked | Intent to open a channel; not a completed call, sent message or lead |
| Form accepted | Valid request accepted by the owning backend; not yet guaranteed downstream receipt |
| Lead received | Persisted/received in the intended authorized destination, with traceable acknowledgment |
| Qualified / meeting / opportunity | The specific local stage criterion was met; distinguish booked from held |
| Won / revenue | Confirmed contract/financial event under the local definition; not estimated pipeline value |

Name events after their real trigger. A static demo may record an explicitly authorized intent event, never simulated business success in production reports. For a real form, trigger acceptance from confirmed success rather than button click, validation start, a thank-you page reload or a timeout. Receipt at each asynchronous boundary is separate evidence.

Record a minimal repo-local event contract: business question, event name/version, owning trigger/sender, intended destination, allowed parameter types, consent/legal basis, nonpersonal deduplication identifier, environment exclusions, attribution method/window, retention/access owner and verification query. Reuse an existing contract instead of inventing another tracker. Do not standardize provider-specific names or attribution models without current official documentation.

## 2. Privacy and integrity checks

Apply current GDPR and AEPD cookie/storage-access guidance with the responsible owner. Nonexempt tracking waits for the required valid consent; consent refusal or withdrawal is an expected state, not a defect to bypass. An exemption needs an applicable documented basis, not a vendor label. Server-side forwarding, hashing and consent mode do not by themselves grant permission or remove personal-data obligations.

Use an allowlist, not an unrestricted payload dump. Do not send form free text, names, email, phone, bearer links, patient/health information or religious membership/activity into marketing analytics. Inspect URLs, titles, query strings, campaign tags, identifiers and errors for leaks. Google Analytics separately prohibits identifying information under `src-google-analytics-pii`; consent alone does not override that product restriction. Review any proposed user-level linking with the authorized data owner rather than treating pseudonymous IDs as anonymous.

Prevent double counting across browser/server/native senders, retries, double taps and reloads using the chosen destination's actual deduplication contract. Exclude test, preview, demo and internal traffic using explicit environment rules. Keep aggregate limitations visible: blocked/denied tracking, missing journeys and model-dependent attribution mean analytics may not equal the CRM's actual lead count. Do not “repair” the difference by collecting disallowed data.

## 3. Verify the complete authorized path

Test with synthetic/minimized data and an approved destination. Cover success, client/server validation failures, backend failure, retries, repeated submissions, reload/back navigation, denied consent, accepted consent and withdrawal. Check the browser payload and actual destination receipt/count; a tag firing locally is not end-to-end proof. Verify no success event on failure, no unexpected duplicates, no fixture pollution and no disallowed personal parameters.

Record exact revision, environment, contract/event version, test inputs, expected versus observed counts and `PASS` / `FAIL` / `NOT RUN`. If access to a destination is missing, report that boundary as unverified. Do not create a real lead, send a real message or spend money to obtain proof without authority.

## 4. Decide whether an experiment can answer the question

Prespecify one falsifiable hypothesis, eligible population/unit of randomization, control/variant, primary metric and denominator, allocation, guardrails, analysis method, minimum effect worth detecting, justified sample/traffic needs, minimum duration and stopping/decision rules. Derive traffic assumptions from available evidence; upstream tables and vendor benchmarks are not universal thresholds. Keep exposure assignment stable and check allocation/data quality before interpretation.

Measure the outcome the decision needs, not an easier vanity event. Changing the primary metric, segment or stopping rule after looking at results changes the evidence; document exploratory analyses separately. Record uncertainty, practical relevance and guardrail outcomes, not just a favorable percentage or p-value. No unplanned peeking or repeated segments masquerading as a single conclusive test.

With insufficient traffic, recommend a bounded usability/content review, repair an observable failure, or extend/defer an authorized experiment. Report **inconclusive**, not “no effect” or a fabricated winner. Roll out only within approved scope with rollback criteria; retain the result in the existing local context as evidence, not an automatic cross-project rule.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "conversion-success-and-data-boundary",
      "type": "pattern",
      "force": "should",
      "text": "Use pb-conversion-measurement-and-experiments: inventory existing senders; define intent, accepted submission and destination receipt separately. Use a minimal approved event/consent contract, deduplication and demo/test exclusions. Do not send PII or sensitive/free-text data to marketing analytics; consent refusal is not a bug. No new service, transfer or live test without authority.",
      "source": "pb-conversion-measurement-and-experiments",
      "covers": ["measurement-integrity", "marketing-privacy"],
      "activate_when": ["archetype:conversion-measurement"],
      "phase": ["planning", "implementation"],
      "priority": 90
    },
    {
      "id": "conversion-end-to-end-evidence",
      "type": "verification",
      "force": "should",
      "text": "Verify the approved conversion path with synthetic data: success/failure, retries/reloads, deduplication, accepted/denied/withdrawn consent, environment exclusions and payload privacy. Check actual authorized destination receipt/count, not just a fired tag. Link revision and observed evidence; mark inaccessible boundaries NOT RUN. A phone/WhatsApp click does not prove a lead.",
      "source": "pb-conversion-measurement-and-experiments",
      "covers": ["measurement-integrity", "marketing-privacy"],
      "activate_when": ["archetype:conversion-measurement"],
      "phase": ["verification"],
      "priority": 94
    },
    {
      "id": "marketing-experiment-evidence",
      "type": "pattern",
      "force": "should",
      "text": "Prespecify the experiment hypothesis, population/allocation, outcome/denominator, guardrails, analysis, justified sample/effect/duration and stopping rule. Check data quality and uncertainty before a decision. Low traffic may require qualitative work or an inconclusive result; do not invent uplift or declare a winner from clicks, peeking or unsupported sample assumptions.",
      "source": "pb-conversion-measurement-and-experiments",
      "covers": ["experiment-validity"],
      "activate_when": ["archetype:marketing-experiment"],
      "phase": ["planning", "implementation", "verification"],
      "priority": 85
    }
  ]
}
```
