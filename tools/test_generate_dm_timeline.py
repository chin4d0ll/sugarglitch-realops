import json
from generate_dm_timeline import generate_dm_timeline

dummy_dms = {
    "conversations": [
        {
            "messages": [
                {"created_at": "2025-06-01T12:00:00", "text": "Hi"},
                {"created_at": "2025-06-01T13:00:00", "text": "Hello"},
                {"created_at": "2025-06-02T09:00:00", "text": "How are you?"},
                {"created_at": "2025-06-03T10:00:00", "text": "Good morning"},
                {"created_at": "2025-06-03T11:00:00", "text": "Good night"},
            ]
        },
        {
            "messages": [
                {"created_at": "2025-06-02T15:00:00", "text": "Hey"},
                {"created_at": "2025-06-03T16:00:00", "text": "What's up?"},
                {"created_at": "2025-06-03T17:00:00", "text": "See you"},
            ]
        }
    ]
}

if __name__ == "__main__":
    generate_dm_timeline(dummy_dms, "test_dm_timeline.png")
    print("Timeline chart saved as test_dm_timeline.png")
