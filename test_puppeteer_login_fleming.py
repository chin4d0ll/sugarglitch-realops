import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from puppeteer_login_fleming import PuppeteerInstagramLogin

@pytest.mark.asyncio
async def test_fresh_login_success(monkeypatch, tmp_path):
    # Arrange
    bot = PuppeteerInstagramLogin()
    bot.base_dir = tmp_path
    bot.sessions_dir = tmp_path / "sessions"
    bot.sessions_dir.mkdir(parents=True, exist_ok=True)

    # Mock Playwright context and page
    mock_browser = AsyncMock()
    mock_context = AsyncMock()
    mock_page = AsyncMock()
    mock_playwright = MagicMock()
    mock_playwright.chromium.launch = AsyncMock(return_value=mock_browser)
    mock_browser.new_context = AsyncMock(return_value=mock_context)
    mock_context.new_page = AsyncMock(return_value=mock_page)
    mock_page.url = "https://www.instagram.com/"
    mock_page.context.cookies = AsyncMock(return_value=[
        {'domain': '.instagram.com', 'name': 'sessionid', 'value': 'abc123'},
        {'domain': '.instagram.com', 'name': 'csrftoken', 'value': 'token'},
        {'domain': '.instagram.com', 'name': 'ds_user_id', 'value': '12345'},
        {'domain': '.instagram.com', 'name': 'mid', 'value': 'midval'},
        {'domain': '.instagram.com', 'name': 'rur', 'value': 'rurval'},
    ])
    mock_page.query_selector = AsyncMock(return_value=True)
    mock_page.text_content = AsyncMock(return_value="")

    # Patch async_playwright context manager
    class DummyAsyncPlaywright:
        async def __aenter__(self):
            return mock_playwright
        async def __aexit__(self, exc_type, exc, tb):
            return False

    monkeypatch.setattr("puppeteer_login_fleming.async_playwright", DummyAsyncPlaywright)

    # Patch sleeps to speed up test
    monkeypatch.setattr("asyncio.sleep", AsyncMock())

    # Act
    result = await bot.fresh_login()

    # Assert
    assert result is True
    session_files = list((tmp_path / "sessions").glob("fleming_fresh_session_*.json"))
    assert session_files, "Session file should be created"
    with open(session_files[0]) as f:
        data = f.read()
        assert "sessionid" in data

@pytest.mark.asyncio
async def test_fresh_login_no_login_form(monkeypatch, tmp_path):
    bot = PuppeteerInstagramLogin()
    bot.base_dir = tmp_path
    bot.sessions_dir = tmp_path / "sessions"
    bot.sessions_dir.mkdir(parents=True, exist_ok=True)

    mock_browser = AsyncMock()
    mock_context = AsyncMock()
    mock_page = AsyncMock()
    mock_playwright = MagicMock()
    mock_playwright.chromium.launch = AsyncMock(return_value=mock_browser)
    mock_browser.new_context = AsyncMock(return_value=mock_context)
    mock_context.new_page = AsyncMock(return_value=mock_page)
    mock_page.query_selector = AsyncMock(side_effect=[None, None])  # No login form, no alt input

    class DummyAsyncPlaywright:
        async def __aenter__(self):
            return mock_playwright
        async def __aexit__(self, exc_type, exc, tb):
            return False

    monkeypatch.setattr("puppeteer_login_fleming.async_playwright", DummyAsyncPlaywright)
    monkeypatch.setattr("asyncio.sleep", AsyncMock())

    result = await bot.fresh_login()
    assert result is False

@pytest.mark.asyncio
async def test_fresh_login_login_failed(monkeypatch, tmp_path):
    bot = PuppeteerInstagramLogin()
    bot.base_dir = tmp_path
    bot.sessions_dir = tmp_path / "sessions"
    bot.sessions_dir.mkdir(parents=True, exist_ok=True)

    mock_browser = AsyncMock()
    mock_context = AsyncMock()
    mock_page = AsyncMock()
    mock_playwright = MagicMock()
    mock_playwright.chromium.launch = AsyncMock(return_value=mock_browser)
    mock_browser.new_context = AsyncMock(return_value=mock_context)
    mock_context.new_page = AsyncMock(return_value=mock_page)
    mock_page.url = "https://www.instagram.com/accounts/login/"
    mock_page.query_selector = AsyncMock(return_value=True)
    mock_page.text_content = AsyncMock(return_value="incorrect password")

    class DummyAsyncPlaywright:
        async def __aenter__(self):
            return mock_playwright
        async def __aexit__(self, exc_type, exc, tb):
            return False

    monkeypatch.setattr("puppeteer_login_fleming.async_playwright", DummyAsyncPlaywright)
    monkeypatch.setattr("asyncio.sleep", AsyncMock())

    result = await bot.fresh_login()
    assert result is False

@pytest.mark.asyncio
async def test_fresh_login_no_sessionid(monkeypatch, tmp_path):
    bot = PuppeteerInstagramLogin()
    bot.base_dir = tmp_path
    bot.sessions_dir = tmp_path / "sessions"
    bot.sessions_dir.mkdir(parents=True, exist_ok=True)

    mock_browser = AsyncMock()
    mock_context = AsyncMock()
    mock_page = AsyncMock()
    mock_playwright = MagicMock()
    mock_playwright.chromium.launch = AsyncMock(return_value=mock_browser)
    mock_browser.new_context = AsyncMock(return_value=mock_context)
    mock_context.new_page = AsyncMock(return_value=mock_page)
    mock_page.url = "https://www.instagram.com/"
    mock_page.query_selector = AsyncMock(return_value=True)
    mock_page.context.cookies = AsyncMock(return_value=[
        {'domain': '.instagram.com', 'name': 'csrftoken', 'value': 'token'}
    ])

    class DummyAsyncPlaywright:
        async def __aenter__(self):
            return mock_playwright
        async def __aexit__(self, exc_type, exc, tb):
            return False

    monkeypatch.setattr("puppeteer_login_fleming.async_playwright", DummyAsyncPlaywright)
    monkeypatch.setattr("asyncio.sleep", AsyncMock())

    result = await bot.fresh_login()
    assert result is False