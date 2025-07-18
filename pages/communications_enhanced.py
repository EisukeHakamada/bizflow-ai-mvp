"""
BizFlow AI MVP - 強化されたコミュニケーション管理ページ
"""

import streamlit as st
from datetime import datetime, timedelta
from utils.ai_communication import AICommunicationHelper
import json

def show():
    """強化されたコミュニケーション管理ページの表示"""
    
    st.title("💬 コミュニケーション管理")
    
    # AI通信ヘルパーを初期化
    if 'ai_comm_helper' not in st.session_state:
        st.session_state.ai_comm_helper = AICommunicationHelper()
    
    # タブ分け
    tab1, tab2, tab3 = st.tabs(["📨 メッセージ一覧", "🤖 AI返信生成", "⚙️ 通知設定"])
    
    with tab1:
        show_enhanced_message_list()
    
    with tab2:
        show_ai_reply_generator()
    
    with tab3:
        show_notification_settings()

def show_enhanced_message_list():
    """強化されたメッセージ一覧の表示"""
    
    st.markdown("### 📨 統合メッセージ一覧")
    
    # 今日の重要アクション表示
    with st.container():
        st.markdown("#### ⚡ 今日の重要アクション")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🔴 緊急対応", "2件", "+1件")
        with col2:
            st.metric("🟡 今日返信", "5件", "-2件") 
        with col3:
            st.metric("🟢 週内対応", "8件", "+3件")
    
    st.markdown("---")
    
    # フィルタリングオプション
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        priority_filter = st.selectbox("重要度", ["全て", "高", "中", "低"])
    
    with col2:
        source_filter = st.selectbox("送信元", ["全て", "Slack", "Teams", "Gmail", "Chatwork"])
    
    with col3:
        status_filter = st.selectbox("ステータス", ["全て", "未読", "AI分析済み", "返信済み", "フォローアップ予定"])
    
    with col4:
        time_filter = st.selectbox("期間", ["今日", "昨日", "今週", "全期間"])
    
    # 一括操作ボタン
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🔄 メッセージ更新"):
            st.success("メッセージを更新しました")
    with col2:
        if st.button("🤖 AI一括分析"):
            with st.spinner("AIが全メッセージを分析中..."):
                import time
                time.sleep(2)
            st.success("AI分析完了！返信案を準備しました")
    with col3:
        if st.button("📧 重要分のみ表示"):
            st.info("重要度「高」のメッセージのみ表示中")
    with col4:
        if st.button("⚡ 緊急対応リスト"):
            st.info("今日中対応が必要なメッセージを表示中")
    
    st.markdown("---")
    
    # サンプルメッセージデータ（AI分析結果付き）
    enhanced_messages = [
        {
            "id": "msg_1",
            "source": "Gmail",
            "sender": "田中一郎 (ABC商事)",
            "subject": "【緊急】明日のプレゼン資料について",
            "preview": "お疲れ様です。明日15時からのプレゼンの件で、資料の最終確認をお願いします。特に価格設定の部分で...",
            "timestamp": "2025-07-18 14:30",
            "ai_priority": "高",
            "ai_category": "緊急対応",
            "ai_suggested_timing": "今すぐ",
            "ai_reply_ready": True,
            "estimated_reply_time": "2分",
            "followup_needed": True
        },
        {
            "id": "msg_2", 
            "source": "Slack",
            "sender": "山田花子 (マーケティング)",
            "subject": "来週のキャンペーン企画",
            "preview": "来週のキャンペーンの件、いくつか確認事項があります。1. ターゲット層の絞り込み 2. 予算配分 3. KPI設定...",
            "timestamp": "2025-07-18 13:15",
            "ai_priority": "中",
            "ai_category": "企画相談",
            "ai_suggested_timing": "今日中",
            "ai_reply_ready": True,
            "estimated_reply_time": "5分",
            "followup_needed": True
        },
        {
            "id": "msg_3",
            "source": "Teams",
            "sender": "佐藤次郎 (開発チーム)",
            "subject": "システム更新の進捗報告",
            "preview": "システム更新の進捗です。現在80%完了しており、予定通り今週末には完了予定です。テスト環境での...",
            "timestamp": "2025-07-18 11:00",
            "ai_priority": "低",
            "ai_category": "進捗報告",
            "ai_suggested_timing": "明日",
            "ai_reply_ready": True,
            "estimated_reply_time": "1分",
            "followup_needed": False
        }
    ]
    
    # メッセージ表示
    for message in enhanced_messages:
        # フィルタリング
        if priority_filter != "全て" and message["ai_priority"] != priority_filter:
            continue
        if source_filter != "全て" and message["source"] != source_filter:
            continue
        
        # 重要度に応じたスタイル
        priority_colors = {"高": "🔴", "中": "🟡", "低": "🟢"}
        source_icons = {"Slack": "💬", "Teams": "👥", "Gmail": "📧", "Chatwork": "💼"}
        
        # カード表示
        with st.container():
            # ヘッダー部分
            col1, col2, col3 = st.columns([6, 2, 2])
            
            with col1:
                st.markdown(f"### {priority_colors[message['ai_priority']]} {source_icons[message['source']]} {message['subject']}")
                st.markdown(f"**送信者:** {message['sender']} | **受信:** {message['timestamp']}")
            
            with col2:
                # AI分析結果
                st.markdown("**🤖 AI分析**")
                st.write(f"**重要度:** {message['ai_priority']}")
                st.write(f"**カテゴリ:** {message['ai_category']}")
                st.write(f"**推奨タイミング:** {message['ai_suggested_timing']}")
            
            with col3:
                # クイックアクション
                st.markdown("**⚡ クイックアクション**")
                if message['ai_reply_ready']:
                    if st.button(f"🚀 即座に返信", key=f"quick_reply_{message['id']}"):
                        st.session_state.selected_message_for_reply = message
                        st.success("AI返信生成タブに移動してください")
                
                if st.button(f"📝 編集して返信", key=f"edit_reply_{message['id']}"):
                    st.session_state.selected_message_for_reply = message
                    st.info("返信を編集できます")
            
            # メッセージ内容
            with st.expander("📖 メッセージ内容を表示", expanded=False):
                st.write(f"**内容:** {message['preview']}")
                
                # 詳細情報
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**AI推定返信時間:** {message['estimated_reply_time']}")
                    st.write(f"**フォローアップ必要:** {'はい' if message['followup_needed'] else 'いいえ'}")
                
                with col2:
                    # アクションボタン
                    if st.button("🔄 AI再分析", key=f"reanalyze_{message['id']}"):
                        st.success("AI分析を更新しました")
                    
                    if st.button("📋 タスク化", key=f"taskify_{message['id']}"):
                        create_task_from_message(message)
            
            st.markdown("---")

