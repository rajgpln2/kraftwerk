# Will the Customer Accept the Coupon?

This project explores a marketing question: **which drivers are most likely to accept a mobile coupon offered while they are driving?

Using the `coupons.csv` dataset, I compared customers who **accepted** the coupon to those who **did not**, and looked for patterns that a business team could act on.

---

## Dataset and Approach

- **Rows (drivers/trips):** 12,684  
- **Target column (`Y`):**
  - `1` = customer accepted the coupon  
  - `0` = customer did not accept the coupon
- **Overall results:**
  - **7,210 drivers (56.8%) accepted** a coupon  
  - **5,474 drivers (43.2%) did not**

**Tools:** Python, pandas, Matplotlib, and Seaborn in a Jupyter Notebook.

I calculated summary statistics and built simple visualizations (bar charts, histograms) to compare groups and highlight differences between those who accepted and rejected the coupons.

---

## How Acceptance Varies by Coupon Type

Acceptance is not uniform; some coupon types perform much better than others:

- **Carry out & Take away:** ~**73.5%** acceptance (2,393 offers)  
- **Inexpensive restaurant (Restaurant \< \$20):** ~**70.7%** (2,786 offers)  
- **Coffee House:** ~**49.9%** (3,996 offers)  
- **Restaurant \$20–\$50:** ~**44.1%** (1,492 offers)  
- **Bar:** ~**41.0%** (2,017 offers)

**Takeaway:** Quick, low-commitment food offers (take-out and inexpensive restaurants) are by far the most successful. Bar and higher-priced restaurant coupons are noticeably harder to convert.

---

## Who Is Most Likely to Accept?

### Companions (Who They’re With)

Acceptance varies strongly by who is in the car:

- Driving with **Friend(s):** **67.3%** acceptance  
- With a **Partner:** **59.5%**  
- **Alone:** **52.6%**  
- With **Kid(s):** **50.5%**

**Insight:** Social outings with friends are the most coupon-friendly context. Drivers with kids or alone are more cautious and less likely to redeem.

---

### Destination (Where They’re Going)

- **No Urgent Place:** **63.4%** acceptance  
- **Home:** **50.6%**  
- **Work:** **50.2%**

**Insight:** When drivers have **no urgent destination**, they are much more open to spontaneous stops driven by coupons. Commuters and people heading home are less responsive.

---

### Age and Demographics

- **Younger drivers accept more often.**  
  - **Below 21:** **63.4%**  
  - **Age 21–26:** about **59–60%**  
  - **50+ years:** drops to **50.9%**

- **Gender:**  
  - **Male:** **59.1%** acceptance  
  - **Female:** **54.7%**

- **Income:**  
  Acceptance is highest for **moderate and lower incomes** (roughly \$25K–\$62K and less than \$12.5K) at around **59–60%**, and lowest for the **\$75K–\$87.5K** group at **48.3%**.

**Insight:** Younger, mid-income drivers are the most responsive segment. Higher income and older drivers tend to ignore offers more often.

---

### Going-Out Habits (Bars and Inexpensive Restaurants)

How often people go out strongly relates to their behavior with coupons:

**Bar visits**

- Bar **4–8 times/month:** **63.8%** acceptance  
- Bar **1–3 times/month:** **62.2%**  
- Bar **never:** **53.2%**

**Inexpensive restaurant visits (Restaurant \< \$20)**

- **More than 8 times/month:** **60.8%**  
- **4–8 times/month:** **58.5%**  
- **1–3 times/month:** **56.0%**  
- **Rarely or never:** ~**53–54%**

**Insight:** Customers who **already go out frequently** are significantly more likely to redeem related coupons. Coupon campaigns are especially effective at nudging “regulars,” not at creating entirely new habits.

---

### Weather and Timing

- **Sunny days:** **59.5%** acceptance  
- **Rainy:** **46.3%**  
- **Snowy:** **47.0%**

**Insight:** Weather matters. People are far more willing to change plans for a coupon when conditions are pleasant.

---

## Nontechnical Summary of Differences

Compared with those who reject coupons, **customers who accept coupons are more likely to:**

1. Be **younger** (under 30) and of **moderate income**.  
2. Be on a **leisure trip** with **no urgent destination**, especially with **friends**.  
3. **Frequently visit** bars or inexpensive restaurants already.  
4. Receive **quick, low-cost food offers** (take-out or cheap restaurants) rather than more expensive or alcohol-focused offers.  
5. Be driving in **good weather**, when a spontaneous stop feels convenient.

Those who **do not** accept coupons are more likely to be:

- Older and higher-income drivers,  
- Commuters or drivers heading straight home,  
- People who go out less frequently, or  
- Drivers in poor weather conditions where changing plans is inconvenient.

---

## Practical Recommendations

1. **Target frequent visitors and social outings.**  
   Focus bar and restaurant coupons on customers who regularly go out and are traveling with friends or partners. They show **60–67%** acceptance rates.

2. **Prioritize low-cost, low-friction offers.**  
   Emphasize “quick bite” or “take-out” coupons (which achieve **70–74%** acceptance) over higher-price dining when trying to maximize redemptions.

3. **Use trip context and weather when available.**  
   Trigger campaigns during leisure trips and on sunny days, especially when the destination is flexible (“No Urgent Place”).

4. **Segment by life stage and income.**  
   Create more conservative, value-focused messaging for older and higher-income drivers, who are less immediately responsive to generic offers.

---

## Repository Contents

- `Practical_Application1.ipynb` – main analysis notebook  
- `coupons.csv` – dataset used in the analysis  
- `README.md` – this nontechnical summary of findings

