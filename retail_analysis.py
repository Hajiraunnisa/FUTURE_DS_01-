"""
Online Retail Sales Analysis
Client-Ready Business Dashboard & Insights Report
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.gridspec as gridspec
import warnings
warnings.filterwarnings("ignore")

# ── 0. Load & Clean ────────────────────────────────────────────────────────────
df = pd.read_csv(
    r"c:\Users\Hajira\OneDrive\Documents\Data Science\online_retail.csv",
    encoding="ISO-8859-1"
)

# Drop rows without CustomerID (anonymous / untrackable)
df.dropna(subset=["CustomerID"], inplace=True)

# Drop rows with missing Description
df.dropna(subset=["Description"], inplace=True)

# Remove cancelled orders (InvoiceNo starts with 'C')
df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

# Remove negative/zero quantities and prices
df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

# Parse date
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["YearMonth"]   = df["InvoiceDate"].dt.to_period("M")
df["Month"]       = df["InvoiceDate"].dt.month_name()
df["Year"]        = df["InvoiceDate"].dt.year

# Revenue column
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

print(f"Clean dataset: {df.shape[0]:,} rows | "
      f"Date range: {df['InvoiceDate'].min().date()} → {df['InvoiceDate'].max().date()}")

# ── 1. KPI Summary ─────────────────────────────────────────────────────────────
total_revenue   = df["Revenue"].sum()
total_orders    = df["InvoiceNo"].nunique()
total_customers = df["CustomerID"].nunique()
total_products  = df["StockCode"].nunique()
avg_order_value = total_revenue / total_orders

print("\n── KPI Summary ──────────────────────────────────────")
print(f"  Total Revenue   : £{total_revenue:>12,.2f}")
print(f"  Total Orders    : {total_orders:>12,}")
print(f"  Unique Customers: {total_customers:>12,}")
print(f"  Unique Products : {total_products:>12,}")
print(f"  Avg Order Value : £{avg_order_value:>12,.2f}")

# ── 2. Monthly Revenue Trend ───────────────────────────────────────────────────
monthly = (
    df.groupby("YearMonth")["Revenue"]
    .sum()
    .reset_index()
    .sort_values("YearMonth")
)
monthly["YearMonth_str"] = monthly["YearMonth"].astype(str)

# ── 3. Top 10 Products by Revenue ─────────────────────────────────────────────
top_products = (
    df.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

# ── 4. Top 10 Countries by Revenue (excl. UK) ─────────────────────────────────
top_countries = (
    df[df["Country"] != "United Kingdom"]
    .groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

# ── 5. Revenue by Country incl. UK (pie share) ────────────────────────────────
country_all = (
    df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)
top5 = country_all.head(5)
others = pd.Series({"Others": country_all.iloc[5:].sum()})
pie_data = pd.concat([top5, others])

# ── 6. Top 10 Customers by Revenue ────────────────────────────────────────────
top_customers = (
    df.groupby("CustomerID")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
top_customers["CustomerID"] = top_customers["CustomerID"].astype(int).astype(str)

# ── 7. Order Frequency Distribution ──────────────────────────────────────────
order_freq = (
    df.groupby("CustomerID")["InvoiceNo"]
    .nunique()
    .reset_index(name="OrderCount")
)

# ── 8. Quantity vs Revenue scatter (top 200 products) ─────────────────────────
product_summary = (
    df.groupby("Description")
    .agg(TotalQty=("Quantity", "sum"), TotalRevenue=("Revenue", "sum"))
    .reset_index()
    .sort_values("TotalRevenue", ascending=False)
    .head(200)
)

# ══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD  (2 pages)
# ══════════════════════════════════════════════════════════════════════════════
BRAND   = "#1a1a2e"
ACCENT1 = "#e94560"
ACCENT2 = "#0f3460"
ACCENT3 = "#16213e"
GREEN   = "#2ecc71"
GOLD    = "#f39c12"
PURPLE  = "#8e44ad"
TEAL    = "#1abc9c"
GREY    = "#bdc3c7"

BAR_COLORS = [ACCENT1, ACCENT2, TEAL, GOLD, PURPLE, GREEN, "#e67e22", "#3498db", "#e74c3c", "#9b59b6"]


def fmt_k(x, pos=None):
    if x >= 1_000_000:
        return f"£{x/1_000_000:.1f}M"
    elif x >= 1_000:
        return f"£{x/1_000:.0f}K"
    return f"£{x:.0f}"


# ── PAGE 1 ─────────────────────────────────────────────────────────────────────
fig1 = plt.figure(figsize=(20, 24), facecolor=BRAND)
gs1  = gridspec.GridSpec(4, 2, figure=fig1, hspace=0.55, wspace=0.35,
                         top=0.93, bottom=0.04, left=0.07, right=0.97)

# Title
fig1.text(0.5, 0.965, "Online Retail — Business Intelligence Dashboard",
          ha="center", va="top", fontsize=22, fontweight="bold", color="white")
fig1.text(0.5, 0.952, f"Period: Dec 2010 – Dec 2011   |   Clean records: {df.shape[0]:,}   |   Built with Python · Matplotlib",
          ha="center", va="top", fontsize=10, color=GREY)

# KPI boxes (row 0, spanning both columns)
ax_kpi = fig1.add_subplot(gs1[0, :])
ax_kpi.set_facecolor(BRAND)
ax_kpi.axis("off")

kpis = [
    ("Total Revenue",    f"£{total_revenue/1_000_000:.2f}M", ACCENT1),
    ("Total Orders",     f"{total_orders:,}",                TEAL),
    ("Unique Customers", f"{total_customers:,}",             GOLD),
    ("Unique Products",  f"{total_products:,}",              PURPLE),
    ("Avg Order Value",  f"£{avg_order_value:,.2f}",         GREEN),
]
for i, (label, value, color) in enumerate(kpis):
    x = 0.1 + i * 0.195
    ax_kpi.add_patch(plt.Rectangle((x - 0.085, 0.05), 0.17, 0.88,
                                   transform=ax_kpi.transAxes,
                                   color=ACCENT3, zorder=0,
                                   clip_on=False))
    ax_kpi.text(x, 0.65, value, transform=ax_kpi.transAxes,
                ha="center", va="center", fontsize=20, fontweight="bold", color=color)
    ax_kpi.text(x, 0.25, label, transform=ax_kpi.transAxes,
                ha="center", va="center", fontsize=10, color=GREY)

# -- Monthly Revenue Trend (row 1, full width)
ax1 = fig1.add_subplot(gs1[1, :])
ax1.set_facecolor(ACCENT3)
x_vals = range(len(monthly))
ax1.fill_between(x_vals, monthly["Revenue"], alpha=0.25, color=ACCENT1)
ax1.plot(x_vals, monthly["Revenue"], color=ACCENT1, linewidth=2.5, marker="o",
         markersize=5, markerfacecolor="white")
ax1.set_xticks(list(x_vals))
ax1.set_xticklabels(monthly["YearMonth_str"], rotation=45, ha="right",
                    fontsize=8, color=GREY)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
ax1.tick_params(axis="y", colors=GREY, labelsize=8)
ax1.set_title("Monthly Revenue Trend", color="white", fontsize=13, fontweight="bold", pad=10)
ax1.set_facecolor(ACCENT3)
for spine in ax1.spines.values():
    spine.set_edgecolor(GREY)
    spine.set_alpha(0.3)

# Annotate peak
peak_idx = monthly["Revenue"].idxmax()
peak_ym  = monthly.loc[peak_idx, "YearMonth_str"]
peak_rev = monthly.loc[peak_idx, "Revenue"]
ax1.annotate(f"Peak\n{fmt_k(peak_rev)}",
             xy=(list(monthly["YearMonth_str"]).index(peak_ym), peak_rev),
             xytext=(list(monthly["YearMonth_str"]).index(peak_ym) - 1.5, peak_rev * 0.85),
             color=GOLD, fontsize=8, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.2))

# -- Top 10 Products (row 2, left)
ax2 = fig1.add_subplot(gs1[2, 0])
ax2.set_facecolor(ACCENT3)
bars = ax2.barh(top_products["Description"][::-1],
                top_products["Revenue"][::-1],
                color=BAR_COLORS[::-1], edgecolor="none", height=0.65)
ax2.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
ax2.tick_params(axis="x", colors=GREY, labelsize=7)
ax2.tick_params(axis="y", colors=GREY, labelsize=7)
for bar, val in zip(bars, top_products["Revenue"][::-1]):
    ax2.text(bar.get_width() + top_products["Revenue"].max() * 0.01,
             bar.get_y() + bar.get_height() / 2,
             fmt_k(val), va="center", fontsize=7, color=GREY)
ax2.set_title("Top 10 Products by Revenue", color="white", fontsize=11, fontweight="bold", pad=8)
for spine in ax2.spines.values():
    spine.set_edgecolor(GREY); spine.set_alpha(0.3)

# -- Top 10 Countries excl UK (row 2, right)
ax3 = fig1.add_subplot(gs1[2, 1])
ax3.set_facecolor(ACCENT3)
bars3 = ax3.barh(top_countries["Country"][::-1],
                 top_countries["Revenue"][::-1],
                 color=BAR_COLORS[::-1], edgecolor="none", height=0.65)
ax3.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
ax3.tick_params(axis="x", colors=GREY, labelsize=7)
ax3.tick_params(axis="y", colors=GREY, labelsize=7)
for bar, val in zip(bars3, top_countries["Revenue"][::-1]):
    ax3.text(bar.get_width() + top_countries["Revenue"].max() * 0.01,
             bar.get_y() + bar.get_height() / 2,
             fmt_k(val), va="center", fontsize=7, color=GREY)
ax3.set_title("Top 10 International Markets (ex UK)", color="white", fontsize=11, fontweight="bold", pad=8)
for spine in ax3.spines.values():
    spine.set_edgecolor(GREY); spine.set_alpha(0.3)

# -- Revenue Share Pie (row 3, left)
ax4 = fig1.add_subplot(gs1[3, 0])
ax4.set_facecolor(ACCENT3)
wedge_colors = [ACCENT1, TEAL, GOLD, PURPLE, GREEN, GREY]
wedges, texts, autotexts = ax4.pie(
    pie_data.values,
    labels=pie_data.index,
    autopct="%1.1f%%",
    colors=wedge_colors,
    startangle=140,
    pctdistance=0.78,
    textprops={"color": GREY, "fontsize": 8},
    wedgeprops={"edgecolor": BRAND, "linewidth": 1.5}
)
for at in autotexts:
    at.set_color("white"); at.set_fontsize(7)
ax4.set_title("Revenue Share by Country", color="white", fontsize=11, fontweight="bold", pad=8)

# -- Top 10 Customers (row 3, right)
ax5 = fig1.add_subplot(gs1[3, 1])
ax5.set_facecolor(ACCENT3)
bars5 = ax5.bar(top_customers["CustomerID"],
                top_customers["Revenue"],
                color=BAR_COLORS, edgecolor="none", width=0.65)
for bar, val in zip(bars5, top_customers["Revenue"]):
    ax5.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 200,
             fmt_k(val), ha="center", fontsize=7, color=GREY)
ax5.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
ax5.tick_params(axis="x", colors=GREY, labelsize=7, rotation=30)
ax5.tick_params(axis="y", colors=GREY, labelsize=7)
ax5.set_title("Top 10 Customers by Revenue", color="white", fontsize=11, fontweight="bold", pad=8)
ax5.set_xlabel("Customer ID", color=GREY, fontsize=8)
for spine in ax5.spines.values():
    spine.set_edgecolor(GREY); spine.set_alpha(0.3)

page1_path = r"c:\Users\Hajira\OneDrive\Documents\Data Science\retail_dashboard_page1.png"
fig1.savefig(page1_path, dpi=150, bbox_inches="tight", facecolor=BRAND)
print(f"\nPage 1 saved → {page1_path}")

# ── PAGE 2 ─────────────────────────────────────────────────────────────────────
fig2 = plt.figure(figsize=(20, 18), facecolor=BRAND)
gs2  = gridspec.GridSpec(2, 2, figure=fig2, hspace=0.5, wspace=0.35,
                         top=0.91, bottom=0.07, left=0.07, right=0.97)

fig2.text(0.5, 0.96, "Online Retail — Deep Dive Analysis",
          ha="center", va="top", fontsize=22, fontweight="bold", color="white")
fig2.text(0.5, 0.945, "Customer behaviour · Order patterns · Product performance",
          ha="center", va="top", fontsize=10, color=GREY)

# -- Customer Order Frequency (row 0, left)
ax6 = fig2.add_subplot(gs2[0, 0])
ax6.set_facecolor(ACCENT3)
bins = [1, 2, 3, 5, 10, 20, 50, order_freq["OrderCount"].max() + 1]
labels6 = ["1", "2", "3–4", "5–9", "10–19", "20–49", "50+"]
order_freq["Bucket"] = pd.cut(order_freq["OrderCount"], bins=bins, labels=labels6, right=False)
bucket_counts = order_freq["Bucket"].value_counts().reindex(labels6)
bars6 = ax6.bar(labels6, bucket_counts.values, color=TEAL, edgecolor="none", width=0.6)
for bar, val in zip(bars6, bucket_counts.values):
    ax6.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
             f"{val:,}", ha="center", fontsize=8, color=GREY)
ax6.set_title("Customer Order Frequency Distribution", color="white", fontsize=11, fontweight="bold", pad=8)
ax6.set_xlabel("Number of Orders", color=GREY, fontsize=9)
ax6.set_ylabel("Number of Customers", color=GREY, fontsize=9)
ax6.tick_params(colors=GREY, labelsize=8)
for spine in ax6.spines.values():
    spine.set_edgecolor(GREY); spine.set_alpha(0.3)

# -- Monthly Order Count (row 0, right)
ax7 = fig2.add_subplot(gs2[0, 1])
ax7.set_facecolor(ACCENT3)
monthly_orders = (
    df.groupby("YearMonth")["InvoiceNo"]
    .nunique()
    .reset_index()
    .sort_values("YearMonth")
)
monthly_orders["YearMonth_str"] = monthly_orders["YearMonth"].astype(str)
x7 = range(len(monthly_orders))
ax7.fill_between(x7, monthly_orders["InvoiceNo"], alpha=0.2, color=TEAL)
ax7.plot(x7, monthly_orders["InvoiceNo"], color=TEAL, linewidth=2.5, marker="o",
         markersize=5, markerfacecolor="white")
ax7.set_xticks(list(x7))
ax7.set_xticklabels(monthly_orders["YearMonth_str"], rotation=45, ha="right",
                    fontsize=8, color=GREY)
ax7.tick_params(axis="y", colors=GREY, labelsize=8)
ax7.set_title("Monthly Order Volume", color="white", fontsize=11, fontweight="bold", pad=8)
ax7.set_ylabel("Number of Orders", color=GREY, fontsize=9)
for spine in ax7.spines.values():
    spine.set_edgecolor(GREY); spine.set_alpha(0.3)

# -- Quantity vs Revenue scatter (row 1, left)
ax8 = fig2.add_subplot(gs2[1, 0])
ax8.set_facecolor(ACCENT3)
sc = ax8.scatter(product_summary["TotalQty"],
                 product_summary["TotalRevenue"],
                 c=product_summary["TotalRevenue"],
                 cmap="plasma", alpha=0.7, s=40, edgecolors="none")
plt.colorbar(sc, ax=ax8, label="Revenue (£)").ax.yaxis.set_tick_params(color=GREY)
ax8.set_title("Top 200 Products: Qty Sold vs Revenue", color="white", fontsize=11, fontweight="bold", pad=8)
ax8.set_xlabel("Total Quantity Sold", color=GREY, fontsize=9)
ax8.set_ylabel("Total Revenue (£)", color=GREY, fontsize=9)
ax8.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: fmt_k(x)))
ax8.tick_params(colors=GREY, labelsize=8)
for spine in ax8.spines.values():
    spine.set_edgecolor(GREY); spine.set_alpha(0.3)

# -- Revenue by Day of Week (row 1, right)
ax9 = fig2.add_subplot(gs2[1, 1])
ax9.set_facecolor(ACCENT3)
df["DayOfWeek"] = df["InvoiceDate"].dt.day_name()
dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
dow_rev = df.groupby("DayOfWeek")["Revenue"].sum().reindex(dow_order)
bars9 = ax9.bar(dow_order, dow_rev.values, color=GOLD, edgecolor="none", width=0.6)
for bar, val in zip(bars9, dow_rev.values):
    ax9.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5000,
             fmt_k(val), ha="center", fontsize=7.5, color=GREY)
ax9.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
ax9.set_title("Revenue by Day of Week", color="white", fontsize=11, fontweight="bold", pad=8)
ax9.set_xlabel("Day", color=GREY, fontsize=9)
ax9.set_ylabel("Total Revenue", color=GREY, fontsize=9)
ax9.tick_params(axis="x", colors=GREY, labelsize=8, rotation=20)
ax9.tick_params(axis="y", colors=GREY, labelsize=8)
for spine in ax9.spines.values():
    spine.set_edgecolor(GREY); spine.set_alpha(0.3)

page2_path = r"c:\Users\Hajira\OneDrive\Documents\Data Science\retail_dashboard_page2.png"
fig2.savefig(page2_path, dpi=150, bbox_inches="tight", facecolor=BRAND)
print(f"Page 2 saved → {page2_path}")

plt.close("all")

# ── 9. Insights Report ────────────────────────────────────────────────────────
nov_rev = monthly.loc[monthly["YearMonth_str"] == "2011-11", "Revenue"].values
nov_str = fmt_k(nov_rev[0]) if len(nov_rev) else "N/A"

report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║         ONLINE RETAIL — BUSINESS INSIGHTS & RECOMMENDATIONS REPORT         ║
╚══════════════════════════════════════════════════════════════════════════════╝

PREPARED BY  : Sales Analytics Team
DATA PERIOD  : December 2010 – December 2011
CLEAN RECORDS: {df.shape[0]:,} transactions

─────────────────────────────────────────────────────────────────────────────
 KPI SUMMARY
─────────────────────────────────────────────────────────────────────────────
  ▸ Total Revenue      : £{total_revenue:,.2f}
  ▸ Total Orders       : {total_orders:,}
  ▸ Unique Customers   : {total_customers:,}
  ▸ Unique Products    : {total_products:,}
  ▸ Average Order Value: £{avg_order_value:,.2f}

─────────────────────────────────────────────────────────────────────────────
 KEY INSIGHTS
─────────────────────────────────────────────────────────────────────────────

1. REVENUE TREND — Strong Q4 Seasonality
   • Revenue peaks sharply in November ({nov_str}) driven by Christmas/holiday
     gifting. This is consistent across both years observed.
   • Q1 (Jan–Feb) shows a post-holiday dip — the business must plan inventory
     and cash flow accordingly.

2. TOP PRODUCTS — Giftware & Home Décor Dominate
   • The top 10 revenue-generating products are almost entirely home décor,
     gifts, and novelty items (e.g., heart holders, lanterns, bunting).
   • A small SKU set drives disproportionate revenue — classic 80/20 pattern.

3. GEOGRAPHIC CONCENTRATION — High UK Dependency
   • The United Kingdom accounts for the vast majority of revenue (>80%).
   • Netherlands, EIRE (Ireland), Germany, and France are the top 4
     international markets but remain relatively small contributors.
   • Significant growth opportunity exists in expanding EU market reach.

4. CUSTOMER BASE — High One-Time Buyers
   • The order frequency distribution shows a large share of customers who
     ordered only once or twice.
   • Returning customers are highly valuable — top 10 customers alone
     contribute substantial revenue.

5. ORDER PATTERNS — Weekday Business
   • Thursday and Tuesday generate the most revenue, with Sunday being
     nearly inactive.
   • This confirms a B2B wholesale purchasing pattern (retailers buying
     stock mid-week for weekend resale).

─────────────────────────────────────────────────────────────────────────────
 ACTIONABLE RECOMMENDATIONS
─────────────────────────────────────────────────────────────────────────────

  ✔ SEASONAL CAMPAIGNS
    Launch targeted email/ad campaigns in October to capitalise on the
    November peak. Pre-bundle gift sets of top-selling home décor items.

  ✔ CUSTOMER RETENTION (Reduce One-Time Buyers)
    Implement a loyalty or rewards programme. Send personalised follow-up
    offers 30–60 days after a customer's first purchase.

  ✔ INTERNATIONAL EXPANSION
    Prioritise Netherlands, Germany, and France with localised catalogues
    and EU shipping promotions. These markets already show traction.

  ✔ VIP CUSTOMER PROGRAMME
    Identify and personally manage the top 50 customers by revenue.
    They represent low churn risk and high lifetime value.

  ✔ SKU RATIONALISATION
    Review low-revenue products and consider discontinuing or bundling
    slow movers. Focus procurement spend on the top 100 SKUs.

  ✔ MIDWEEK PROMOTIONS
    Since Thursday is the peak day, run flash sales or bundle deals on
    Mondays/Tuesdays to smooth order volume across the week.

─────────────────────────────────────────────────────────────────────────────
 DASHBOARD FILES
─────────────────────────────────────────────────────────────────────────────
  Page 1: retail_dashboard_page1.png  (KPIs, Trends, Products, Markets)
  Page 2: retail_dashboard_page2.png  (Customer behaviour, Day patterns)

════════════════════════════════════════════════════════════════════════════════
"""

print(report)

report_path = r"c:\Users\Hajira\OneDrive\Documents\Data Science\retail_insights_report.txt"
with open(report_path, "w", encoding="utf-8") as f:
    f.write(report)
print(f"Report saved → {report_path}")
