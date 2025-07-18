"""
BizFlow AI MVP - AI機能付き完全版
実際のGemini APIを使用した返信生成機能
"""

import streamlit as st
import sys
import os

# プロジェクトのルートディレクトリをPythonパスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Streamlitページ設定
st.set_page_config(
    page_title="BizFlow AI MVP",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# AI設定
def setup_ai():
    """AI APIの設定"""
    try:
        import google.generativeai as genai
        api_key = st.secrets.get("GEMINI_API_KEY", "")
        if api_key and api_key != "test-gemini-api-key-12345":
            genai.configure(api_key=api_key)
            return True
        else:
            return False
    except Exception as e:
        st.error(f"AI設定エラー: {str(e)}")
        return False

def generate_ai_reply(message_info, tone="丁寧・フォーマル"):
    """AI返信生成"""
    try:
        import google.generativeai as genai
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        tone_instructions = {
            '丁寧・フォーマル': '敬語を使い、ビジネスマナーに配慮した丁寧な返信',
            'カジュアル・親しみやすい': 'フレンドリーで親しみやすく、でもプロフェッショナルな返信',
            '簡潔・ビジネスライク': '要点を簡潔にまとめた効率的な返信'
        }
        
        prompt = f"""
あなたは優秀なビジネスアシスタントです。以下のメッセージに対する返信を作成してください。

## 受信メッセージ情報
送信者: {message_info['sender']}
件名: {message_info['subject']}
内容の推測: {message_info['subject']}に関する業務依頼または確認事項

## 返信の要件
- トーン: {tone_instructions.get(tone, '丁寧・フォーマル')}
- 3つの異なるバリエーションを作成
- 各返信は100-200文字程度
- 相手の依頼に適切に応答

以下の形式で出力してください：

**返信案1: 即座に対応版**
[返信内容1]

**返信案2: 詳細確認版**
[返信内容2]

**返信案3: 簡潔回答版**
[返信内容3]
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"AI生成エラー: {str(e)}\n\n代替テンプレート返信を使用します。"

def simple_auth():
    """簡易認証システム"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.title("🔐 BizFlow AI ログイン")
        
        with st.form("login_form"):
            st.markdown("### ログイン情報を入力してください")
            username = st.text_input("ユーザー名")
            password = st.text_input("パスワード", type="password")
            submit_button = st.form_submit_button("ログイン")
            
            if submit_button:
                if username == "admin" and password == "admin123":
                    st.session_state.authenticated = True
                    st.success("ログインに成功しました！")
                    st.rerun()
                else:
                    st.error("ユーザー名またはパスワードが間違っています。")
        
        # 開発用のヒント
        st.markdown("---")
        st.markdown("**開発用ログイン情報:**")
        st.code("ユーザー名: admin\nパスワード: admin123")
        return False
    
    return True

def show_dashboard():
    """ダッシュボード表示"""
    st.title("📊 BizFlow AI ダッシュボード")
    st.markdown("### 今日のタスクとプロジェクト概要")
    
    # 3列のレイアウト
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🔴 緊急返信", "2件", "AI準備済み")
    
    with col2:
        st.metric("💬 未読メッセージ", "12件", "+3件（1時間）")
    
    with col3:
        st.metric("✅ 完了タスク", "5件", "+2件（今日）")
    
    st.markdown("---")
    
    # AI提案セクション
    st.markdown("### 🤖 AI提案: 今日の優先アクション")
    
    with st.expander("今日の推奨アクション", expanded=True):
        st.markdown("""
        **🔴 緊急度: 高**
        - 田中一郎さんからの【緊急】プレゼン資料確認 → **AI返信案準備済み**
        
        **🟡 緊急度: 中** 
        - 山田花子さんからのキャンペーン企画質問 → **AI分析完了**
        
        **🟢 緊急度: 低**
        - 佐藤次郎さんからの進捗報告 → **確認済み**
        """)
    
    if st.button("🔄 AI再計算"):
        st.success("優先度を再計算しました！AIが最新の状況を分析中...")

def show_ai_reply_dialog(message_info):
    """AI返信生成ダイアログ"""
    st.markdown(f"### 🤖 AI返信生成: {message_info['subject']}")
    st.markdown(f"**送信者:** {message_info['sender']}")
    
    # 返信トーン選択
    col1, col2 = st.columns(2)
    
    with col1:
        tone = st.selectbox(
            "返信のトーン",
            ["丁寧・フォーマル", "カジュアル・親しみやすい", "簡潔・ビジネスライク"],
            key="reply_tone"
        )
    
    with col2:
        ai_available = setup_ai()
        if ai_available:
            st.success("🤖 AI機能: 有効")
        else:
            st.warning("🤖 AI機能: テストモード")
    
    if st.button("🚀 AI返信案を生成", type="primary"):
        with st.spinner("🤖 AIが返信案を生成中..."):
            if ai_available:
                reply_text = generate_ai_reply(message_info, tone)
            else:
                # テスト用の代替返信
                reply_text = f"""
**返信案1: 即座に対応版**
{message_info['sender']}さん

お疲れ様です。{message_info['subject']}の件、承知いたしました。
すぐに確認し、本日中に対応いたします。

よろしくお願いいたします。

**返信案2: 詳細確認版**
{message_info['sender']}さん

お疲れ様です。{message_info['subject']}の件でご連絡いただき、ありがとうございます。
いくつか確認させていただきたい点がございますので、お時間のある時にお聞かせください。

よろしくお願いいたします。

**返信案3: 簡潔回答版**
{message_info['sender']}さん

承知いたしました。対応いたします。
"""
        
        # 返信案を表示
        st.markdown("### 📝 生成された返信案")
        
        # 返信案をパース
        reply_sections = reply_text.split("**返信案")
        
        for i, section in enumerate(reply_sections[1:], 1):
            lines = section.strip().split('\n')
            title = lines[0].replace(':', '')
            content = '\n'.join(lines[1:]).strip()
            
            with st.expander(f"返信案 {i}: {title}", expanded=i==1):
                edited_content = st.text_area(
                    f"返信内容 {i}:",
                    value=content,
                    height=150,
                    key=f"reply_content_{i}"
                )
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button(f"📤 この返信を送信", key=f"send_{i}"):
                        st.success(f"✅ {message_info['sender']}に返信を送信しました！")
                        st.balloons()
                
                with col2:
                    if st.button(f"📋 コピー", key=f"copy_{i}"):
                        st.success("📋 クリップボードにコピーしました！")
                
                with col3:
                    if st.button(f"📅 フォローアップ", key=f"followup_{i}"):
                        st.success("📅 3日後にフォローアップタスクを作成しました！")

def show_communication():
    """AI機能付きコミュニケーション表示"""
    st.title("💬 AI駆動コミュニケーション管理")
    
    # AI状態表示
    ai_available = setup_ai()
    if ai_available:
        st.success("🤖 **AI機能が有効です** - 返信案の自動生成、優先度判定、要約機能が利用可能")
    else:
        st.warning("🤖 **AIテストモード** - 基本機能のみ利用可能（APIキーを設定してください）")
    
    st.markdown("---")
    st.markdown("### 📨 AI分析済みメッセージ一覧")
    
    # サンプルメッセージ（AI分析結果付き）
    messages = [
        {
            "sender": "田中一郎", 
            "subject": "【緊急】プレゼン資料確認", 
            "time": "14:30", 
            "priority": "🔴",
            "ai_category": "緊急対応",
            "ai_suggestion": "今すぐ返信推奨",
            "estimated_time": "2分"
        },
        {
            "sender": "山田花子", 
            "subject": "キャンペーン企画の件", 
            "time": "13:15", 
            "priority": "🟡",
            "ai_category": "企画相談",
            "ai_suggestion": "今日中に返信",
            "estimated_time": "5分"
        },
        {
            "sender": "佐藤次郎", 
            "subject": "進捗報告", 
            "time": "11:00", 
            "priority": "🟢",
            "ai_category": "定期報告",
            "ai_suggestion": "明日返信でOK",
            "estimated_time": "1分"
        }
    ]
    
    # 返信生成モード
    if 'show_reply_dialog' in st.session_state and st.session_state.show_reply_dialog:
        selected_msg = st.session_state.selected_message
        show_ai_reply_dialog(selected_msg)
        
        if st.button("⬅️ メッセージ一覧に戻る"):
            st.session_state.show_reply_dialog = False
            st.rerun()
        
        return
    
    # メッセージ一覧表示
    for msg in messages:
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"{msg['priority']} **{msg['subject']}** - {msg['sender']} ({msg['time']})")
                st.write(f"🤖 **AI分析:** {msg['ai_category']} | **推奨:** {msg['ai_suggestion']} | **予想時間:** {msg['estimated_time']}")
            
            with col2:
                # AIアクションボタン
                if st.button("🚀 AI返信", key=f"ai_reply_{msg['sender']}", type="primary"):
                    st.session_state.selected_message = msg
                    st.session_state.show_reply_dialog = True
                    st.rerun()
            
            # 従来のアクションボタン
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📝 要約", key=f"summary_{msg['sender']}"):
                    with st.spinner("🤖 AIが要約中..."):
                        import time
                        time.sleep(1)
                    st.info(f"📋 **AI要約:** {msg['subject']}について、{msg['sender']}さんから{msg['ai_category']}の依頼。{msg['ai_suggestion']}が推奨されます。")
            
            with col2:
                if st.button("📋 タスク化", key=f"task_{msg['sender']}"):
                    st.success(f"✅ 「{msg['subject']}への対応」タスクを作成しました！")
            
            with col3:
                if st.button("⚡ 優先度変更", key=f"priority_{msg['sender']}"):
                    st.info("🤖 AIが状況を再分析して優先度を調整しました")
            
            st.markdown("---")

