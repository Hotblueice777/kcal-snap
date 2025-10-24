# backend/utils/build_knowledge.py
import pandas as pd

def csv_to_docs():
    """Convert mapping.csv & addons.csv into text documents for embeddings"""
    docs = []

    # basic food dataset
    try:
        df = pd.read_csv("data/mapping.csv")
        for _, row in df.iterrows():
            text = (
                f"{row['label']} ({row['keywords']}) provides about "
                f"{row['base_kcal_per_100g']} kcal, "
                f"{row['base_protein_g_per_100g']}g protein, "
                f"{row['base_fat_g_per_100g']}g fat, and "
                f"{row['base_carb_g_per_100g']}g carbohydrates per 100g."
            )

            docs.append(text)
    except Exception as e:
        print("⚠️ mapping.csv not loaded:", e)

    # addons datasets
    try:
        df2 = pd.read_csv("data/addons.csv")
        for _, row in df2.iterrows():
            addon = row.get("addon", "")
            kcal = row.get("kcal", "")
            if addon:
                text = f"Addon {addon} provides about {kcal} kcal energy."
                docs.append(text)
    except Exception as e:
        print("⚠️ addons.csv not loaded:", e)

    print(f"✅ Loaded {len(docs)} knowledge items.")
    return docs

# performance while run script
if __name__ == "__main__":
    docs = csv_to_docs()
    print("\n📘 Sample (first 3 entries):")
    for t in docs[:3]:
        print("-", t)