def show_ai_reply_generator():
    """AI返信生成機能"""
    
    st.markdown("### 🤖 AI返信生成")
    
    # メッセージ選択
    if 'selected_message_for_reply' not in st.session_state:
        st.info("メッセージ一覧から返信したいメッセージを選択してください。")
        
        # デモ用メッセージ選択
        st.markdown("#### または、デモ用メッセージで試してみる")
        demo_messages = [
            "【緊急】明日のプレゼン資料について - 田中一郎",
            "来週のキャンペーン企画 - 山田花子", 
            "システム更新の進捗報告 - 佐藤次郎"
        ]
        
        selected_demo = st.selectbox("デモメッセージを選択", ["選択してください"] + demo_messages)
        
        if selected_demo != "選択してください":
            # デモメッセージのデータを設定
            demo_message_data = {
                "sender": selected_demo.split(" - ")[1],
                "subject": selected_demo.split(" - ")[0],
                "preview": f"{selected_demo.split(' - ')[0]}に関する詳細な内容です。...",
                "source": "Gmail"
            }
            st.session_state.selected_message_for_reply = demo_message_data
        else:
            return
    
    message = st.session_state.selected_message_for_reply
    
    # 選択されたメッセージ表示
    st.markdown(f"**返信対象:** {message['subject']}")
    st.markdown(f"**送信者:** {message['sender']}")
    st.markdown(f"**送信元:** {message['source']}")
    
    # AI分析結果表示
    ai_helper = st.session_state.ai_comm_helper
    priority = ai_helper.analyze_message_priority(message)
    timing_suggestions = ai_helper.suggest_reply_timing(message)
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"🤖 **AI分析結果**\n重要度: {priority}")
    with col2:
        st.info(f"⏰ **推奨返信タイミング**\n{timing_suggestions[0]['timing']} - {timing_suggestions[0]['reason']}")
    
    # 元メッセージの表示
    with st.expander("📖 元メッセージ内容", expanded=False):
        st.write(message['preview'])
    
    st.markdown("---")
    
    # 返信設定
    st.markdown("#### 🎛️ 返信設定")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        reply_tone = st.selectbox(
            "返信のトーン",
            ["丁寧・フォーマル", "カジュアル・親しみやすい", "簡潔・ビジネスライク"]
        )
    
    with col2:
        reply_urgency = st.selectbox(
            "返信の緊急度",
            ["今すぐ返信", "今日中に返信", "明日以降に返信"]
        )
    
    with col3:
        include_followup = st.checkbox("フォローアップを含める", value=True)
    
    # 追加指示
    custom_instructions = st.text_area(
        "追加の指示（オプション）",
        placeholder="例: 来週の会議日程を提案してください、技術的な詳細は避けてください など"
    )
    
    # AI返信生成ボタン
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("🤖 AI返信案を生成", type="primary"):
            generate_and_display_replies(message, reply_tone, custom_instructions, ai_helper)
    
    with col2:
        if st.button("📋 返信をタスク化"):
            st.success("返信タスクを作成しました！タスク管理ページで確認できます。")

