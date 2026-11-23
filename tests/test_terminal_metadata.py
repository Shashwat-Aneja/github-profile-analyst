from analyze_github import display_data

def test_remote_metadata_cannot_emit_terminal_controls(capsys):
    display_data({'Name': 'café\x1b[2J\nspoofed'})
    output = capsys.readouterr().out
    assert '\x1b' not in output
    assert 'café\\x1b[2J\\nspoofed' in output
