import os
import sys
import uuid
import pandas as pd

# Add parent directory to path so we can import from newsletter package
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from newsletter.objectfactory import ObjectFactory


def main():
    """Simple smoke test for SnippetDBPostgres using the ObjectFactory."""
    factory = ObjectFactory()
    snippet_db = factory.get_obj(ObjectFactory.SNIPPET_DB)

    project = f"demo-project-{uuid.uuid4().hex[:8]}"
    category = "examples"
    text = "Hello from SnippetDBPostgres backed by PostgreSQL!"
    approval_state = 1
    deleted = 0

    if not snippet_db.add(project, category, text, approval_state=approval_state, deleted=deleted):
        raise RuntimeError("Failed to insert the demo snippet row.")

    df = snippet_db.get_all_df()
    matching_rows = df[
        (df["project"] == project)
        & (df["category"] == category)
        & (df["text"] == text)
    ]
    if matching_rows.empty:
        raise AssertionError("Inserted snippet not found in the database.")

    row = matching_rows.iloc[-1]
    assert row["approval_state"] == approval_state
    assert row["deleted"] == deleted
    # added_ts might be numpy int64 from pandas, so convert to int for comparison
    added_ts_value = int(row["added_ts"])
    assert added_ts_value > 0  # Should be a valid timestamp

    print("Snippet inserted and verified successfully:", row.to_dict())


if __name__ == "__main__":
    main()

