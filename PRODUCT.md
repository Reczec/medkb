# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

- **Doctors (Arzt/Ärztin)**, especially new ones, who look up symptoms, diagnoses and guidelines in professional language, with ICD codes, current studies and drug data. Read-only.
- **Patients** who want a topic explained in plain language and to know when to see a doctor. Read-only, never shown internal data such as classifier scores.
- **Admins** who maintain the knowledge base: create, edit, classify, archive, review the change log.
- **Evaluators of the demo** (recruiters, hiring managers) who open the public live link from a CV and judge craft within a minute. When goals conflict, the product must first be a credible clinical tool; the impression on evaluators comes from it looking and behaving like a real one.

## Product Purpose

MedKB is a digital medical knowledge base: structured entries, keyword search, transparent rule-based classification into medical specialties, JSON archiving with restore, and an audit log. Version 2 adds roles, AI explanations and summaries, and live data from official sources. It exists as a portfolio and CV project and re-implements the author's chapter of a diploma thesis (TGM Wien, 2026). Success: a visitor can pick a demo role and immediately sees a modern, trustworthy, working tool.

## Positioning

An explainable knowledge base: every automatic category comes with its scores and matched terms; AI answers cite the stored entries; external facts come from named official sources (PubMed, WHO ICD-11, openFDA). The rule-based classifier from the thesis stays visible next to the AI ("Regeln vs. KI").

## Operating Context

Public demo hosted on a free tier (cold starts possible). Demo logins per role, no registration. Database resets to the seed state regularly. UI in German, code and API in English.

## Capabilities and Constraints

- Backend FastAPI + SQLAlchemy (SQLite or PostgreSQL); frontend React + TypeScript + Tailwind + shadcn/ui + motion.
- Roles: admin, doctor, patient (from stage 2 of the v2 spec).
- AI through a free, swappable OpenAI-compatible provider; results cached; rate-limited.
- Spec: `docs/superpowers/specs/2026-10-10-medkb-v2-design.md`.

## Brand Commitments

Name "MedKB". Every view carries the notice "Prototyp mit Beispieldaten – keine medizinische Beratung."

## Evidence on Hand

Content is editorial demo content at textbook level, no patient data. There are no real users, customers, testimonials or usage numbers; do not invent any.

## Product Principles

1. Credible before flashy: behave like a real clinical tool; motion supports orientation, never decoration for its own sake.
2. Explainable: show why (scores, matched terms, sources) wherever the system decides something.
3. Safe by default: no individual diagnoses, clear disclaimers, emergency hints where relevant.
4. Role-appropriate: the same knowledge, told in professional language for doctors and plain language for patients.

## Accessibility & Inclusion

German UI; plain-language mode for patients. Keyboard-operable components, visible focus, `prefers-reduced-motion` respected, WCAG AA contrast in light and dark themes.
