"""Synthetic multi-city retail transactions (replace with your own sales CSV)."""
import numpy as np
import pandas as pd

CATALOG = {
    "Electronics": [("Smartphone", 18000), ("Laptop", 52000), ("Earbuds", 2500), ("Smartwatch", 6000)],
    "Fashion": [("Kurta", 1200), ("Jeans", 1800), ("Sneakers", 3200), ("Saree", 2800)],
    "Home & Kitchen": [("Mixer Grinder", 3500), ("Cookware Set", 2600), ("Air Fryer", 6500)],
    "Grocery": [("Basmati Rice 5kg", 650), ("Cold-pressed Oil", 420), ("Dry Fruits Pack", 900)],
    "Beauty": [("Skincare Kit", 1500), ("Perfume", 2200), ("Hair Dryer", 1900)],
}
CITIES = {"Bengaluru": "South", "Chennai": "South", "Madurai": "South", "Hyderabad": "South",
          "Mumbai": "West", "Pune": "West", "Delhi": "North", "Jaipur": "North", "Kolkata": "East"}
MARGIN = {"Electronics": .12, "Fashion": .35, "Home & Kitchen": .22, "Grocery": .10, "Beauty": .40}


def make_sales(n=40000, seed=11) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    days = pd.date_range("2024-01-01", "2025-12-31", freq="D")
    # seasonality: festive peak in Oct-Nov, growth over time, weekend lift
    w = 1 + 0.6 * np.isin(days.month, [10, 11]) + 0.25 * (days.month == 12) + np.linspace(0, .45, len(days)) \
        + 0.2 * (days.dayofweek >= 5)
    dates = rng.choice(days, n, p=w / w.sum())
    cats = rng.choice(list(CATALOG), n, p=[.22, .28, .18, .20, .12])
    prods, prices = [], []
    for c in cats:
        name, price = CATALOG[c][rng.integers(len(CATALOG[c]))]
        prods.append(name)
        prices.append(price * rng.uniform(.9, 1.1))
    qty = rng.choice([1, 1, 1, 2, 2, 3, 4], n)
    discount = rng.choice([0, 0, .05, .1, .15, .2], n)
    city = rng.choice(list(CITIES), n, p=[.2, .14, .06, .12, .14, .07, .14, .06, .07])
    df = pd.DataFrame({
        "date": pd.to_datetime(dates), "city": city, "region": [CITIES[c] for c in city],
        "category": cats, "product": prods, "channel": rng.choice(["Online", "Store", "App"], n, p=[.42, .35, .23]),
        "qty": qty, "unit_price": np.round(prices, 0), "discount": discount,
        "hour": rng.choice(range(9, 23), n),
    })
    df["revenue"] = (df.qty * df.unit_price * (1 - df.discount)).round(0)
    df["profit"] = (df.revenue * (df.category.map(MARGIN) - df.discount * .5)).round(0)
    return df.sort_values("date").reset_index(drop=True)