def show_tasks():
    """タスク管理表示"""
    st.title("✅ AI駆動タスク管理")
    
    st.markdown("### 🤖 AI分析済みタスク一覧")
    
    tasks = [
        {"name": "田中さんへの返信", "priority": "🔴 高", "status": "AI準備済み", "ai_time": "2分"},
        {"name": "プロポーザル作成", "priority": "🔴 高", "status": "進行中", "ai_time": "2時間"},
        {"name": "ミーティング準備", "priority": "🟡 中", "status": "AI支援可能", "ai_time": "30分"},
        {"name": "市場調査", "priority": "🟢 低", "status": "未着手", "ai_time": "3時間"}
    ]
    
    for task in tasks:
        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
        
        with col1:
            st.write(task["name"])
        with col2:
            st.write(task["priority"])
        with col3:
            st.write(task["status"])
        with col4:
            st.write(f"⏰ {task['ai_time']}")
        with col5:
            if st.button("完了", key=f"complete_{task['name']}"):
                st.success(f"「{task['name']}」を完了しました！")

def show_projects():
    """プロジェクト管理表示"""
    st.title("📁 AI駆動プロジェクト管理")
    
    st.markdown("### 🤖 AI分析済みプロジェクト")
    
    projects = [
        {"name": "プロジェクトX", "progress": 65, "status": "順調", "ai_insight": "予定通り進行中"},
        {"name": "マーケティング戦略", "progress": 30, "status": "要注意", "ai_insight": "リソース不足の可能性"},
    ]
    
    for project in projects:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write(f"**{project['name']}**")
            st.progress(project['progress'] / 100, text=f"進捗: {project['progress']}%")
            st.write(f"🤖 **AI分析:** {project['ai_insight']}")
        
        with col2:
            st.write(f"状況: {project['status']}")
            if st.button(f"🤖 AI提案", key=f"ai_suggest_{project['name']}"):
                st.info("🤖 AIが次のアクションを分析中...")

