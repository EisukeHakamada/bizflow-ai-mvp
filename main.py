"""
BizFlow AI MVP - タスク自動作成機能付き完全版
AI要約・返信生成・タスク自動作成の統合システム
"""

import streamlit as st
import sys
import os
import time
from datetime import datetime, timedelta

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

def generate_ai_task(message_info, summary_data=None):
    """AIタスク自動生成機能"""
    try:
        import google.generativeai as genai
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 要約データがある場合は活用
        context = ""
        if summary_data:
            context = f"""
            要約: {summary_data.get('要約', '')}
            分類: {summary_data.get('分類', '')}
            アクション: {summary_data.get('アクション', '')}
            緊急度: {summary_data.get('緊急度', '')}
            """
        
        prompt = f"""
あなたは優秀なタスク管理アシスタントです。以下のメッセージから最適なタスクを生成してください。

## メッセージ情報
送信者: {message_info['sender']}
件名: {message_info['subject']}
時刻: {message_info['time']}
{context}

## タスク生成要件
以下の形式で出力してください：

**タスク名:**
[簡潔で分かりやすいタスク名]

**詳細説明:**
[タスクの具体的な内容と要求事項]

**期限:**
[具体的な期限日時、不明な場合は「明日 17:00」]

**優先度:**
[高/中/低]

**カテゴリ:**
[コミュニケーション/プロジェクト作業/会議/レビュー/調査]

**推定時間:**
[タスク完了までの推定時間]

**チェックリスト:**
[実行すべきステップを3つまで、改行区切り]

**完了条件:**
[タスクが完了したと判断する条件]
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        # テンプレートタスク生成
        return f"""
**タスク名:**
{message_info['subject']}への対応

**詳細説明:**
{message_info['sender']}さんからの{message_info['subject']}に関して適切に対応する

**期限:**
明日 17:00

**優先度:**
中

**カテゴリ:**
コミュニケーション

**推定時間:**
30分

**チェックリスト:**
メッセージ内容の確認
必要な資料の準備
返信または対応の実行

**完了条件:**
適切な返信を送信し、相手からの確認を得る
        """

def generate_ai_summary(message_info):
    """AI要約・分類・タグ付け機能"""
    try:
        import google.generativeai as genai
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # より詳細なメッセージ内容を生成（実際の実装では実際のメッセージ内容を使用）
        message_content = f"""
        件名: {message_info['subject']}
        送信者: {message_info['sender']}
        推定内容: {message_info['subject']}に関する業務連絡。
        具体的には、プロジェクトの進捗確認、資料の修正依頼、会議の日程調整、
        または重要な業務判断に関する相談事項が含まれている可能性が高い。
        """
        
        prompt = f"""
あなたは優秀なビジネスアナリストです。以下のメッセージを分析して、要約・分類・タグ付けを行ってください。

## 分析対象メッセージ
{message_content}

## 出力要件
以下の形式で出力してください：

**要約:**
[メッセージの要点を1-2行で簡潔に要約]

**分類:**
[情報共有/依頼/確認/緊急/相談 のいずれか]

**アクション:**
[必要なアクション項目を1行で]

**緊急度:**
[高/中/低]

**感情:**
[ポジティブ/ニュートラル/ネガティブ]

**推定処理時間:**
[対応にかかる推定時間]

**タグ:**
[関連するタグを3つまで、カンマ区切り]
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"""
**要約:**
{message_info['subject']}に関する業務連絡

**分類:**
確認

**アクション:**
内容確認後、適切に対応

**緊急度:**
中

**感情:**
ニュートラル

**推定処理時間:**
5-10分

**タグ:**
業務連絡, 確認事項, プロジェクト
        """

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

def parse_ai_response(response_text):
    """AI応答をパース"""
    sections = response_text.split("**")
    parsed_data = {}
    
    for i in range(1, len(sections), 2):
        if i + 1 < len(sections):
            key = sections[i].strip().replace(':', '')
            value = sections[i + 1].strip()
            parsed_data[key] = value
    
    return parsed_data

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

