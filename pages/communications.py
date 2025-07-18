"""
BizFlow AI MVP - コミュニケーション管理ページ
"""

import streamlit as st
from datetime import datetime, timedelta

def show():
    """コミュニケーション管理ページの表示"""
    
    st.title("💬 コミュニケーション管理")
    
    # タブ分け
    tab1, tab2, tab3 = st.tabs(["📨 メッセージ一覧", "🤖 AI返信生成", "⚙️ 連携設定"])
    
    with tab1:
        show_message_list()
    
    with tab2:
        show_ai_reply_generator()
    
    with tab3:
        show_integration_settings()

def show_message_list():
    """メッセージ一覧の表示"""
    
    st.markdown("### 📨 統合メッセージ一覧")
    
    # フィルタリングオプション
    col1, col2, col3 = st.columns(3)
    
    with col1:
        source_filter = st.selectbox(
            "送信元",
            ["全て", "Slack", "Teams", "Gmail", "Chatwork"]
        )
    
    with col2:
        status_filter = st.selectbox(
            "ステータス",
            ["全て", "未読", "重要", "返信済み", "アーカイブ"]
        )
    
    with col3:
        date_filter = st.selectbox(
            "期間",
            ["今日", "昨日", "今週", "先週", "全期間"]
        )
    
    # 一括操作ボタン
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 メッセージ更新"):
            st.success("メッセージを更新しました")
    with col2:
        if st.button("📧 一括既読"):
            st.success("表示中のメッセージを既読にしました")
    with col3:
        if st.button("🤖 重要度再分析"):
            with st.spinner("AIが重要度を分析中..."):
                import time
                time.sleep(2)
            st.success("重要度を更新しました")
    
    st.markdown("---")
    
    # サンプルメッセージデータ
    sample_messages = [
        {
            "id": "msg_1",
            "source": "Slack",
            "sender": "田中さん (開発チーム)",
            "subject": "プロジェクトXのAPI仕様について",
            "preview": "お疲れ様です。API仕様の件でご相談があります。認証部分の実装方針について...",
            "timestamp": "2025-07-17 14:30",
            "status": "未読",
            "importance": "高",
            "thread_count": 3,
            "channel": "#project-x"
        },
        {
            "id": "msg_2",
            "source": "Gmail",
            "sender": "client@example.com",
            "subject": "提案書についてのフィードバック",
            "preview": "先日お送りいただいた提案書を拝見いたしました。いくつか質問がございまして...",
            "timestamp": "2025-07-17 10:15",
            "status": "重要",
            "importance": "高",
            "thread_count": 1,
            "channel": "メール"
        },
        {
            "id": "msg_3",
            "source": "Teams",
            "sender": "山田さん (営業部)",
            "subject": "来週のクライアント打ち合わせ",
            "preview": "来週火曜日のクライアント打ち合わせの件でご相談です。議題の追加をお願いしたく...",
            "timestamp": "2025-07-17 09:45",
            "status": "未読",
            "importance": "中",
            "thread_count": 2,
            "channel": "営業チーム"
        },
        {
            "id": "msg_4",
            "source": "Chatwork",
            "sender": "佐藤さん (デザイン)",
            "subject": "UI/UXデザインのレビュー依頼",
            "preview": "新機能のデザインが完成しました。お時間のある時にレビューをお願いします...",
            "timestamp": "2025-07-16 16:20",
            "status": "返信済み",
            "importance": "中",
            "thread_count": 5,
            "channel": "デザインチーム"
        },
        {
            "id": "msg_5",
            "source": "Gmail",
            "sender": "support@service.com",
            "subject": "月次レポートの送付",
            "preview": "いつもお世話になっております。6月分の月次レポートをお送りいたします...",
            "timestamp": "2025-07-16 12:00",
            "status": "アーカイブ",
            "importance": "低",
            "thread_count": 1,
            "channel": "メール"
        }
    ]
    
    # メッセージ表示
    for message in sample_messages:
        # フィルタリング
        if source_filter != "全て" and message["source"] != source_filter:
            continue
        if status_filter != "全て" and message["status"] != status_filter:
            continue
        
        # 重要度と送信元に応じたアイコン
        importance_icon = {"高": "🔴", "中": "🟡", "低": "🟢"}
        source_icon = {"Slack": "💬", "Teams": "👥", "Gmail": "📧", "Chatwork": "💼"}
        status_icon = {"未読": "🔵", "重要": "⭐", "返信済み": "✅", "アーカイブ": "📁"}
        
        with st.expander(f"{importance_icon[message['importance']]} {source_icon[message['source']]} {status_icon[message['status']]} {message['subject']}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**送信者:** {message['sender']}")
                st.write(f"**チャンネル/場所:** {message['channel']}")
                st.write(f"**受信日時:** {message['timestamp']}")
                st.write(f"**メッセージ概要:**")
                st.write(message['preview'])
                
                if message['thread_count'] > 1:
                    st.write(f"**スレッド:** {message['thread_count']}件のメッセージ")
            
            with col2:
                st.write(f"**送信元:** {message['source']}")
                st.write(f"**重要度:** {message['importance']}")
                st.write(f"**ステータス:** {message['status']}")
            
            # アクションボタン
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("返信", key=f"reply_{message['id']}"):
                    st.session_state.selected_message = message
                    st.success("AI返信生成タブに移動してください")
            
            with col2:
                if st.button("🤖 要約", key=f"summary_{message['id']}"):
                    show_ai_summary(message)
            
            with col3:
                if st.button("📋 タスク化", key=f"task_{message['id']}"):
                    create_task_from_message(message)
            
            with col4:
                if message['status'] == "未読":
                    if st.button("既読", key=f"read_{message['id']}"):
                        st.success("既読にしました")
                else:
                    if st.button("未読", key=f"unread_{message['id']}"):
                        st.info("未読にしました")

