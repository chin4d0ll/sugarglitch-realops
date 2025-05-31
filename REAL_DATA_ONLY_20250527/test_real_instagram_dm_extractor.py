import pytest
from unittest.mock import patch, MagicMock
from REAL_DATA_ONLY_20250527.real_instagram_dm_extractor import RealInstagramDMExtractor

@pytest.fixture
def extractor():
    extractor = RealInstagramDMExtractor()
    extractor.session_data = {'sessionid': 'real_sessionid_example_987654'}
    return extractor

@patch("REAL_DATA_ONLY_20250527.real_instagram_dm_extractor.time.sleep", return_value=None)
@patch("REAL_DATA_ONLY_20250527.real_instagram_dm_extractor.requests.Session")
def test_login_suc
cess_data_payload(mock_session_cls, mock_sleep, extractor):
    mock_session = MagicMock()
    extractor.session = mock_session

    # Mock pre-login GET
    pre_login_response = MagicMock()
    # Use real data: simulate a real CSRF token value as would be returned by Instagram
    pre_login_response.cookies.get.return_value = "csrftoken_real_example_123456"
    mock_session.get.return_value = pre_login_response

    # Mock POST (data=payload) - success
    post_response = MagicMock()
    post_response.status_code = 200
    post_response.text = '{"authenticated": true}'
    mock_session.post.return_value = post_response

    result = extractor.login_and_fetch_session("user", "pass")
    assert result == extractor.session_data
    assert mock_session.post.call_count >= 1

@patch("REAL_DATA_ONLY_20250527.real_instagram_dm_extractor.time.sleep", return_value=None)
@patch("REAL_DATA_ONLY_20250527.real_instagram_dm_extractor.requests.Session")
def test_login_success_json_payload(mock_session_cls, mock_sleep, extractor: RealInstagramDMExtractor):
    mock_session = MagicMock()
    extractor.session = mock_session

    # Mock pre-login GET
    pre_login_response = MagicMock()
    pre_login_response.cookies.get.return_value = "fake_csrf"
    mock_session.get.return_value = pre_login_response

    # Mock POST (data=payload) - fail
    post_response = MagicMock()
    post_response.status_code = 400
    post_response.text = '{}'
    # Mock POST (json=payload) - success
    post_json_response = MagicMock()
    post_json_response.status_code = 200
    post_json_response.text = '{"authenticated": true}'
    mock_session.post.side_effect = [post_response, post_json_response]

    result = extractor.login_and_fetch_session("user", "pass")
    assert result == extractor.session_data
    assert mock_session.post.call_count >= 2

@patch("REAL_DATA_ONLY_20250527.real_instagram_dm_extractor.time.sleep", return_value=None)
@patch("REAL_DATA_ONLY_20250527.real_instagram_dm_extractor.requests.Session")
def test_login_success_fresh_session(mock_session_cls, mock_sleep, extractor: RealInstagramDMExtractor):
    mock_session = MagicMock()
    extractor.session = mock_session

    # Mock pre-login GET
    pre_login_response = MagicMock()
    pre_login_response.cookies.get.return_value = "fake_csrf"
    mock_session.get.return_value = pre_login_response

    # Mock POST (data=payload) - fail
    post_response = MagicMock()
    post_response.status_code = 400
    post_response.text = '{}'
    # Mock POST (json=payload) - fail
    post_json_response = MagicMock()
    post_json_response.status_code = 400
    post_json_response.text = '{}'
    # Mock POST (fresh session) - success
    fresh_session = MagicMock()
    fresh_pre_login = MagicMock()
    fresh_pre_login.cookies.get.return_value = "fresh_csrf"
    fresh_session.get.return_value = fresh_pre_login
    fresh_post_response = MagicMock()
    fresh_post_response.status_code = 200
    fresh_post_response.text = '{"authenticated": true}'
    fresh_session.post.return_value = fresh_post_response
    mock_session_cls.return_value = fresh_session

    mock_session.post.side_effect = [post_response, post_json_response]

    result = extractor.login_and_fetch_session("user", "pass")
    assert result == extractor.session_data
    assert mock_session_cls.call_count >= 1

@patch("REAL_DATA_ONLY_20250527.real_instagram_dm_extractor.time.sleep", return_value=None)
@patch("REAL_DATA_ONLY_20250527.real_instagram_dm_extractor.requests.Session")
def test_login_success_appid(mock_session_cls, mock_sleep, extractor: RealInstagramDMExtractor):
    mock_session = MagicMock()
    extractor.session = mock_session

    # Mock pre-login GET
    pre_login_response = MagicMock()
    pre_login_response.cookies.get.return_value = "fake_csrf"
    mock_session.get.return_value = pre_login_response

    # Mock POST (data=payload) - fail
    post_response = MagicMock()
    post_response.status_code = 400
    post_response.text = '{}'
    # Mock POST (json=payload) - fail
    post_json_response = MagicMock()
    post_json_response.status_code = 400
    post_json_response.text = '{}'
    # Mock POST (fresh session) - fail
    fresh_session = MagicMock()
    fresh_pre_login = MagicMock()
    fresh_pre_login.cookies.get.return_value = "fresh_csrf"
    fresh_session.get.return_value = fresh_pre_login
    fresh_post_response = MagicMock()
    fresh_post_response.status_code = 400
    fresh_post_response.text = '{}'
    fresh_session.post.return_value = fresh_post_response
    mock_session_cls.return_value = fresh_session
    # Mock POST (appid) - success
    post_appid_response = MagicMock()
    post_appid_response.status_code = 200
    post_appid_response.text = '{"authenticated": true}'

    mock_session.post.side_effect = [post_response, post_json_response, post_appid_response]

    result = extractor.login_and_fetch_session("user", "pass")
    assert result == extractor.session_data
    assert mock_session.post.call_count == 3

@patch("REAL_DATA_ONLY_20250527.real_instagram_dm_extractor.time.sleep", return_value=None)
@patch("REAL_DATA_ONLY_20250527.real_instagram_dm_extractor.requests.Session")
def test_login_all_methods_fail(mock_session_cls, mock_sleep, extractor: RealInstagramDMExtractor):
    mock_session = MagicMock()
    extractor.session = mock_session

    # Mock pre-login GET
    pre_login_response = MagicMock()
    pre_login_response.cookies.get.return_value = "fake_csrf"
    mock_session.get.return_value = pre_login_response

    # All POSTs fail
    post_response = MagicMock()
    post_response.status_code = 400
    post_response.text = '{}'
    post_json_response = MagicMock()
    post_json_response.status_code = 400
    post_json_response.text = '{}'
    post_appid_response = MagicMock()
    post_appid_response.status_code = 400
    post_appid_response.text = '{}'

    # Fresh session also fails
    fresh_session = MagicMock()
    fresh_pre_login = MagicMock()
    fresh_pre_login.cookies.get.return_value = "fresh_csrf"
    fresh_session.get.return_value = fresh_pre_login
    fresh_post_response = MagicMock()
    fresh_post_response.status_code = 400
    fresh_post_response.text = '{}'
    fresh_session.post.return_value = fresh_post_response
    mock_session_cls.return_value = fresh_session

    mock_session.post.side_effect = [post_response, post_json_response, post_appid_response]

    result = extractor.login_and_fetch_session("user", "pass")
    assert result is None