def generate_and_display_replies(message, tone, instructions, ai_helper):
    """AI返信案の生成と表示"""
    
    with st.spinner("🤖 AIが返信案を生成中..."):
        import time
        time.sleep(2)  # 生成時間をシミュレート
    
    # AI返信案生成
    reply_suggestions = ai_helper.generate_reply_suggestions(message, tone, instructions)
    
    if not reply_suggestions:
        st.error("返信案の生成に失敗しました。テンプレート返信を表示します。")
        return
    
    st.markdown("### 📝 生成された返信案")
    st.success("🎉 AI返信案が生成されました！選択して送信または編集してください。")
    
    for i, reply in enumerate(reply_suggestions, 1):
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"#### 返信案 {i}: {reply['version']}")
                
                # 編集可能なテキストエリア
                edited_content = st.text_area(
                    f"返信内容 {i}:",
                    value=reply['content'],
                    height=120,
                    key=f"reply_edit_{i}"
                )
            
            with col2:
                st.markdown("#### アクション")
                
                # 送信ボタン
                if st.button(f"📤 この返信を送信", key=f"send_{i}", type="primary"):
                    send_reply(message, edited_content)
                
                # コピーボタン  
                if st.button(f"📋 コピー", key=f"copy_{i}"):
                    st.success("クリップボードにコピーしました！")
                
                # お気に入りボタン
                if st.button(f"⭐ テンプレート保存", key=f"fav_{i}"):
                    st.success("テンプレートとして保存しました！")
            
            st.markdown("---")

def show_notification_settings():
    """通知設定"""
    
    st.markdown("### ⚙️ 通知・自動化設定")
    
    # 基本設定
    st.markdown("#### 📱 基本通知設定")
    
    col1, col2 = st.columns(2)
    
    with col1:
        enable_notifications = st.checkbox("プッシュ通知を有効化", value=True)
        urgent_only = st.checkbox("緊急メッセージのみ通知", value=False)
        quiet_hours = st.checkbox("静音時間を設定", value=True)
    
    with col2:
        if quiet_hours:
            st.time_input("静音開始時間", value=datetime.strptime("22:00", "%H:%M").time())
            st.time_input("静音終了時間", value=datetime.strptime("08:00", "%H:%M").time())
    
    st.markdown("---")
    
    # AI自動化設定
    st.markdown("#### 🤖 AI自動化設定")
    
    col1, col2 = st.columns(2)
    
    with col1:
        auto_analysis = st.checkbox("メッセージ受信時にAI自動分析", value=True)
        auto_reply_draft = st.checkbox("返信案の自動生成", value=True)
        auto_priority = st.checkbox("重要度の自動判定", value=True)
    
    with col2:
        auto_categorize = st.checkbox("カテゴリの自動分類", value=True)
        auto_followup = st.checkbox("フォローアップの自動設定", value=False)
        auto_task_creation = st.checkbox("タスクの自動作成", value=False)
    
    st.