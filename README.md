# YouTube 英文影片分類器

以 Python 掃描 YouTube「稍後觀看」，擷取每部影片前 90 秒音訊，使用 Whisper 判斷口語語言，並把高可信度英文影片移到指定播放清單（預設「大便」）。

## 安裝

需要 Python 3.11+、FFmpeg 與已登入 YouTube 的 Chrome。

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
```

先關閉 Chrome，然後預覽（不修改播放清單）：

```powershell
python yt_playlist_mover.py
```

確認輸出後正式移動：

```powershell
python yt_playlist_mover.py --apply --profile-dir "$env:LOCALAPPDATA\Google\Chrome\User Data"
```

可用 `--threshold 0.9` 提高英文判定門檻。工具只有在加入目標清單的操作成功後才會取消「稍後觀看」。YouTube 介面若改版，定位文字可能需要調整。

## 隱私

Cookie、音訊與登入資料不會加入 Git；音訊只存在系統暫存資料夾，辨識完成即刪除。
