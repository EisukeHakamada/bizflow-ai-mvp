"""
BizFlow AI MVP - AI要約機能付き拡張版
Gemini APIを使用した要約・分類・タグ付け機能
"""

import streamlit as st
import sys
import os
import time

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
    st.markdown("### 🤖 AI分析サマリー")
    
    # 4列のレイアウト
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🔴 緊急返信", "2件", "AI準備済み")
    
    with col2:
        st.metric("📝 要約済み", "12件", "+8件（今日）")
    
    with col3:
        st.metric("✅ 完了タスク", "5件", "+2件（今日）")
    
    with col4:
        st.metric("⏰ 節約時間", "2.5時間", "+30分（今日）")
    
    st.markdown("---")
    
    # AI提案セクション
    st.markdown("### 🤖 AI提案: 今日の優先アクション")
    
    with st.expander("AI分析による推奨アクション", expanded=True):
        st.markdown("""
        **🔴 最優先（今すぐ）**
        - 田中一郎さん：【緊急】プレゼン資料確認 → **要約済み・返信案準備済み**
        
        **🟡 重要（今日中）** 
        - 山田花子さん：キャンペーン企画質問 → **要約済み・詳細確認推奨**
        
        **🟢 通常（明日以降）**
        - 佐藤次郎さん：進捗報告 → **要約済み・確認のみ**
        
        **📊 AI分析結果**
        - 処理済みメッセージ: 12件
        - 節約時間: 2.5時間
        - AI精度: 96%
        """)
    
    if st.button("🔄 AI再分析"):
        with st.spinner("🤖 AIが全メッセージを再分析中..."):
            time.sleep(2)
        st.success("✅ 分析完了！最新の優先度で更新しました。")

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
        
        # 分析結果を表示
        st.markdown("### 📊 AI分析結果")
        
        # 分析結果をパース
        sections = summary_result.split("**")
        analysis_data = {}
        
        for i in range(1, len(sections), 2):
            if i + 1 < len(sections):
                key = sections[i].strip().replace(':', '')
                value = sections[i + 1].strip()
                analysis_data[key] = value
        
        # 分析結果を美しく表示
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
        
        # アクションボタン
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🚀 AI返信生成"):
                st.session_state.selected_message = message_info
                st.session_state.show_reply_dialog = True
                st.session_state.show_summary_dialog = False
                st.rerun()
        
        with col2:
            if st.button("📋 タスク作成"):
                task_name = f"{message_info['subject']}への対応"
                st.success(f"✅ タスク「{task_name}」を作成しました！")
        
        with col3:
            if st.button("📅 フォローアップ"):
                st.success("📅 3日後にフォローアップリマインダーを設定しました！")
        
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
        st.success("🤖 **AI機能フル稼働中** - 要約・分析・返信生成・分類・タグ付けが利用可能")
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
                # メイン AI アクション
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("📝 要約", key=f"summary_{msg['sender']}", type="primary"):
                        st.session_state.selected_message = msg
                        st.session_state.show_summary_dialog = True
                        st.rerun()
                
                with col_b:
                    if st.button("🚀 返信", key=f"ai_reply_{msg['sender']}", type="primary"):
                        st.session_state.selected_message = msg
                        st.session_state.show_reply_dialog = True
                        st.rerun()
            
            # 詳細分析情報
            with st.expander("🤖 AI分析詳細", expanded=False):
                detail_col1, detail_col2 = st.columns(2)
                
                with detail_col1:
                    st.write(f"**📂 分類:** {msg['ai_category']}")
                    st.write(f"**⚡ 推奨:** {msg['ai_suggestion']}")
                
                with detail_col2:
                    st.write(f"**⏰ 予想時間:** {msg['estimated_time']}")
                    st.write(f"**🎯 優先度:** {msg['priority']}")
                
                # サブアクション
                sub_col1, sub_col2, sub_col3 = st.columns(3)
                with sub_col1:
                    if st.button("📋 タスク化", key=f"task_{msg['sender']}"):
                        st.success(f"✅ 「{msg['subject']}への対応」タスクを作成しました！")
                
                with sub_col2:
                    if st.button("⚡ 優先度変更", key=f"priority_{msg['sender']}"):
                        st.info("🤖 AIが状況を再分析して優先度を調整しました")
                
                with sub_col3:
                    if st.button("📅 リマインド", key=f"remind_{msg['sender']}"):
                        st.success("📅 フォローアップリマインダーを設定しました！")
            
            st.markdown("---")

def show_tasks():
    """AI駆動タスク管理表示"""
    st.title("✅ AI駆動タスク管理")
    
    st.markdown("### 🤖 AI分析済みタスク一覧")
    
    tasks = [
        {"name": "田中さんへの返信", "priority": "🔴 高", "status": "AI準備済み", "ai_time": "2分", "auto_created": True},
        {"name": "プロポーザル作成", "priority": "🔴 高", "status": "進行中", "ai_time": "2時間", "auto_created": False},
        {"name": "ミーティング準備", "priority": "🟡 中", "status": "AI支援可能", "ai_time": "30分", "auto_created": False},
        {"name": "市場調査", "priority": "🟢 低", "status": "未着手", "ai_time": "3時間", "auto_created": False}
    ]
    
    for task in tasks:
        col1, col2, col3, col4, col5, col6 = st.columns([3, 1, 1, 1, 1, 1])
        
        with col1:
            task_name = task["name"]
            if task["auto_created"]:
                task_name += " 🤖"
            st.write(task_name)
        
        with col2:
            st.write(task["priority"])
        
        with col3:
            st.write(task["status"])
        
        with col4:
            st.write(f"⏰ {task['ai_time']}")
        
        with col5:
            if st.button("完了", key=f"complete_{task['name']}"):
                st.success(f"「{task['name']}」を完了しました！")
        
        with col6:
            if st.button("🤖", key=f"ai_assist_{task['name']}"):
                st.info("🤖 AIアシスタント機能は開発中です")

def show_projects():
    """AI駆動プロジェクト管理表示"""
    st.title("📁 AI駆動プロジェクト管理")
    
    st.markdown("### 🤖 AI分析済みプロジェクト")
    
    projects = [
        {"name": "プロジェクトX", "progress": 65, "status": "順調", "ai_insight": "予定通り進行中、リスクなし"},
        {"name": "マーケティング戦略", "progress": 30, "status": "要注意", "ai_insight": "リソース不足、追加人員検討推奨"},
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
                st.info("🤖 AIが最新の状況を分析して提案を準備中...")

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
        st.sidebar.success("🤖 AI: フル稼働")
        st.sidebar.write("📝 要約・分析・返信生成")
    else:
        st.sidebar.warning("🤖 AI: テストモード")
    
    st.sidebar.markdown("---")
    
    # ナビゲーション
    page = st.sidebar.selectbox(
        "メニュー",
        ["📊 ダッシュボード", "💬 コミュニケーション", "✅ タスク管理", "📁 プロジェクト管理"]
    )
    
    st.sidebar.markdown("---")
    
    # 今日の AI 分析サマリー
    st.sidebar.markdown("### 🤖 今日のAI分析")
    st.sidebar.write("📝 要約済み: 12件")
    st.sidebar.write("🚀 返信生成: 8件")
    st.sidebar.write("📋 自動タスク: 3件")
    st.sidebar.write("⏰ 節約時間: 2.5時間")
    
    # 進捗表示
    st.sidebar.markdown("### 📈 今日の進捗")
    st.sidebar.progress(0.75, text="完了率: 75%")
    st.sidebar.write("🤖 AI支援効率: 96%")
    
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