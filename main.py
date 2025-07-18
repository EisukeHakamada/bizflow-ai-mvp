"""
BizFlow AI MVP - メインアプリケーション（簡略版）
まずは基本動作を確認するための最小構成
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

# カスタムCSS（スマホ対応）
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
    
    /* ダッシュボード用のカード風デザイン */
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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

def show_simple_pages():
    """シンプルなページ表示"""
    st.sidebar.title("🚀 BizFlow AI")
    st.sidebar.markdown("---")
    
    # ナビゲーションメニュー
    page = st.sidebar.selectbox(
        "メニュー",
        ["📊 ダッシュボード", "✅ タスク管理", "📁 プロジェクト管理", "💬 コミュニケーション"],
        key="navigation"
    )
    
    if page == "📊 ダッシュボード":
        show_dashboard()
    elif page == "✅ タスク管理":
        st.title("✅ タスク管理")
        st.info("タスク管理機能は開発中です。近日公開予定！")
        st.markdown("### サンプルタスク")
        st.checkbox("プロポーザル作成")
        st.checkbox("ミーティング準備")
        st.checkbox("競合調査")
    elif page == "📁 プロジェクト管理":
        st.title("📁 プロジェクト管理")
        st.info("プロジェクト管理機能は開発中です。近日公開予定！")
        st.markdown("### 進行中のプロジェクト")
        st.write("- プロジェクトX (進捗: 65%)")
        st.write("- マーケティング戦略 (進捗: 30%)")
    elif page == "💬 コミュニケーション":
        st.title("💬 コミュニケーション")
        st.info("コミュニケーション機能は開発中です。近日公開予定！")
        st.markdown("### 未読メッセージ")
        st.write("- Slack: 5件")
        st.write("- Gmail: 7件")
    
    st.sidebar.markdown("---")
    if st.sidebar.button("ログアウト"):
        st.session_state.authenticated = False
        st.rerun()

def main():
    """メインアプリケーション"""
    
    # 認証チェック
    if not simple_auth():
        return
    
    # メインページ表示
    show_simple_pages()

if __name__ == "__main__":
    main()
    