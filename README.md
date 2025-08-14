# Discord Auto-Reply Bot

メッセージの自動返信機能を持つDiscord BOTです。

## 機能

- 挨拶への自動返信
  - 「こんにちは」「hello」→ 挨拶を返信
  - 「おはよう」「good morning」→ 朝の挨拶を返信  
  - 「おやすみ」「good night」→ 夜の挨拶を返信
- 感謝への自動返信
  - 「ありがとう」「thank you」→ お礼の返信
- メンション応答
  - BOTがメンションされた時に反応
- コマンド機能
  - `!ping` → Pong!を返信

## セットアップ

1. 必要なライブラリをインストール
```bash
pip install -r requirements.txt
```

2. Discord Developer Portalでボットを作成
   - https://discord.com/developers/applications/
   - 新しいアプリケーションを作成
   - "Bot"タブでトークンを取得
   - "Privileged Gateway Intents"で`MESSAGE CONTENT INTENT`を有効化

3. 環境変数を設定
```bash
cp .env.example .env
```
`.env`ファイルにボットトークンを設定

4. ボットを実行
```bash
python bot.py
```

## ファイル構成

- `bot.py` - メインのボットコード
- `requirements.txt` - 必要なライブラリ
- `.env.example` - 環境変数のサンプル
- `.gitignore` - Git除外ファイル