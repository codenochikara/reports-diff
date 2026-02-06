from differ import diff_entities
from loader import load_excel
from matcher import compute_hashes
from normalizer import normalize_df


def run():
    old_df = load_excel("data/prev.xlsx")
    new_df = load_excel("data/curr.xlsx")

    old_df = normalize_df(old_df)
    new_df = normalize_df(new_df)

    old_df = compute_hashes(old_df)
    new_df = compute_hashes(new_df)

    added, removed, modified = diff_entities(old_df, new_df)

    added.to_excel("output/added_entities.xlsx", index=False)
    removed.to_excel("output/removed_entities.xlsx", index=False)
    modified.to_excel("output/modified_entities.xlsx", index=False)

if __name__ == "__main__":
    run()
