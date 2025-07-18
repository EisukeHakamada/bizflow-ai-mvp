"""
BizFlow AI MVP - ダッシュボードページ
"""

import streamlit as st
from utils.database import get_user_data
from datetime import datetime, timedelta
import pandas as pd

def show():
    """ダッシュボードページの表示"""
    
    st.title("📊 BizFlow AI ダッシュボード")
    st.markdown("### 今日のタスクとプロジェクト概要")
    
    # データベースから情報を取得
    db = st.session_state.db
    user_id = st.session_state.get('username', 'admin')
    
    # 3列のレイアウト
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📋 今日のタスク</h3>
            <h2 style="color: #1f77b4;">5件</h2>
            <p>完了: 2件 | 残り: 3件</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🚀 進行中プロジェクト</h3>
            <h2 style="color: #ff7f0e;">3件</h2>
            <p>今週締切: 1件</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>💬 未読メッセージ</h3>
            <h2 style="color: #d62728;">12件</h2>
            <p>重要: 3件</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # AI提案セクション
    st.markdown("### 🤖 AI提案: 今日の優先アクション")
    
    with st.expander("今日の推奨アクション", expanded=True):
        ai_suggestions = [
            {
                "priority": "高",
                "task": "クライアントA向けプロポーザル完成",
                "action": "最終レビューと送信準備",
                "reason": "明日が提出期限のため最優先",
                "time_estimate": "2時間"
            },
            {
                "priority": "中",
                "task": "週次チームミーティング準備",
                "action": "アジェンダ作成とスライド準備",
                "reason": "明後日のミーティングで必要",
                "time_estimate": "1時間"
            },
            {
                "priority": "低",
                "task": "新規案件の市場調査",
                "action": "競合分析の開始",
                "reason": "来週までに完了予定",
                "time_estimate": "3時間"
            }
        ]
        
        for i, suggestion in enumerate(ai_suggestions):
            priority_class = f"priority-{suggestion['priority'].lower()}"
            if suggestion['priority'] == '高':
                priority_class = "priority-high"
            elif suggestion['priority'] == '中':
                priority_class = "priority-medium"
            else:
                priority_class = "priority-low"
            
            st.markdown(f"""
            <div class="metric-card {priority_class}">
                <h4>優先度: {suggestion['priority']} | 予想時間: {suggestion['time_estimate']}</h4>
                <h5>📋 {suggestion['task']}</h5>
                <p><strong>次のアクション:</strong> {suggestion['action']}</p>
                <p><strong>理由:</strong> {suggestion['reason']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # 再計算ボタン
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🔄 AI再計算"):
            st.success("優先度を再計算しました！")
            st.rerun()
    
    st.markdown("---")
    
    # 今日のスケジュール
    st.markdown("### 📅 今日のスケジュール")
    
    # サンプルスケジュール
    schedule_data = {
        "時間": ["09:00", "10:30", "14:00", "16:00"],
        "予定": [
            "チームミーティング",
            "クライアントA打ち合わせ",
            "プロポーザル作成",
            "メール返信・雑務"
        ],
        "ステータス": ["完了", "進行中", "未着手", "未着手"]
    }
    
    df = pd.DataFrame(schedule_data)
    st.dataframe(df, use_container_width=True)
    
    # 最近のアクティビティ
    st.markdown("### 📈 最近のアクティビティ")
    
    activities = [
        "✅ プロジェクトBの企画書を完成",
        "💬 Slackで新規案件の相談を受信",
        "📝 タスク「競合分析」を作成",
        "🤖 AIによる優先度提案を実行"
    ]
    
    for activity in activities:
        st.markdown(f"- {activity}")
    
    # クイックアクションボタン
    st.markdown("---")
    st.markdown("### ⚡ クイックアクション")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📝 新規タスク"):
            st.session_state.navigation = "✅ タスク管理"
            st.rerun()
    
    with col2:
        if st.button("📁 新規プロジェクト"):
            st.session_state.navigation = "📁 プロジェクト管理"
            st.rerun()
    
    with col3:
        if st.button("💬 メッセージ確認"):
            st.session_state.navigation = "💬 コミュニケーション"
            st.rerun()
    
    with col4:
        if st.button("🤖 AI相談"):
            st.info("AI相談機能は開発中です")