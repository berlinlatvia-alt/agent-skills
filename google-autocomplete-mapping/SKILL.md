---
name: google-autocomplete-mapping
description: Systematic e-commerce keyword demand research by proxying Google Autocomplete suggestion signals. Use when asked to: (1) perform keyword research for Etsy/Amazon/Shopify products, (2) identify product niches, (3) analyze search volumes, (4) verify demand/supply stats for digital or physical products, (5) audit competition levels for e-commerce listings.
---

# Google Autocomplete Mapping & E-Commerce Keyword Research

Systematically extract and prioritize high-demand search keywords on e-commerce platforms (Etsy, Amazon, Shopify) by proxying Google's autocomplete suggestion signals.

## Core Workflows

### 1. Standard Demand Verification

Execute the standard script to map search variations and discover related long-tail phrases:

```bash
python scripts/verify_etsy_demand.py "[Seed Keyword]"
```

This performs a query sweep on multiple intent-modified variants (e.g., `etsy [seed]`, `[seed] spreadsheet etsy`, etc.) and outputs direct links to Google Trends and Etsy.

### 2. Stealth Supply Scraping (Bypassing DataDome)

Etsy protects its catalog pages using DataDome bot detection (HTTP 403 blocks). To programmatically measure competitor listing counts (supply):

1. Log into Etsy on Chrome or Brave browser.
2. Export browser cookies as a JSON file using a cookie exporter extension.
3. Save the JSON file to `C:\Users\smmgo\Documents\Hermes-Agent\etsy_cookies.json`.
4. Run the stealth script:

```bash
python scripts/verify_etsy_demand_stealth.py "[Seed Keyword]" --cookies "etsy_cookies.json"
```

Use `--limit` to control the number of keywords audited (lower limits protect cookie life).

## Metrics Interpretation

- **Demand Score (Autocomplete Index):** Derived from how early and frequently a term appears in search suggestions (Max 50 pts). Higher = stronger user search interest.
- **Supply Count (Listing Count):**
  - `< 1,000` = Ultra-low competition (instant organic rank potential).
  - `1,000 - 10,000` = Low competition (highly targetable).
  - `10,000 - 50,000` = Medium competition (requires strong differentiation).
  - `> 50,000` = High competition (saturated, requires ad spend).
- **Opportunity Ratio:** Calculated as `(Demand Score / Supply Count) * 1000`. Keywords with ratio `> 1.0` are target niches.
- **Ad Density & Pricing Floor Correlation:**
  - **Low Ads + Low Price ($1-$3):** Saturated commodity trap. Sellers rely on high organic volume because margins cannot sustain CPC bidding. Avoid.
  - **Low Ads + High Price ($15+):** Premium Goldmine. High ticket value with zero advertising competition.
  - **High Ads + High Price ($15+):** Validated commercial market. Highly profitable but entry requires high-quality differentiation.

## Scripts

- `scripts/verify_etsy_demand.py` - Google Autocomplete query sweep against intent-modified keyword variants; outputs ranked demand scores with Trends + Etsy deep links.
- `scripts/verify_etsy_demand_stealth.py` - Same demand sweep plus live Etsy supply-count scraping via exported browser cookies to bypass DataDome.
