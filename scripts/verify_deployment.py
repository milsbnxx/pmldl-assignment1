import json
import time
import urllib.request

URLS = {
    "api": "http://localhost:8000/health",
    "app": "http://localhost:8501/_stcore/health",
}


def wait_for(name: str, url: str, attempts: int = 24, delay: int = 5) -> None:
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                body = response.read().decode("utf-8", errors="replace")
                if 200 <= response.status < 300:
                    print(f"{name} is ready: HTTP {response.status} {body[:120]}")
                    return
        except Exception as exc:  # noqa: BLE001 - smoke test should report any connection failure
            last_error = exc
        print(f"Waiting for {name} ({attempt}/{attempts})...")
        time.sleep(delay)
    raise RuntimeError(f"{name} did not become ready at {url}. Last error: {last_error}")


def main() -> None:
    for name, url in URLS.items():
        wait_for(name, url)
    print(json.dumps({"deployment": "healthy", "services": list(URLS)}, indent=2))


if __name__ == "__main__":
    main()
