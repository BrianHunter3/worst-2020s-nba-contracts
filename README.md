# Worst 2020s NBA Contract Analysis: Contract Surplus Yield (CSY)

**Author:** Brian Hunter ([@Vello_Ball](https://github.com/BrianHunter3))  
**Degree:** B.A. in Economics, University of Illinois at Urbana-Champaign  
**Focus:** Basketball Strategy, Econometrics, & Financial Analytics  

---

## Project Overview
Credit to sports creator Lucas Burns (@itslucasburns), who posted an ordered compilation of what he believed to be the sixteen worst NBA free agent contracts of the 2020s, dividing them into "death sentences" vs. "good players who were simply overpaid."

As an economics senior preparing for roles in sports analytics and strategy, I set out to test his thesis empirically: **Can we mathematically evaluate NBA contractual return on investment (ROI) down to the dollar?**

This repository contains the complete empirical pipeline—from raw contract data cleaning and multi-column edge case handling (accounting for dead-money buyouts) to the formulation of a novel sports valuation metric: **Contract Surplus Yield (CSY)**.

---

## The Contract Surplus Yield (CSY) Model

Traditional sports efficiency metrics divide total output by salary, producing a gross benefit-to-cost ratio that can never evaluate negative return. In real financial economics, Net ROI measures percentage return against baseline capital cost.

### 1. Volume-Adjusted Production
Using Player Impact Estimate (PIE), Games Played (GP), and Minutes Per Game (MPG):
Total Impact ROI = (GP x MPG x PIE) / Annual Salary ($M)

### 2. The Net Surplus Metric
Benchmarking against an empirical median starter baseline (70 GP, 30 MPG, 10.0% PIE, $20M Salary ≈ 10.0 baseline output ratio):

CSY (%) = ((Total Impact ROI - 10.0) / 10.0) x 100

### 3. Wasted Cap Space ($M)
Wasted Salary ($M) = Salary ($M) x (-CSY / 100)

---

## Contract Valuation Tiers

| Tier | Name | CSY Range | Characteristics |
| :---: | :--- | :---: | :--- |
| **1** | **Toxic Assets / Dead Money** | < -75% | Buyouts, waived dead cap, and extreme non-availability (-100.0%) |
| **2** | **Inefficient Contracts** | -75% to -40% | Heavy overpays for durability-first starter output |
| **3** | **Below-Average Value** | -40% to -10% | Moderate overpays or age-related athletic decline |
| **4** | **Fair Market Value** | -10% to +15% | Production commensurate with salary cap hit |
| **5** | **Surplus Value** | > +15% | High-bargain starter or All-Star value |

---

## Key Findings

* **The Dead Money Stratosphere:** Bradley Beal’s Phoenix Suns buyout ($2025–26, $96.92M) sits as the single most catastrophic dead-money commitment in modern NBA history ($-100.0% CSY, $96.92M wasted).
* **Validating Burns's "Good Players Overpaid" Claim:** Early contract years for Joe Harris ($2020–21, +13.1% CSY) and Kyle Kuzma ($2023–24, +1.7\%\text{ CSY}$) operated in **Tier 4: Fair Market Value** before injury and roster misalignment degraded their long-term value.
* **The Second Apron Era:** Under the 2023 CBA, negative-CSY deals are no longer just luxury-tax penalties for wealthy owners. They freeze trade flexibility, eliminate Mid-Level Exceptions, and relegate future first-round draft picks.

---
