import hashlib

from rapidfuzz import fuzz


def row_hash(row):
  """
  Hash only relatively stable fields.
  Address is excluded intentionally.
  """
  values = [
    row["Subsidiary"],
    row["Country ISO-2 Code"],
    row["Entity Registration Number"]
  ]
  joined = "|".join(values)
  return hashlib.sha256(joined.encode()).hexdigest()


def compute_hashes(df):
  df = df.copy()
  df["row_hash"] = df.apply(row_hash, axis=1)
  return df


def similarity_score(row_a, row_b):
  """
  Business-aligned similarity scoring.
  """

  reg_a = row_a["Entity Registration Number"]
  reg_b = row_b["Entity Registration Number"]

  # If registration number matches, we consider it the same entity
  if reg_a and reg_a == reg_b:
    return 100.0

  name_score = fuzz.token_sort_ratio(
    row_a["Subsidiary"], row_b["Subsidiary"]
  )

  address_score = fuzz.token_sort_ratio(
    row_a["Registered Address"], row_b["Registered Address"]
  )

  iso_score = (
    100 if row_a["Country ISO-2 Code"] == row_b["Country ISO-2 Code"] else 0
  )

  # Weighted average based on change frequency
  return (
    name_score * 0.45 +
    address_score * 0.40 +
    iso_score * 0.15
  )
