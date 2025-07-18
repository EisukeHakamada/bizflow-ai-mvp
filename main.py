"""
BizFlow AI MVP - 修正されたメインアプリケーション
session_state navigation エラーを修正
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

# カスタムCSS（スマホ対応 + 新機能用）
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* スマホ対応 */
    @media (max-width: 768px) {
        .stApp {
            padding: 1rem 0.5rem;
        }
        
        .block-container {
            padding: 1rem;
        }
    }
    
    /* メッセージカード用のスタイル */
    .message-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .message-card.priority-high {
        border-left-color: #ff4444;
    }
    
    .message-card.priority-medium {
        border-left-color: #ffaa00;
    }
    
    .message-card.priority-low {
        border-left-color: #00aa00;
    }
    
    /* AI分析結果用のスタイル */
    .ai-analysis {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem;
        border-radius: 4px;
        margin: 0.5rem 0;
    }
    
    /* クイックアクションボタン */
    .quick-action {
        background: #4CAF50;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        cursor: pointer;
        margin: 0.2rem;
    }
    
    .quick-action:hover {
        background: #45a049;
    }
</style>
""", unsafe_allow_html=True)

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

def show_enhanced_dashboard():
    """強化されたダッシュボード"""
    st.title("📊 BizFlow AI ダッシュボード")
    
    # 今日の重要アクション（コミュニケーション重視）
    st.markdown("### ⚡ 今日の重要アクション")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🔴 緊急返信", "2件", "今すぐ対応")
    
    with col2:
        st.metric("💬 未読メッセージ", "12件", "+3件（1時間）")
    
    with col3:
        st.metric("✅ 完了タスク", "5件", "+2件（今日）")
    
    with col4:
        st.metric("🎯 進行中プロジェクト", "3件", "順調")
    
    st.markdown("---")
    
    # AI提案セクション（コミュニケーション中心）
    st.markdown("### 🤖 AI提案: 今すぐやるべきこと")
    
    # 緊急対応エリア
    with st.container():
        st.markdown("#### 🚨 緊急対応（今すぐ）")
        
        urgent_actions = [
            {
                "type": "返信",
                "title": "田中一郎さんからの【緊急】プレゼン資料確認",
                "ai_suggestion": "AI返信案を準備済み。「確認して修正版を送付」で即座に対応可能",
                "estimated_time": "2分",
                "action_button": "🚀 AI返信案を見る"
            },
            {
                "type": "確認",
                "title": "山田花子さんからのキャンペーン企画質問",
                "ai_suggestion": "3つの確認事項に対してAI回答案を生成済み",
                "estimated_time": "5分",
                "action_button": "📝 回答案を確認"
            }
        ]
        
        for action in urgent_actions:
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"**{action['title']}**")
                st.write(f"💡 {action['ai_suggestion']}")
            
            with col2:
                st.write(f"⏱️ 推定時間: {action['estimated_time']}")
                st.write(f"📋 種類: {action['type']}")
            
            with col3:
                if st.button(action['action_button'], key=f"urgent_{action['title'][:10]}"):
                    st.info("💬 コミュニケーションタブでAI返信機能をご確認ください！")
    
    st.markdown("---")
    
    # 今日の推奨スケジュール
    st.markdown("#### 📅 今日の推奨スケジュール（AI最適化済み）")
    
    with st.expander("本日のタイムライン", expanded=True):
        timeline = [
            {"time": "09:00", "task": "緊急返信対応（2件）", "status": "⚡ 即座", "ai_note": "AI返信案準備済み"},
            {"time": "09:30", "task": "プロジェクトX進捗確認", "status": "📊 重要", "ai_note": "関係者への自動更新通知"},
            {"time": "11:00", "task": "新規案件の市場調査", "status": "🔍 集中", "ai_note": "AI調査アシスト利用"},
            {"time": "14:00", "task": "残りメッセージ対応", "status": "💬 定常", "ai_note": "一括AI分析済み"},
            {"time": "16:00", "task": "明日の準備", "status": "📝 計画", "ai_note": "AI自動生成"}
        ]
        
        for item in timeline:
            col1, col2, col3, col4 = st.columns([1, 3, 1, 2])
            
            with col1:
                st.write(f"**{item['time']}**")
            with col2:
                st.write(item['task'])
            with col3:
                st.write(item['status'])
            with col4:
                st.write(f"🤖 {item['ai_note']}")
    
    # クイックアクション
    st.markdown("---")
    st.markdown("### ⚡ クイックアクション")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💬 AI返信生成", type="primary"):
            st.info("💬 コミュニケーションタブでAI返信機能をお試しください！")
    
    with col2:
        if st.button("📋 新規タスク"):
            st.info("✅ タスク管理タブで新規タスクを作成できます！")
    
    with col3:
        if st.button("🤖 AI相談"):
            st.info("💭 何でも聞いてください！「この案件、受けるべき？」「今日の優先順位は？」など")
    
    with col4:
        if st.button("📊 進捗レポート"):
            st.success("📈 週次レポートを自動生成中...")

