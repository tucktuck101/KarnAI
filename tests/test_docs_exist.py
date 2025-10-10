from pathlib import Path


def test_contributor_doc_and_readme_exist():
    assert Path("docs/21_contributor_guide.md").exists()
    assert Path("README.md").exists()
