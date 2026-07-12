"""Move English-spoken videos from YouTube Watch Later to a named playlist."""
from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path

from faster_whisper import WhisperModel
from playwright.sync_api import Page, sync_playwright


def run(*args: str) -> str:
    return subprocess.check_output(args, text=True, encoding="utf-8")


def watch_later_entries(browser: str) -> list[dict]:
    raw = run("yt-dlp", "--cookies-from-browser", browser, "--flat-playlist",
              "--dump-single-json", "https://www.youtube.com/playlist?list=WL")
    return json.loads(raw).get("entries", [])


def language(video_id: str, browser: str, model: WhisperModel) -> tuple[str, float]:
    with tempfile.TemporaryDirectory() as td:
        target = str(Path(td) / "audio.%(ext)s")
        subprocess.run(["yt-dlp", "--cookies-from-browser", browser, "-x",
                        "--audio-format", "mp3", "--download-sections", "*0-90",
                        "-o", target, f"https://youtu.be/{video_id}"], check=True)
        audio = next(Path(td).glob("audio.*"))
        _, info = model.transcribe(str(audio), beam_size=1)
        return info.language, info.language_probability


def click_unique(page: Page, role: str, names: tuple[str, ...]) -> None:
    for name in names:
        loc = page.get_by_role(role, name=name, exact=True)
        if loc.count() == 1:
            loc.click()
            return
    raise RuntimeError(f"找不到唯一控制項: {names}")


def move_in_ui(page: Page, video_id: str, playlist: str) -> None:
    page.goto(f"https://www.youtube.com/watch?v={video_id}", wait_until="domcontentloaded")
    click_unique(page, "button", ("儲存", "Save"))
    dialog = page.get_by_role("dialog")
    dialog.wait_for()
    target = dialog.get_by_text(playlist, exact=True)
    if target.count() != 1:
        raise RuntimeError(f"找不到播放清單：{playlist}")
    target.click()
    wl = dialog.get_by_text("稍後觀看", exact=True).or_(dialog.get_by_text("Watch later", exact=True))
    if wl.count() == 1:
        wl.click()
    page.keyboard.press("Escape")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--playlist", default="大便")
    ap.add_argument("--browser", default="chrome")
    ap.add_argument("--profile-dir", help="Chrome User Data 資料夾；正式移動時必填")
    ap.add_argument("--model", default="small")
    ap.add_argument("--threshold", type=float, default=.80)
    ap.add_argument("--apply", action="store_true", help="實際移動；預設僅預覽")
    args = ap.parse_args()

    entries = watch_later_entries(args.browser)
    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    english = []
    for i, item in enumerate(entries, 1):
        code, confidence = language(item["id"], args.browser, model)
        result = {"id": item["id"], "title": item.get("title"), "language": code,
                  "confidence": round(confidence, 4)}
        print(json.dumps(result, ensure_ascii=False))
        if code == "en" and confidence >= args.threshold:
            english.append(item["id"])

    if not args.apply:
        print(f"預覽完成：{len(english)} 部英文影片；加上 --apply 才會移動。")
        return
    if not args.profile_dir:
        ap.error("--apply 需要 --profile-dir")
    with sync_playwright() as pw:
        context = pw.chromium.launch_persistent_context(args.profile_dir, channel="chrome", headless=False)
        page = context.pages[0] if context.pages else context.new_page()
        for video_id in english:
            move_in_ui(page, video_id, args.playlist)
        context.close()


if __name__ == "__main__":
    main()