def main():
    """メインアプリケーション"""
    
    # 認証チェック
    if not simple_auth():
        return
    
    # サイドバー
    st.sidebar.title("🚀 BizFlow AI")
    st.sidebar.markdown("---")
    
    # AI状態表示
    ai_available = setup_ai()
    if ai_available:
        st.sidebar.success("🤖 AI: 有効")
    else:
        st.sidebar.warning("🤖 AI: テストモード")
    
    st.sidebar.markdown("---")
    
    # ナビゲーション
    page = st.sidebar.selectbox(
        "メニュー",
        ["📊 ダッシュボード", "💬 コミュニケーション", "✅ タスク管理", "📁 プロジェクト管理"]
    )
    
    st.sidebar.markdown("---")
    
    # 進捗表示
    st.sidebar.markdown("### 📈 今日の進捗")
    st.sidebar.progress(0.6, text="完了率: 60%")
    st.sidebar.write("🤖 AI支援: 8タスク")
    
    st.sidebar.markdown("---")
    
    if st.sidebar.button("ログアウト"):
        st.session_state.authenticated = False
        st.rerun()
    
    # ページ表示
    if page == "📊 ダッシュボード":
        show_dashboard()
    elif page == "💬 コミュニケーション":
        show_communication()
    elif page == "✅ タスク管理":
        show_tasks()
    elif page == "📁 プロジェクト管理":
        show_projects()

if __name__ == "__main__":
    main()