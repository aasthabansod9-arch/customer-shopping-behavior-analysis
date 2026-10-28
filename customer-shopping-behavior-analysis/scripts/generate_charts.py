"""Generate summary charts used in the README (saved to images/)."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "images"
IMG.mkdir(exist_ok=True)
df = pd.read_csv(ROOT / "data" / "processed" / "customer_shopping_behavior_clean.csv")

PINK, BLUE, PURPLE = "#E066B5", "#1B2A9F", "#7B2D8E"
plt.rcParams.update({"axes.spines.top": False, "axes.spines.right": False, "font.size": 11})


def save(fig, name):
    fig.tight_layout()
    fig.savefig(IMG / name, dpi=150)
    plt.close(fig)


# 1. Revenue by category
s = df.groupby("category")["purchase_amount"].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(s.index, s.values, color=BLUE)
ax.set_title("Revenue by Category"); ax.set_ylabel("Revenue (USD)")
for i, v in enumerate(s.values): ax.text(i, v, f"{v/1000:.0f}K", ha="center", va="bottom")
save(fig, "revenue_by_category.png")

# 2. Subscription split
s = df["subscription_status"].value_counts()
fig, ax = plt.subplots(figsize=(4.5, 4.5))
ax.pie(s.values, labels=[f"Subscribed: {k}" for k in s.index], autopct="%1.0f%%",
       colors=[PINK, BLUE], wedgeprops={"width": 0.45}, startangle=90)
ax.set_title("Customers by Subscription Status")
save(fig, "subscription_split.png")

# 3. Revenue by age group
order = ["Young Adult", "Middle-aged", "Adult", "Senior"]
s = df.groupby("age_group")["purchase_amount"].sum().reindex(order)
fig, ax = plt.subplots(figsize=(6, 4))
ax.barh(s.index[::-1], s.values[::-1], color=BLUE)
ax.set_title("Revenue by Age Group"); ax.set_xlabel("Revenue (USD)")
save(fig, "revenue_by_age_group.png")

# 4. Customer segments
seg = pd.cut(df["previous_purchases"], [0, 1, 10, 10**6], labels=["New", "Returning", "Loyal"])
s = seg.value_counts().reindex(["New", "Returning", "Loyal"])
fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(s.index, s.values, color=[PINK, PURPLE, BLUE])
ax.set_title("Customer Segments"); ax.set_ylabel("Customers")
for i, v in enumerate(s.values): ax.text(i, v, f"{v:,}", ha="center", va="bottom")
save(fig, "customer_segments.png")

# 5. Discount rate by product (top 5)
s = (df.assign(d=df["discount_applied"].eq("Yes")).groupby("item_purchased")["d"].mean() * 100).nlargest(5)
fig, ax = plt.subplots(figsize=(6, 4))
ax.barh(s.index[::-1], s.values[::-1], color=PURPLE)
ax.set_title("Top 5 Products by Discount Rate"); ax.set_xlabel("% of purchases discounted")
save(fig, "top_discounted_products.png")
print("charts saved:", sorted(p.name for p in IMG.glob("*.png")))