def show_pages():
    """ページ表示管理"""
    st.sidebar.title("🚀 BizFlow AI")
    st.sidebar.markdown("---")
    
    # 緊急通知エリア
    if st.sidebar.button("🚨 緊急通知 (2件)", type="primary"):
        st.sidebar.error("🔴 田中一郎さんから緊急メッセージ")
        st.sidebar.warning("🟡 山田花子さんから重要な質問")
    
    st.sidebar.markdown("---")
    
    # ナビゲーションメニュー（修正: デフォルトページの設定）
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "📊 ダッシュボード"
    
    page = st.sidebar.selectbox(
        "メニュー",
        ["📊 ダッシュボード", "💬 コミュニケーション", "✅ タスク管理", "📁 プロジェクト管理"],
        index=["📊 ダッシュボード", "💬 コミュニケーション", "✅ タスク管理", "📁 プロジェクト管理"].index(st.session_state.current_page)
    )
    
    # ページが変更された場合の処理
    if page != st.session_state.current_page:
        st.session_state.current_page = page
        st.rerun()
    
    # AI設定エリア
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🤖 AI設定")
    
    ai_mode = st.sidebar.selectbox(
        "AIモード",
        ["自動化最大", "バランス", "手動確認"]
    )
    
    if ai_mode == "自動化最大":
        st.sidebar.success("🚀 返信案自動生成、優先度自動判定、タスク自動作成が有効")
    elif ai_mode == "バランス":
        st.sidebar.info("⚖️ 重要な判断のみユーザー確認")
    else:
        st.sidebar.warning("👤 全ての判断をユーザーが確認")
    
    st.sidebar.markdown("---")
    
    # 今日の進捗
    st.sidebar.markdown("### 📈 今日の進捗")
    st.sidebar.progress(0.6, text="完了率: 60%")
    st.sidebar.write("完了: 6タスク / 残り: 4タスク")
    
    st.sidebar.markdown("---")
    
    if st.sidebar.button("ログアウト"):
        st.session_state.authenticated = False
        st.rerun()
    
    # ページ表示
    if page == "📊 ダッシュボード":
        show_enhanced_dashboard()
    elif page == "💬 コミュニケーション":
        # 強化されたコミュニケーションページを読み込み
        try:
            from pages.communications_enhanced import show
            show()
        except ImportError:
            st.error("強化されたコミュニケーション機能の読み込みに失敗しました。")
            st.info("pages/communications_enhanced.pyファイルを確認してください。")
            # 基本機能表示
            show_basic_communication()
    elif page == "✅ タスク管理":
        show_task_management()
    elif page == "📁 プロジェクト管理":
        show_project_management()

def show_basic_communication():
    """基本的なコミュニケーション機能"""
    st.title("💬 コミュニケーション管理")
    st.info("強化された機能を読み込み中です...")
    
    st.markdown("### 📨 基本メッセージ一覧")
    
    # サンプルメッセージ
    messages = [
        {"sender": "田中一郎", "subject": "【緊急】プレゼン資料確認", "time": "14:30", "priority": "🔴"},
        {"sender": "山田花子", "subject": "キャンペーン企画の件", "time": "13:15", "priority": "🟡"},
        {"sender": "佐藤次郎", "subject": "進捗報告", "time": "11:00", "priority": "🟢"}
    ]
    
    for msg in messages:
        st.markdown(f"{msg['priority']} **{msg['subject']}** - {msg['sender']} ({msg['time']})")

def show_task_management():
    """タスク管理機能"""
    st.title("✅ タスク管理")
    
    st.markdown("### 今日のタスク（AI優先度順）")
    tasks = [
        {"name": "田中さんへの返信", "priority": "🔴 高", "ai_time": "2分", "status": "AI準備済み"},
        {"name": "プロジェクトX進捗確認", "priority": "🟡 中", "ai_time": "15分", "status": "自動化可能"},
        {"name": "市場調査レポート", "priority": "🟢 低", "ai_time": "2時間", "status": "AI支援可能"}
    ]
    
    for task in tasks:
        col1, col2, col3, col4 = st.columns([3, 1, 1, 2])
        with col1:
            st.write(task["name"])
        with col2:
            st.write(task["priority"])
        with col3:
            st.write(task["ai_time"])
        with col4:
            st.write(f"🤖 {task['status']}")
    
    # 新規タスク作成
    st.markdown("---")
    st.markdown("### 新規タスク作成")
    
    with st.form("new_task"):
        task_name = st.text_input("タスク名")
        task_priority = st.selectbox("優先度", ["高", "中", "低"])
        task_deadline = st.date_input("期限")
        
        if st.form_submit_button("タスク作成"):
            st.success(f"タスク「{task_name}」を作成しました！")

def show_project_management():
    """プロジェクト管理機能"""
    st.title("📁 プロジェクト管理")
    
    st.markdown("### 進行中プロジェクト")
    
    projects = [
        {"name": "プロジェクトX", "progress": 65, "deadline": "2025-09-01", "status": "順調"},
        {"name": "マーケティング戦略", "progress": 30, "deadline": "2025-12-31", "status": "計画中"},
        {"name": "業務効率化ツール", "progress": 100, "deadline": "2025-06-30", "status": "完了"}
    ]
    
    for project in projects:
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.write(f"**{project['name']}**")
            st.progress(project['progress'] / 100, text=f"進捗: {project['progress']}%")
        
        with col2:
            st.write(f"期限: {project['deadline']}")
        
        with col3:
            st.write(f"状況: {project['status']}")
    
    # 新規プロジェクト作成
    st.markdown("---")
    st.markdown("### 新規プロジェクト作成")
    
    with st.form("new_project"):
        project_name = st.text_input("プロジェクト名")
        project_description = st.text_area("概要")
        project_deadline = st.date_input("完了予定日")
        
        if st.form_submit_button("プロジェクト作成"):
            st.success(f"プロジェクト「{project_name}」を作成しました！")

def main():
    """メインアプリケーション"""
    
    # 認証チェック
    if not simple_auth():
        return
    
    # メインページ表示
    show_pages()

if __name__ == "__main__":
    main()