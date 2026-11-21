import json,pytest
import analyze_github as app
def test_profile_export_round_trip(tmp_path):
    p=tmp_path/'nested'/'profile.json';app.export_profile_json({'Name':'Démo','Total Stars':3},p)
    assert json.loads(p.read_text())=={'Name':'Démo','Total Stars':3}
def test_replace_failure_preserves_previous_summary(tmp_path,monkeypatch):
    p=tmp_path/'profile.json';p.write_text('keep')
    def fail(*args):raise OSError('replace failed')
    monkeypatch.setattr(app.os,'replace',fail)
    with pytest.raises(OSError):app.export_profile_json({'Total Stars':3},p)
    assert p.read_text()=='keep' and list(tmp_path.iterdir())==[p]
