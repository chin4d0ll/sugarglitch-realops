import os
import json
import tempfile
import shutil
from unittest import mock
import pytest
from hijacked_session_dm_extractor import load_working_hijacked_session

@pytest.fixture
def temp_session_dir():
    # Create a temporary directory to act as hijacked_sessions
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def patch_session_dir(monkeypatch, temp_session_dir):
    # Patch the session_dir path in the function to use our temp dir
    monkeypatch.setattr(
        "hijacked_session_dm_extractor.load_working_hijacked_session.__globals__",
        "session_dir",
        temp_session_dir,
        raising=False
    )

def make_session_file(path, data, mtime=None):
    with open(path, "w") as f:
        json.dump(data, f)
    if mtime:
        os.utime(path, (mtime, mtime))

def test_no_session_files(monkeypatch, tmp_path):
    # Patch session_dir and fallback_files to empty temp dir
    monkeypatch.setattr("hijacked_session_dm_extractor.os.listdir", lambda d: [])
    monkeypatch.setattr("hijacked_session_dm_extractor.os.path.exists", lambda f: False)
    monkeypatch.setattr("hijacked_session_dm_extractor.print", lambda *a, **k: None)
    assert load_working_hijacked_session() is None

def test_valid_hijacked_session(monkeypatch, tmp_path):
    session_dir = tmp_path / "hijacked_sessions"
    session_dir.mkdir()
    session_file = session_dir / "session1.json"
    session_data = {"cookies": [{"name": "sessionid", "value": "abc"}]}
    make_session_file(session_file, session_data)
    # Patch paths
    monkeypatch.setattr("hijacked_session_dm_extractor.os.listdir", lambda d: ["session1.json"])
    monkeypatch.setattr("hijacked_session_dm_extractor.os.path.exists", lambda f: False)
    monkeypatch.setattr("hijacked_session_dm_extractor.os.path.getmtime", lambda f: 100)
    monkeypatch.setattr("hijacked_session_dm_extractor.open", open)
    monkeypatch.setattr("hijacked_session_dm_extractor.print", lambda *a, **k: None)
    # Patch test_session_validity to return True for our session
    monkeypatch.setattr("hijacked_session_dm_extractor.test_session_validity", lambda data, user_agent=None: True)
    # Patch session_dir in function
    monkeypatch.setattr("hijacked_session_dm_extractor.load_working_hijacked_session.__globals__", "session_dir", str(session_dir), raising=False)
    result = load_working_hijacked_session()
    assert result == session_data

def test_invalid_then_valid_session(monkeypatch, tmp_path):
    session_dir = tmp_path / "hijacked_sessions"
    session_dir.mkdir()
    session1 = session_dir / "session1.json"
    session2 = session_dir / "session2.json"
    data1 = {"cookies": [{"name": "sessionid", "value": "bad"}]}
    data2 = {"cookies": [{"name": "sessionid", "value": "good"}]}
    make_session_file(session1, data1)
    make_session_file(session2, data2)
    # Patch paths
    monkeypatch.setattr("hijacked_session_dm_extractor.os.listdir", lambda d: ["session1.json", "session2.json"])
    monkeypatch.setattr("hijacked_session_dm_extractor.os.path.exists", lambda f: False)
    # session2 newer
    monkeypatch.setattr("hijacked_session_dm_extractor.os.path.getmtime", lambda f: 200 if "session2" in f else 100)
    monkeypatch.setattr("hijacked_session_dm_extractor.open", open)
    monkeypatch.setattr("hijacked_session_dm_extractor.print", lambda *a, **k: None)
    # test_session_validity returns False for session2, True for session1
    def fake_test_session_validity(data, user_agent=None):
        if data == data2:
            return False
        if data == data1:
            return True
    monkeypatch.setattr("hijacked_session_dm_extractor.test_session_validity", fake_test_session_validity)
    monkeypatch.setattr("hijacked_session_dm_extractor.load_working_hijacked_session.__globals__", "session_dir", str(session_dir), raising=False)
    result = load_working_hijacked_session()
    assert result == data1

def test_fallback_session(monkeypatch, tmp_path):
    session_dir = tmp_path / "hijacked_sessions"
    session_dir.mkdir()
    fallback_file = tmp_path / "session.json"
    fallback_data = {"cookies": [{"name": "sessionid", "value": "fallback"}]}
    make_session_file(fallback_file, fallback_data)
    # Patch paths
    monkeypatch.setattr("hijacked_session_dm_extractor.os.listdir", lambda d: [])
    monkeypatch.setattr("hijacked_session_dm_extractor.os.path.exists", lambda f: str(f) == str(fallback_file))
    monkeypatch.setattr("hijacked_session_dm_extractor.os.path.getmtime", lambda f: 100)
    monkeypatch.setattr("hijacked_session_dm_extractor.open", open)
    monkeypatch.setattr("hijacked_session_dm_extractor.print", lambda *a, **k: None)
    monkeypatch.setattr("hijacked_session_dm_extractor.test_session_validity", lambda data, user_agent=None: True)
    # Patch fallback_files in function
    monkeypatch.setattr("hijacked_session_dm_extractor.load_working_hijacked_session.__globals__", "session_dir", str(session_dir), raising=False)
    monkeypatch.setattr("hijacked_session_dm_extractor.load_working_hijacked_session.__globals__", "fallback_files", [str(fallback_file)], raising=False)
    result = load_working_hijacked_session()
    assert result == fallback_data

def test_all_sessions_invalid(monkeypatch, tmp_path):
    session_dir = tmp_path / "hijacked_sessions"
    session_dir.mkdir()
    session_file = session_dir / "session1.json"
    session_data = {"cookies": [{"name": "sessionid", "value": "abc"}]}
    make_session_file(session_file, session_data)
    # Patch paths
    monkeypatch.setattr("hijacked_session_dm_extractor.os.listdir", lambda d: ["session1.json"])
    monkeypatch.setattr("hijacked_session_dm_extractor.os.path.exists", lambda f: False)
    monkeypatch.setattr("hijacked_session_dm_extractor.os.path.getmtime", lambda f: 100)
    monkeypatch.setattr("hijacked_session_dm_extractor.open", open)
    monkeypatch.setattr("hijacked_session_dm_extractor.print", lambda *a, **k: None)
    monkeypatch.setattr("hijacked_session_dm_extractor.test_session_validity", lambda data, user_agent=None: False)
    monkeypatch.setattr("hijacked_session_dm_extractor.load_working_hijacked_session.__globals__", "session_dir", str(session_dir), raising=False)
    result = load_working_hijacked_session()
    assert result is None