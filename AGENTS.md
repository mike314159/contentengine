

This project uses uv and pytest.

### Test Commands

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest app/youtube/test_youtubeclient.py

# Run specific test method
uv run pytest app/youtube/test_youtubeclient.py::TestYouTubeClient::test_get_channel_id

# Run with verbose output and show print statements
uv run pytest -v -s
```