def show_ai_reply_generator():
    """AI返信生成"""
    
    st.markdown("### 🤖 AI返信生成")
    
    # メッセージ選択
    if 'selected_message' not in st.session_state:
        st.info("メッセージ一覧から返信したいメッセージを選択してください。")
        return
    
    message = st.session_state.selected_message
    
    st.markdown(f"**返信対象:** {message['subject']}")
    st.markdown(f"**送信者:** {message['sender']}")
    st.markdown(f"**送信元:** {message['source']}")
    
    # 元メッセージの表示
    with st.expander("元メッセージ内容", expanded=True):
        st.write(message['preview'])
    
    st.markdown("---")
    
    # 返信設定
    col1, col2 = st.columns(2)
    
    with col1:
        reply_tone = st.selectbox(
            "返信のトーン",
            ["丁寧・フォーマル", "親しみやすい", "簡潔・ビジネスライク", "カスタム"]
        )
        
        reply_intent = st.selectbox(
            "返信の意図",
            ["情報提供", "質問への回答", "依頼の承諾", "依頼の辞退", "確認・質問", "お礼", "謝罪"]
        )
    
    with col2:
        ai_model = st.selectbox(
            "使用するAIモデル",
            ["Gemini", "Claude", "GPT-4"]
        )
        
        include_context = st.checkbox("プロジェクト文脈を含める", value=True)
    
    # カスタム指示
    custom_instructions = st.text_area(
        "追加の指示（オプション）",
        placeholder="例: 来週の会議日程を提案してください、技術的な詳細は避けてください など"
    )
    
    # AI返信生成ボタン
    if st.button("🤖 AI返信を生成"):
        with st.spinner(f"{ai_model}が返信を生成中..."):
            import time
            time.sleep(2)
        
        # 生成された返信案
        reply_drafts = generate_reply_drafts(message, reply_tone, reply_intent, custom_instructions)
        
        st.markdown("### 📝 生成された返信案")
        
        for i, draft in enumerate(reply_drafts, 1):
            with st.expander(f"返信案 {i}: {draft['style']}", expanded=i==1):
                st.text_area(
                    f"返信内容 {i}:",
                    value=draft['content'],
                    height=150,
                    key=f"draft_{i}"
                )
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button(f"この返信を使用", key=f"use_draft_{i}"):
                        st.success("返信内容をクリップボードにコピーしました！")
                
                with col2:
                    if st.button(f"編集", key=f"edit_draft_{i}"):
                        st.info("編集機能は開発中です")
                
                with col3:
                    if st.button(f"送信", key=f"send_draft_{i}"):
                        send_reply(message, draft['content'])