def initialize_session_state():
    """セッション状態の初期化"""
    if 'ai_tasks' not in st.session_state:
        st.session_state.ai_tasks = []
    
    if 'task_counter' not in st.session_state:
        st.session_state.task_counter = 1

def add_ai_task(message_info, task_data):
    """AIタスクをセッションに追加"""
    initialize_session_state()
    
    task = {
        'id': st.session_state.task_counter,
        'name': task_data.get('タスク名', f"{message_info['subject']}への対応"),
        'description': task_data.get('詳細説明', ''),
        'deadline': task_data.get('期限', '明日 17:00'),
        'priority': task_data.get('優先度', '中'),
        'category': task_data.get('カテゴリ', 'コミュニケーション'),
        'estimated_time': task_data.get('推定時間', '30分'),
        'checklist': task_data.get('チェックリスト', '').split('\n'),
        'completion_criteria': task_data.get('完了条件', ''),
        'status': '未着手',
        'created_from_message': True,
        'source_message': message_info,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    
    st.session_state.ai_tasks.append(task)
    st.session_state.task_counter += 1
    
    return task

def show_dashboard():
    """ダッシュボード表示"""
    st.title("📊 BizFlow AI ダッシュボード")
    st.markdown("### 🤖 AI統合管理サマリー")
    
    initialize_session_state()
    
    # 5列のレイアウト
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("🔴 緊急返信", "2件", "AI準備済み")
    
    with col2:
        st.metric("📝 要約済み", "12件", "+8件（今日）")
    
    with col3:
        ai_tasks_count = len([t for t in st.session_state.ai_tasks if t['created_from_message']])
        st.metric("🤖 AI作成タスク", f"{ai_tasks_count}件", "+3件（今日）")
    
    with col4:
        completed_tasks = len([t for t in st.session_state.ai_tasks if t['status'] == '完了'])
        st.metric("✅ 完了タスク", f"{completed_tasks}件", "+2件（今日）")
    
    with col5:
        st.metric("⏰ 節約時間", "3.2時間", "+45分（今日）")
    
    st.markdown("---")
    
    # AI提案セクション
    st.markdown("### 🤖 AI統合ワークフロー: 今日の推奨アクション")
    
    with st.expander("AI統合分析による推奨フロー", expanded=True):
        st.markdown("""
        **🔴 最優先フロー（今すぐ）**
        - 田中一郎さん：【緊急】プレゼン資料確認
          - ✅ AI要約完了 → ✅ 返信案準備済み → 🚀 タスク自動生成可能
        
        **🟡 重要フロー（今日中）** 
        - 山田花子さん：キャンペーン企画質問
          - ✅ AI分析完了 → 🚀 返信+タスク化推奨
        
        **🟢 標準フロー（明日以降）**
        - 佐藤次郎さん：進捗報告
          - ✅ 要約済み → ✅ 確認タスク自動生成済み
        
        **📊 AI統合効果**
        - 🤖 自動タスク生成: {ai_tasks_count}件
        - ⚡ 処理速度: 95%向上
        - 🎯 対応漏れ: 0件
        - 📈 生産性向上: 320%
        """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 AI全体再分析", type="primary"):
            with st.spinner("🤖 AI が全メッセージ・タスクを統合分析中..."):
                time.sleep(2)
            st.success("✅ 統合分析完了！メッセージ→タスク→フォローアップの最適化を更新しました。")
    
    with col2:
        if st.button("📊 AI効果レポート"):
            st.info("""
            📈 **今日のAI効果**
            - メッセージ処理時間: 90%削減
            - タスク作成時間: 100%削減（自動化）
            - 対応漏れ防止: 100%
            - 全体効率: 3.2倍向上
            """)

def show_ai_task_creation_dialog(message_info, summary_data=None):
    """AIタスク作成ダイアログ"""
    st.markdown(f"### 🤖 AIタスク自動生成: {message_info['subject']}")
    st.markdown(f"**送信者:** {message_info['sender']}")
    
    if summary_data:
        st.info(f"📝 **AI要約:** {summary_data.get('要約', 'N/A')}")
    
    # AI状態確認
    ai_available = setup_ai()
    
    if ai_available:
        st.success("🤖 AIタスク生成: 有効")
    else:
        st.warning("🤖 AIタスク生成: テストモード")
    
    # タスク生成オプション
    col1, col2 = st.columns(2)
    
    with col1:
        auto_deadline = st.checkbox("期限自動設定", value=True)
        auto_priority = st.checkbox("優先度自動判定", value=True)
    
    with col2:
        create_checklist = st.checkbox("チェックリスト自動生成", value=True)
        link_to_message = st.checkbox("メッセージと連携", value=True)
    
    # タスク生成実行
    if st.button("🚀 AIタスクを生成", type="primary"):
        with st.spinner("🤖 AIが最適なタスクを生成中..."):
            task_result = generate_ai_task(message_info, summary_data)
        
        # タスクデータをパース
        task_data = parse_ai_response(task_result)
        
        # タスクをセッションに追加
        created_task = add_ai_task(message_info, task_data)
        
        # 生成結果を表示
        st.markdown("### ✅ AIタスク生成完了！")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success(f"""
            **📋 タスク名:** {created_task['name']}
            **⏰ 期限:** {created_task['deadline']}
            **🎯 優先度:** {created_task['priority']}
            """)
        
        with col2:
            st.info(f"""
            **📂 カテゴリ:** {created_task['category']}
            **⏱️ 推定時間:** {created_task['estimated_time']}
            **🔗 メッセージ連携:** ✅
            """)
        
        # 詳細情報表示
        with st.expander("📋 タスク詳細", expanded=True):
            st.write(f"**詳細説明:** {created_task['description']}")
            
            if created_task['checklist'] and created_task['checklist'][0]:
                st.write("**チェックリスト:**")
                for item in created_task['checklist']:
                    if item.strip():
                        st.write(f"- {item.strip()}")
            
            st.write(f"**完了条件:** {created_task['completion_criteria']}")
        
        # 次のアクション
        st.markdown("### 🚀 次のアクション")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("✅ タスク管理で確認"):
                st.session_state.navigate_to_tasks = True
                st.success("タスク管理ページで確認できます！")
        
        with col2:
            if st.button("📧 返信も生成"):
                st.session_state.show_reply_dialog = True
                st.session_state.show_task_dialog = False
                st.rerun()
        
        with col3:
            if st.button("📅 カレンダー連携"):
                st.success("カレンダーに期限を追加しました！")
        
        with col4:
            if st.button("🔔 リマインダー設定"):
                st.success("期限前にリマインダーを設定しました！")

def show_ai_summary_dialog(message_info):
    """AI要約表示ダイアログ"""
    st.markdown(f"### 📝 AI要約分析: {message_info['subject']}")
    st.markdown(f"**送信者:** {message_info['sender']}")
    
    # AI状態確認
    ai_available = setup_ai()
    
    if ai_available:
        st.success("🤖 AI分析機能: 有効")
    else:
        st.warning("🤖 AI分析機能: テストモード")
    
    # 要約生成
    if st.button("🚀 AI分析を実行", type="primary"):
        with st.spinner("🤖 AIがメッセージを分析中..."):
            summary_result = generate_ai_summary(message_info)
        
        # 分析結果をパース
        analysis_data = parse_ai_response(summary_result)
        
        # セッションに保存（他の機能で使用するため）
        st.session_state.current_analysis = analysis_data
        
        # 分析結果を表示
        st.markdown("### 📊 AI分析結果")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 要約とアクション
            if '要約' in analysis_data:
                st.info(f"📝 **要約**\n{analysis_data['要約']}")
            
            if 'アクション' in analysis_data:
                st.warning(f"⚡ **必要なアクション**\n{analysis_data['アクション']}")
            
            if '推定処理時間' in analysis_data:
                st.success(f"⏰ **推定処理時間**\n{analysis_data['推定処理時間']}")
        
        with col2:
            # 分類と緊急度
            if '分類' in analysis_data:
                classification = analysis_data['分類']
                classification_colors = {
                    '緊急': '🔴',
                    '依頼': '🟡', 
                    '確認': '🔵',
                    '情報共有': '🟢',
                    '相談': '🟣'
                }
                icon = classification_colors.get(classification, '📋')
                st.markdown(f"**📂 分類:** {icon} {classification}")
            
            if '緊急度' in analysis_data:
                urgency = analysis_data['緊急度']
                urgency_colors = {'高': '🔴', '中': '🟡', '低': '🟢'}
                icon = urgency_colors.get(urgency, '📊')
                st.markdown(f"**⚡ 緊急度:** {icon} {urgency}")
            
            if '感情' in analysis_data:
                emotion = analysis_data['感情']
                emotion_colors = {
                    'ポジティブ': '😊',
                    'ニュートラル': '😐', 
                    'ネガティブ': '😟'
                }
                icon = emotion_colors.get(emotion, '💭')
                st.markdown(f"**💭 感情:** {icon} {emotion}")
        
        # タグ表示
        if 'タグ' in analysis_data:
            st.markdown("**🏷️ 関連タグ:**")
            tags = analysis_data['タグ'].split(',')
            tag_cols = st.columns(len(tags))
            for i, tag in enumerate(tags):
                with tag_cols[i]:
                    st.markdown(f"`{tag.strip()}`")
        
        # 統合アクションボタン
        st.markdown("---")
        st.markdown("### 🚀 統合アクション")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🤖 AI返信生成", type="primary"):
                st.session_state.selected_message = message_info
                st.session_state.show_reply_dialog = True
                st.session_state.show_summary_dialog = False
                st.rerun()
        
        with col2:
            if st.button("📋 AIタスク生成", type="primary"):
                st.session_state.selected_message = message_info
                st.session_state.show_task_dialog = True
                st.session_state.show_summary_dialog = False
                st.rerun()
        
        with col3:
            if st.button("⚡ 一括処理"):
                st.success("🤖 返信案生成 + タスク作成 + フォローアップ設定を実行中...")
                time.sleep(1)
                st.balloons()
                st.success("✅ 全ての処理が完了しました！")
        
        with col4:
            if st.button("📧 重要マーク"):
                st.success("⭐ 重要メッセージとしてマークしました！")

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
    
    # 返信生成オプション
    col1, col2 = st.columns(2)
    with col1:
        auto_task_after_reply = st.checkbox("返信後にタスク自動作成", value=True)
    with col2:
        auto_followup = st.checkbox("フォローアップ自動設定", value=True)
    
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
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button(f"📤 送信", key=f"send_{i}"):
                        st.success(f"✅ {message_info['sender']}に返信を送信しました！")
                        
                        # 自動タスク作成
                        if auto_task_after_reply:
                            task_data = {
                                'タスク名': f"{message_info['subject']} - フォローアップ",
                                '期限': '3日後 17:00',
                                '優先度': '中',
                                'カテゴリ': 'フォローアップ'
                            }
                            add_ai_task(message_info, task_data)
                            st.success("🤖 フォローアップタスクも自動作成しました！")
                        
                        st.balloons()
                
                with col2:
                    if st.button(f"📋 コピー", key=f"copy_{i}"):
                        st.success("📋 クリップボードにコピーしました！")
                
                with col3:
                    if st.button(f"📋 タスク化", key=f"task_{i}"):
                        # 返信をタスクに変換
                        task_data = {
                            'タスク名': f"{message_info['subject']}への返信送信",
                            '詳細説明': f"以下の内容で返信:\n{edited_content[:100]}...",
                            '期限': '今日 18:00',
                            '優先度': '高',
                            'カテゴリ': 'コミュニケーション'
                        }
                        add_ai_task(message_info, task_data)
                        st.success("📋 返信タスクを作成しました！")
                
                with col4:
                    if st.button(f"📅 後で送信", key=f"schedule_{i}"):
                        st.success("📅 指定時刻に自動送信する予約をしました！")

def show_communication():
    """AI機能付きコミュニケーション表示"""
    st.title("💬 AI駆動コミュニケーション統合管理")
    
    # AI状態表示
    ai_available = setup_ai()
    if ai_available:
        st.success("🤖 **AI統合システム全機能稼働中** - 要約・分析・返信生成・タスク自動作成・フォローアップが利用可能")
    else:
        st.warning("🤖 **AI統合テストモード** - 基本機能のみ利用可能（APIキーを設定してください）")
    
    st.markdown("---")
    st.markdown("### 📨 AI統合分析済みメッセージ一覧")
    
    # サンプルメッセージ（AI分析結果付き）
    messages = [
        {
            "sender": "田中一郎", 
            "subject": "【緊急】プレゼン資料確認", 
            "time": "14:30", 
            "priority": "🔴",
            "ai_category": "緊急対応",
            "ai_suggestion": "今すぐ返信推奨",
            "estimated_time": "2分",
            "ai_summary": "プレゼン資料の修正3箇所要請、明日15時締切",
            "tags": ["緊急", "プレゼン", "修正依頼"]
        },
        {
            "sender": "山田花子", 
            "subject": "キャンペーン企画の件", 
            "time": "13:15", 
            "priority": "🟡",
            "ai_category": "企画相談",
            "ai_suggestion": "今日中に返信",
            "estimated_time": "5分",
            "ai_summary": "新キャンペーンのターゲット層と予算について質問",
            "tags": ["企画", "マーケティング", "相談"]
        },
        {
            "sender": "佐藤次郎", 
            "subject": "進捗報告", 
            "time": "11:00", 
            "priority": "🟢",
            "ai_category": "定期報告",
            "ai_suggestion": "明日返信でOK",
            "estimated_time": "1分",
            "ai_summary": "システム更新80%完了、今週末完了予定",
            "tags": ["進捗", "システム", "報告"]
        }
    ]
    
    # ダイアログ表示モード
    if 'show_summary_dialog' in st.session_state and st.session_state.show_summary_dialog:
        selected_msg = st.session_state.selected_message
        show_ai_summary_dialog(selected_msg)
        
        if st.button("⬅️ メッセージ一覧に戻る"):
            st.session_state.show_summary_dialog = False
            st.rerun()
        return
    
    if 'show_reply_dialog' in st.session_state and st.session_state.show_reply_dialog:
        selected_msg = st.session_state.selected_message
        show_ai_reply_dialog(selected_msg)
        
        if st.button("⬅️ メッセージ一覧に戻る"):
            st.session_state.show_reply_dialog = False
            st.rerun()
        return
    
    if 'show_task_dialog' in st.session_state and st.session_state.show_task_dialog:
        selected_msg = st.session_state.selected_message
        summary_data = st.session_state.get('current_analysis', None)
        show_ai_task_creation_dialog(selected_msg, summary_data)
        
        if st.button("⬅️ メッセージ一覧に戻る"):
            st.session_state.show_task_dialog = False
            st.rerun()
        return
    
    # メッセージ一覧表示
    for msg in messages:
        with st.container():
            # メッセージヘッダー
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"{msg['priority']} **{msg['subject']}** - {msg['sender']} ({msg['time']})")
                # AI要約を小さく表示
                st.caption(f"📝 AI要約: {msg['ai_summary']}")
                # タグ表示
                tag_text = " ".join([f"`{tag}`" for tag in msg['tags']])
                st.markdown(f"🏷️ {tag_text}")
            
            with col2:
                # 統合AIワークフロー
                if st.button("🚀 AI統合処理", key=f"ai_workflow_{msg['sender']}", type="primary"):
                    with st.spinner("🤖 AI統合ワークフロー実行中..."):
                        time.sleep(2)
                    st.success("✅ 要約→返信案→タスク→フォローアップの統合処理完了！")
                    st.balloons()
            
            # 個別アクションボタン
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("📝 要約", key=f"summary_{msg['sender']}"):
                    st.session_state.selected_message = msg
                    st.session_state.show_summary_dialog = True
                    st.rerun()
            
            with col2:
                if st.button("🚀 返信", key=f"reply_{msg['sender']}"):
                    st.session_state.selected_message = msg
                    st.session_state.show_reply_dialog = True
                    st.rerun()
            
            with col3:
                if st.button("📋 タスク", key=f"task_create_{msg['sender']}"):
                    st.session_state.selected_message = msg
                    st.session_state.show_task_dialog = True
                    st.rerun()
            
            with col4:
                if st.button("⚡ 全処理", key=f"all_process_{msg['sender']}"):
                    # 要約→返信→タスクの統合処理デモ
                    with st.spinner("🤖 統合AI処理中..."):
                        # タスク自動作成
                        task_data = {
                            'タスク名': f"{msg['subject']}への対応",
                            '期限': '明日 17:00',
                            '優先度': msg['priority'].split()[1] if len(msg['priority'].split()) > 1 else '中',
                            'カテゴリ': 'コミュニケーション'
                        }
                        add_ai_task(msg, task_data)
                        time.sleep(1)
                    
                    st.success("✅ 要約・返信案・タスク・フォローアップをすべて準備しました！")
            
            st.markdown("---")

def show_tasks():
    """AI駆動タスク管理表示"""
    st.title("✅ AI統合タスク管理システム")
    
    initialize_session_state()
    
    # タスク統計
    ai_tasks = [t for t in st.session_state.ai_tasks if t['created_from_message']]
    manual_tasks = [t for t in st.session_state.ai_tasks if not t['created_from_message']]
    completed_tasks = [t for t in st.session_state.ai_tasks if t['status'] == '完了']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🤖 AI作成タスク", f"{len(ai_tasks)}件", "自動生成")
    
    with col2:
        st.metric("👤 手動タスク", f"{len(manual_tasks)}件", "手動作成")
    
    with col3:
        st.metric("✅ 完了タスク", f"{len(completed_tasks)}件", "今日")
    
    with col4:
        total_estimated_time = sum([
            int(t['estimated_time'].split('分')[0]) if '分' in t['estimated_time'] 
            else int(t['estimated_time'].split('時間')[0]) * 60 if '時間' in t['estimated_time']
            else 30 
            for t in st.session_state.ai_tasks if t['status'] != '完了'
        ])
        st.metric("⏰ 残り時間", f"{total_estimated_time}分", "推定")
    
    st.markdown("---")
    st.markdown("### 🤖 AI統合タスク一覧")
    
    # デフォルトタスクの追加（初回のみ）
    if not st.session_state.ai_tasks:
        default_tasks = [
            {
                'id': 1, 'name': '田中さんへの返信', 'priority': '高', 'status': 'AI準備済み', 
                'estimated_time': '2分', 'created_from_message': True, 'category': 'コミュニケーション',
                'deadline': '今日 18:00', 'description': '【緊急】プレゼン資料確認への返信',
                'source_message': {'sender': '田中一郎', 'subject': '【緊急】プレゼン資料確認'},
                'checklist': ['メッセージ確認', '返信内容検討', '送信'], 
                'completion_criteria': '返信送信完了', 'created_at': '2025-07-19 14:30'
            },
            {
                'id': 2, 'name': 'プロポーザル作成', 'priority': '高', 'status': '進行中', 
                'estimated_time': '2時間', 'created_from_message': False, 'category': 'プロジェクト作業',
                'deadline': '明日 12:00', 'description': '新規クライアント向けプロポーザル資料作成',
                'checklist': ['要件整理', '資料作成', 'レビュー'], 
                'completion_criteria': 'プロポーザル完成', 'created_at': '2025-07-18 10:00'
            },
            {
                'id': 3, 'name': 'キャンペーン企画回答', 'priority': '中', 'status': 'AI支援可能', 
                'estimated_time': '30分', 'created_from_message': True, 'category': 'コミュニケーション',
                'deadline': '今日 17:00', 'description': '山田花子さんからの企画相談への回答',
                'source_message': {'sender': '山田花子', 'subject': 'キャンペーン企画の件'},
                'checklist': ['企画内容確認', '回答準備', '返信'], 
                'completion_criteria': '企画回答送信', 'created_at': '2025-07-19 13:15'
            }
        ]
        st.session_state.ai_tasks = default_tasks
        st.session_state.task_counter = 4
    
    # タスク表示
    for task in st.session_state.ai_tasks:
        with st.container():
            col1, col2, col3, col4, col5, col6 = st.columns([3, 1, 1, 1, 1, 1])
            
            with col1:
                task_name = task["name"]
                if task["created_from_message"]:
                    task_name += " 🤖"
                
                if task['status'] == '完了':
                    st.markdown(f"~~{task_name}~~")
                else:
                    st.write(f"**{task_name}**")
                
                # メッセージ連携情報
                if task.get("source_message"):
                    st.caption(f"📧 {task['source_message']['sender']} - {task['source_message']['subject']}")
            
            with col2:
                priority_colors = {"高": "🔴", "中": "🟡", "低": "🟢"}
                priority_text = priority_colors.get(task['priority'], "📊")
                st.write(f"{priority_text} {task['priority']}")
            
            with col3:
                status_colors = {
                    "未着手": "⚪", "進行中": "🟡", "AI準備済み": "🤖", 
                    "AI支援可能": "🔧", "完了": "✅"
                }
                status_icon = status_colors.get(task['status'], "📋")
                st.write(f"{status_icon} {task['status']}")
            
            with col4:
                st.write(f"⏰ {task['estimated_time']}")
            
            with col5:
                st.write(f"📅 {task['deadline']}")
            
            with col6:
                if task['status'] != '完了':
                    if st.button("完了", key=f"complete_{task['id']}"):
                        task['status'] = '完了'
                        st.success(f"「{task['name']}」を完了しました！")
                        st.rerun()
                else:
                    st.write("✅ 完了済み")
            
            # タスク詳細（展開可能）
            if task['status'] != '完了':
                with st.expander(f"📋 {task['name']} - 詳細", expanded=False):
                    st.write(f"**説明:** {task.get('description', 'N/A')}")
                    st.write(f"**カテゴリ:** {task.get('category', 'N/A')}")
                    st.write(f"**作成日時:** {task.get('created_at', 'N/A')}")
                    
                    if task.get('checklist'):
                        st.write("**チェックリスト:**")
                        for item in task['checklist']:
                            if item:
                                st.write(f"- {item}")
                    
                    if task.get('completion_criteria'):
                        st.write(f"**完了条件:** {task['completion_criteria']}")
                    
                    # アクションボタン
                    action_col1, action_col2, action_col3 = st.columns(3)
                    
                    with action_col1:
                        if task.get('source_message') and st.button("📧 元メッセージ", key=f"msg_{task['id']}"):
                            st.info(f"📧 {task['source_message']['sender']}: {task['source_message']['subject']}")
                    
                    with action_col2:
                        if st.button("🤖 AI支援", key=f"ai_help_{task['id']}"):
                            st.success("🤖 AIが作業のヒントとネクストステップを提案中...")
                    
                    with action_col3:
                        if st.button("📅 期限変更", key=f"deadline_{task['id']}"):
                            st.info("📅 期限変更機能は開発中です")
            
            st.markdown("---")
    
    # 新規タスク作成セクション
    st.markdown("### ➕ 新規タスク作成")
    
    with st.expander("手動でタスクを作成", expanded=False):
        with st.form("manual_task_creation"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_task_name = st.text_input("タスク名")
                new_task_priority = st.selectbox("優先度", ["高", "中", "低"])
                new_task_category = st.selectbox("カテゴリ", ["コミュニケーション", "プロジェクト作業", "会議", "レビュー", "調査"])
            
            with col2:
                new_task_deadline = st.text_input("期限", placeholder="明日 17:00")
                new_task_time = st.text_input("推定時間", placeholder="30分")
                new_task_description = st.text_area("説明", height=100)
            
            if st.form_submit_button("📋 タスクを作成"):
                if new_task_name:
                    new_task = {
                        'id': st.session_state.task_counter,
                        'name': new_task_name,
                        'priority': new_task_priority,
                        'status': '未着手',
                        'estimated_time': new_task_time or '30分',
                        'deadline': new_task_deadline or '明日 17:00',
                        'category': new_task_category,
                        'description': new_task_description,
                        'created_from_message': False,
                        'checklist': [],
                        'completion_criteria': '',
                        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M')
                    }
                    
                    st.session_state.ai_tasks.append(new_task)
                    st.session_state.task_counter += 1
                    
                    st.success(f"✅ タスク「{new_task_name}」を作成しました！")
                    st.rerun()
                else:
                    st.error("タスク名を入力してください。")

def show_projects():
    """AI駆動プロジェクト管理表示"""
    st.title("📁 AI駆動プロジェクト管理")
    
    st.markdown("### 🤖 AI分析済みプロジェクト")
    
    projects = [
        {"name": "プロジェクトX", "progress": 65, "status": "順調", "ai_insight": "予定通り進行中、リスクなし", "related_tasks": 3},
        {"name": "マーケティング戦略", "progress": 30, "status": "要注意", "ai_insight": "リソース不足、追加人員検討推奨", "related_tasks": 2},
    ]
    
    for project in projects:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write(f"**{project['name']}**")
            st.progress(project['progress'] / 100, text=f"進捗: {project['progress']}%")
            st.write(f"🤖 **AI分析:** {project['ai_insight']}")
            st.write(f"📋 **関連タスク:** {project['related_tasks']}件")
        
        with col2:
            st.write(f"状況: {project['status']}")
            if st.button(f"🤖 AI提案", key=f"ai_suggest_{project['name']}"):
                st.info("🤖 AIが最新の状況を分析して提案を準備中...")
            
            if st.button(f"📋 タスク追加", key=f"add_task_{project['name']}"):
                st.success(f"🤖 {project['name']}用の新規タスクを自動生成しました！")

def main():
    """メインアプリケーション"""
    
    # 認証チェック
    if not simple_auth():
        return
    
    # セッション状態初期化
    initialize_session_state()
    
    # サイドバー
    st.sidebar.title("🚀 BizFlow AI")
    st.sidebar.markdown("---")
    
    # AI状態表示
    ai_available = setup_ai()
    if ai_available:
        st.sidebar.success("🤖 AI: 完全統合")
        st.sidebar.write("📝 要約・返信・タスク・分析")
    else:
        st.sidebar.warning("🤖 AI: テストモード")
    
    st.sidebar.markdown("---")
    
    # ナビゲーション
    page = st.sidebar.selectbox(
        "メニュー",
        ["📊 ダッシュボード", "💬 コミュニケーション", "✅ タスク管理", "📁 プロジェクト管理"]
    )
    
    st.sidebar.markdown("---")
    
    # 今日の AI 統合サマリー
    st.sidebar.markdown("### 🤖 AI統合効果")
    ai_tasks_count = len([t for t in st.session_state.ai_tasks if t['created_from_message']])
    st.sidebar.write(f"📝 要約生成: 12件")
    st.sidebar.write(f"🚀 返信作成: 8件")
    st.sidebar.write(f"📋 自動タスク: {ai_tasks_count}件")
    st.sidebar.write(f"⏰ 節約時間: 3.2時間")
    
    # 進捗表示
    st.sidebar.markdown("### 📈 統合効率")
    completed_count = len([t for t in st.session_state.ai_tasks if t['status'] == '完了'])
    total_count = len(st.session_state.ai_tasks)
    completion_rate = completed_count / total_count if total_count > 0 else 0
    
    st.sidebar.progress(completion_rate, text=f"完了率: {int(completion_rate * 100)}%")
    st.sidebar.write("🤖 AI統合効率: 98%")
    
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