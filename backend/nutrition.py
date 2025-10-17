# nutrition.py
from __future__ import annotations
import math
import pandas as pd
from cachetools import TTLCache

# 读CSV（程序启动时加载到内存）
class NutritionRepo:
    def __init__(self, mapping_csv: str, addons_csv: str):
        self.mapping = pd.read_csv("data/mapping.csv")
        self.addons = pd.read_csv("data/addons.csv")

        # 列表化关键词
        self.mapping["kw_list"] = self.mapping["keywords"].apply(
            lambda s: [x.strip() for x in str(s).split("|")]
        )

    # ✅ 主食物基础营养查找
    def get_base(self, label: str) -> dict | None:
        # 先直接匹配 label 列
        row = self.mapping[self.mapping["label"] == label]
        if not row.empty:
            return row.iloc[0].to_dict()

        # 如果没匹配到，尝试 keyword 匹配
        for _, r in self.mapping.iterrows():
            if any(label.lower() in kw.lower() for kw in r["kw_list"]):
                return r.to_dict()

        # 都没找到就返回 None
        return None

    # ✅ 附加项（配料）查找
    def get_addons_for_label(self, label: str) -> list[dict]:
        # 1️⃣ 先尝试直接匹配 label
        df = self.addons[self.addons["applies_to_labels"].str.contains(label, case=False, na=False)]
        if not df.empty:
            return [r._asdict() if hasattr(r, "_asdict") else dict(r) for _, r in df.iterrows()]

        # 2️⃣ 如果没匹配到，尝试关键词匹配主类（如 hamburger → burger）
        base = self.get_base(label)
        if base:
            true_label = base["label"]
            df = self.addons[self.addons["applies_to_labels"].str.contains(true_label, case=False, na=False)]
            if not df.empty:
                return [r._asdict() if hasattr(r, "_asdict") else dict(r) for _, r in df.iterrows()]

        # 3️⃣ 都没找到就返回空列表
        return []


    # ✅ 根据关键字查找主类别（备用功能）
    def find_label_by_keyword(self, text: str) -> str | None:
        t = text.lower()
        for _, r in self.mapping.iterrows():
            if any(kw in t for kw in r["kw_list"]):
                return r["label"]
        return None


# 计算总营养
def calc_totals(base: dict, grams: int, selected_addons: list[dict]) -> dict:
    factor = grams / 100.0
    base_totals = {
        "kcal": base["base_kcal_per_100g"] * factor,
        "protein_g": base["base_protein_g_per_100g"] * factor,
        "fat_g": base["base_fat_g_per_100g"] * factor,
        "carb_g": base["base_carb_g_per_100g"] * factor,
    }
    addon_totals = {"kcal":0,"protein_g":0,"fat_g":0,"carb_g":0}
    for a in selected_addons:
        addon_totals["kcal"] += float(a["delta_kcal_per_unit"])   # type: ignore
        addon_totals["protein_g"] += float(a["delta_protein_g"])   # type: ignore
        addon_totals["fat_g"] += float(a["delta_fat_g"])   # type: ignore
        addon_totals["carb_g"] += float(a["delta_carb_g"])    # type: ignore
    totals = {
        "kcal": round(base_totals["kcal"] + addon_totals["kcal"]),
        "protein_g": round(base_totals["protein_g"] + addon_totals["protein_g"], 1),
        "fat_g": round(base_totals["fat_g"] + addon_totals["fat_g"], 1),
        "carb_g": round(base_totals["carb_g"] + addon_totals["carb_g"], 1),
    }
    # 先用±15% 作为不确定区间
    rng = {"kcal_low": round(totals["kcal"] * 0.85), "kcal_high": round(totals["kcal"] * 1.15)}
    return {"totals": totals, "range": rng}

# 简单缓存 label+grams+addons 结果
class NutriCache:
    def __init__(self):  # 500 个键，生存 48h
        self.cache = TTLCache(maxsize=500, ttl=60*60*48)

    def key(self, label, grams, addon_ids):
        return f"{label}|{grams}|{','.join(sorted(addon_ids))}"

    def get(self, label, grams, addon_ids):
        return self.cache.get(self.key(label, grams, addon_ids))

    def set(self, label, grams, addon_ids, value):
        self.cache[self.key(label, grams, addon_ids)] = value

