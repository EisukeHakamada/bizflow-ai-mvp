"""
BizFlow AI MVP - シンプル版
基本動作確認用
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
        st.metric("今日のタスク", "5件", "完了: 2件")
    
    with col2:
        st.metric("進行中プロジェクト", "3件", "今週締切: 1件")
    
    with col3:
        st.metric("未読メッセージ", "12件", "重要: 3件")
    
    st.markdown("---")
    
    # AI提案セクション
    st.markdown("### 🤖 AI提案: 今日の優先アクション")
    
    with st.expander("今日の推奨アクション", expanded=True):
        st.markdown("""
        **優先度: 高**
        - クライアントA向けプロポーザル完成 (期限: 明日)
        
        **優先度: 中** 
        - 週次チームミーティング準備 (期限: 明後日)
        
        **優先度: 低**
        - 新規案件の市場調査 (期限: 来週)
        """)
    
    if st.button("🔄 AI再計算"):
        st.success("優先度を再計算しました！")

def show_communication():
    """コミュニケーション表示"""
    st.title("💬 コミュニケーション管理")
    
    st.markdown("### 📨 メッセージ一覧")
    
    # サンプルメッセージ
    messages = [
        {"sender": "田中一郎", "subject": "【緊急】プレゼン資料確認", "time": "14:30", "priority": "🔴"},
        {"sender": "山田花子", "subject": "キャンペーン企画の件", "time": "13:15", "priority": "🟡"},
        {"sender": "佐藤次郎", "subject": "進捗報告", "time": "11:00", "priority": "🟢"}
    ]
    
    for msg in messages:
        with st.container():
            st.markdown(f"{msg['priority']} **{msg['subject']}** - {msg['sender']} ({msg['time']})")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("返信", key=f"reply_{msg['sender']}"):
                    st.success("返信機能は開発中です")
            with col2:
                if st.button("要約", key=f"summary_{msg['sender']}"):
                    st.info("AI要約機能は開発中です")
            with col3:
                if st.button("タスク化", key=f"task_{msg['sender']}"):
                    st.success("タスクを作成しました")
            
            st.markdown("---")

def show_tasks():
    """タスク管理表示"""
    st.title("✅ タスク管理")
    
    st.markdown("### 今日のタスク")
    
    tasks = [
        {"name": "プロポーザル作成", "priority": "🔴 高", "status": "進行中"},
        {"name": "ミーティング準備", "priority": "🟡 中", "status": "未着手"},
        {"name": "市場調査", "priority": "🟢 低", "status": "未着手"}
    ]
    
    for task in tasks:
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        
        with col1:
            st.write(task["name"])
        with col2:
            st.write(task["priority"])
        with col3:
            st.write(task["status"])
        with col4:
            if st.button("完了", key=f"complete_{task['name']}"):
                st.success(f"「{task['name']}」を完了しました！")

def show_projects():
    """プロジェクト管理表示"""
    st.title("📁 プロジェクト管理")
    
    st.markdown("### 進行中プロジェクト")
    
    projects = [
        {"name": "プロジェクトX", "progress": 65, "status": "順調"},
        {"name": "マーケティング戦略", "progress": 30, "status": "計画中"},
    ]
    
    for project in projects:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write(f"**{project['name']}**")
            st.progress(project['progress'] / 100, text=f"進捗: {project['progress']}%")
        
        with col2:
            st.write(f"状況: {project['status']}")

def main():
    """メインアプリケーション"""
    
    # 認証チェック
    if not simple_auth():
        return
    
    # サイドバー
    st.sidebar.title("🚀 BizFlow AI")
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