def show_integration_settings():
    """外部サービス連携設定"""
    
    st.markdown("### ⚙️ 外部サービス連携設定")
    
    # 各サービスの設定状況
    services = [
        {"name": "Slack", "status": "接続済み", "icon": "💬", "last_sync": "2025-07-17 15:00"},
        {"name": "Microsoft Teams", "status": "未接続", "icon": "👥", "last_sync": "-"},
        {"name": "Gmail", "status": "接続済み", "icon": "📧", "last_sync": "2025-07-17 14:45"},
        {"name": "Chatwork", "status": "接続済み", "icon": "💼", "last_sync": "2025-07-17 14:30"}
    ]
    
    for service in services:
        with st.expander(f"{service['icon']} {service['name']} - {service['status']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**ステータス:** {service['status']}")
                st.write(f"**最終同期:** {service['last_sync']}")
            
            with col2:
                if service['status'] == "接続済み":
                    if st.button(f"設定変更", key=f"config_{service['name']}"):
                        show_service_config(service['name'])
                    if st.button(f"接続解除", key=f"disconnect_{service['name']}"):
                        st.warning(f"{service['name']}の接続を解除しました")
                else:
                    if st.button(f"接続設定", key=f"connect_{service['name']}"):
                        show_connection_setup(service['name'])
    
    st.markdown("---")
    
    # AI設定
    st.markdown("### 🤖 AI分析設定")
    
    col1, col2 = st.columns(2)
    
    with col1:
        auto_importance = st.checkbox("重要度の自動判定", value=True)
        auto_summary = st.checkbox("長文メッセージの自動要約", value=True)
        auto_task_extract = st.checkbox("タスクの自動抽出", value=False)
    
    with col2:
        notification_threshold = st.selectbox(
            "通知する重要度",
            ["高のみ", "中以上", "全て"]
        )
        
        batch_processing = st.selectbox(
            "AI処理のタイミング",
            ["リアルタイム", "5分毎", "15分毎", "1時間毎"]
        )
    
    if st.button("設定を保存"):
        st.success("設定を保存しました！")

def generate_reply_drafts(message, tone, intent, custom_instructions):
    """返信案を生成（サンプル実装）"""
    
    # サンプルの返信案
    drafts = [
        {
            "style": "丁寧・詳細版",
            "content": f"""お疲れ様です。

{message['subject']}の件について、ご連絡いただきありがとうございます。

内容を確認いたしました。こちらの件については、以下のように対応させていただきます：

1. 詳細な検討を行い、来週までに回答いたします
2. 必要に応じてチームメンバーと相談いたします
3. 追加で確認が必要な点があれば、改めてご連絡いたします

何かご不明な点がございましたら、お気軽にお声かけください。

よろしくお願いいたします。"""
        },
        {
            "style": "簡潔・ビジネス版",
            "content": f"""お疲れ様です。

{message['subject']}の件、承知いたしました。

来週までに詳細を検討し、回答いたします。
追加で確認事項があれば改めて連絡いたします。

よろしくお願いいたします。"""
        },
        {
            "style": "親しみやすい版",
            "content": f"""お疲れ様です！

{message['subject']}の件、確認しました。

いくつか検討したい点があるので、来週中には返事させてください。
何か急ぎの件があれば、いつでも声をかけてくださいね。

ありがとうございます！"""
        }
    ]
    
    return drafts

def show_ai_summary(message):
    """AIによるメッセージ要約"""
    
    with st.spinner("AIがメッセージを要約中..."):
        import time
        time.sleep(1)
    
    summary_result = f"""
    **📋 メッセージ要約:**
    {message['sender']}から{message['subject']}について連絡。
    
    **🎯 求められていること:**
    - 技術仕様の確認と回答
    - 来週までの対応
    
    **⏰ 対応期限:**
    来週金曜日まで
    
    **💡 推奨アクション:**
    1. チームメンバーと技術的な点を相談
    2. 詳細な回答を準備
    3. 期限までに返信
    """
    
    st.success(summary_result)

def create_task_from_message(message):
    """メッセージからタスクを作成"""
    
    st.success(f"""
    📋 **新規タスクを作成しました:**
    
    **タスク名:** {message['subject']}への対応
    **担当事業:** 自動判定中...
    **期限:** 来週金曜日
    **優先度:** {message['importance']}
    **メモ:** {message['sender']}からの{message['source']}メッセージに対応
    
    タスク管理ページで詳細を確認できます。
    """)

def show_service_config(service_name):
    """サービス設定画面"""
    st.info(f"{service_name}の詳細設定は開発中です。")

def show_connection_setup(service_name):
    """接続設定画面"""
    st.info(f"{service_name}の接続設定は開発中です。")

def send_reply(message, content):
    """返信送信"""
    st.success(f"{message['source']}に返信を送信しました！")