# Suggested event taxonomy — not implemented in Lagos Life

This is a conceptual future internal analytics design only. It requires Vatar authorisation and privacy review. Do not collect emails, chat contents, payment references, device identifiers, real-world location, or sensitive profile information.

| Event | Trigger | Minimal properties | Purpose |
|---|---|---|---|
| session_started | Confirmed session | pseudonymous_id; timestamp UTC; platform | DAU and retention cohorts |
| onboarding_milestone_completed | First task completed | pseudonymous_id; milestone category; timestamp | Onboarding friction |
| job_task_completed | Job workflow completed | pseudonymous_id; job category; timestamp | Job-system engagement |
| property_action_completed | Home/rent workflow completed | pseudonymous_id; action category; timestamp | Housing adoption |
| transport_used | Travel completed | pseudonymous_id; transport category; timestamp | Travel-system adoption |
| currency_earned | Fictional credit awarded | pseudonymous_id; coarse amount bucket; source category | In-game economic inputs |
| currency_spent | Fictional debit recorded | pseudonymous_id; coarse amount bucket; sink category | In-game economic outputs |
| client_error | Sanitised error recorded | error_code; version; timestamp | Performance guardrails |

**D1 retention:** number of signup-day players with a qualifying session on the following local calendar day / total signup-day players eligible for complete observation. **D7:** same at day seven. Exclude cohorts without a full observation window. Define deduplication, cutoff timezone and consent approach in advance. No such data is currently accessed by this repo.
