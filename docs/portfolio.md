# Portfolio Collateral

## Resume bullets

- Built a Python pipeline that classifies Watch Later videos by spoken language using 90-second audio samples and local Whisper inference.
- Reduced playlist mutation risk through preview-by-default behavior, confidence thresholds, exact UI locators, and add-before-remove transaction ordering.
- Protected browser sessions and media history by keeping cookies local and deleting temporary audio automatically.
- Integrated yt-dlp, faster-whisper, Playwright, FFmpeg, and Chrome into a reviewable human-in-the-loop automation workflow.

## LinkedIn

I built a privacy-conscious Python tool that organizes YouTube Watch Later by spoken language. Instead of trusting titles, it samples the first 90 seconds of each video, runs local faster-whisper language detection, and reports confidence before changing anything. Preview mode is the default. During an approved run, Playwright adds each high-confidence English video to the destination playlist before removing it from Watch Later, protecting the source when a UI operation fails. The project combines yt-dlp, Whisper, Playwright, FFmpeg, and strict secret handling to demonstrate how uncertain AI predictions can be converted into safe, human-governed automation.

## Commit message

```text
docs: publish English project and Medium content
```

## Future work

- resumable SQLite checkpoints
- multi-window language sampling
- human review dashboard
- structured audit reports and retries
- generalized multilingual playlist agents
