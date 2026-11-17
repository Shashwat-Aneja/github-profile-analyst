import json
import analyze_github


def test_json_cli_emits_one_machine_readable_document(monkeypatch, capsys):
    expected = {"Username": "demo", "Name": "Renée", "Total Stars": 2}
    monkeypatch.setattr(analyze_github, "fetch_github_data", lambda username: expected)
    analyze_github.main(["demo", "--json"])
    assert json.loads(capsys.readouterr().out) == expected
