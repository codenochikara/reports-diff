import pandas as pd

from matcher import similarity_score


def diff_entities(old_df, new_df):
    added = []
    removed = []
    modified = []

    matched_old = set()
    matched_new = set()

    # Phase 1: Hash matches
    hash_map_old = {row["row_hash"]: idx for idx, row in old_df.iterrows()}
    hash_map_new = {row["row_hash"]: idx for idx, row in new_df.iterrows()}

    for h in set(hash_map_old) & set(hash_map_new):
        matched_old.add(hash_map_old[h])
        matched_new.add(hash_map_new[h])

    # Phase 2: Fuzzy matching
    for old_idx, old_row in old_df.iterrows():
        if old_idx in matched_old:
            continue

        best_match = None
        best_score = 0

        for new_idx, new_row in new_df.iterrows():
            if new_idx in matched_new:
                continue

            score = similarity_score(old_row, new_row)
            if score > best_score:
                best_score = score
                best_match = new_idx

        if best_score >= 85:
            matched_old.add(old_idx)
            matched_new.add(best_match)

            changes = {}
            for col in old_df.columns:
                if col == "row_hash":
                    continue
                if old_row[col] != new_df.loc[best_match, col]:
                    changes[col] = {
                        "old": old_row[col],
                        "new": new_df.loc[best_match, col]
                    }

            if changes:
                modified.append(changes)
        else:
            removed.append(old_row)

    # Phase 3: Additions
    for new_idx, new_row in new_df.iterrows():
        if new_idx not in matched_new:
            added.append(new_row)

    return (
        pd.DataFrame(added),
        pd.DataFrame(removed),
        pd.DataFrame(format_modified(modified))
    )


def format_modified(modified):
    rows = []
    for change in modified:
        for field, vals in change.items():
            rows.append({
                "Field": field,
                "Old Value": vals["old"],
                "New Value": vals["new"]
            })
    return rows
