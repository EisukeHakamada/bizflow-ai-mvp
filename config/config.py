"""
BizFlow AI MVP - 設定ファイル
このファイルでAIモデルの切り替えやデータベース設定を管理します
"""

import os
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# Firebase設定
FIREBASE_CONFIG = {
    "type": "service_account",
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY", "").replace('\\n', '\n'),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
}

# AIモデル設定（ここで切り替え可能）
AI_MODELS = {
    "primary": "gemini",  # メインで使用するAIモデル
    "secondary": "claude",  # サブで使用するAIモデル
    "models": {
        "gemini": {
            "api_key": os.getenv("GEMINI_API_KEY"),
            "model_name": "gemini-1.5-pro"
        },
        "claude": {
            "api_key": os.getenv("CLAUDE_API_KEY"),
            "model_name": "claude-3-sonnet-20240229"
        },
        "openai": {
            "api_key": os.getenv("OPENAI_API_KEY"),
            "model_name": "gpt-4"
        }
    }
}

# 外部サービス連携設定
EXTERNAL_SERVICES = {
    "slack": {
        "token": os.getenv("SLACK_TOKEN"),
        "enabled": True if os.getenv("SLACK_TOKEN") else False
    },
    "gmail": {
        "credentials": os.getenv("GMAIL_CREDENTIALS"),
        "enabled": True if os.getenv("GMAIL_CREDENTIALS") else False
    },
    "teams": {
        "client_id": os.getenv("TEAMS_CLIENT_ID"),
        "client_secret": os.getenv("TEAMS_CLIENT_SECRET"),
        "enabled": True if os.getenv("TEAMS_CLIENT_ID") else False
    }
}

# アプリケーション設定
APP_CONFIG = {
    "title": "BizFlow AI MVP",
    "version": "1.0.0",
    "debug": os.getenv("DEBUG", "False").lower() == "true",
    "secret_key": os.getenv("SECRET_KEY", "your-secret-key-here")
}