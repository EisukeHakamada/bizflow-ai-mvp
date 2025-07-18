"""
BizFlow AI MVP - 超リアルAsana風タスク管理システム
ドラッグ風ステータス変更・モーダル詳細表示・完全インタラクティブUI
"""

import streamlit as st
import sys
import os
import time
from datetime import datetime, timedelta
import json

# プロジェクトのルートディレクトリをPythonパスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Streamlitページ設定
st.set_page_config(
    page_title="BizFlow AI MVP",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 超リアルAsana風CSS
st.markdown("""
<style>
    /* グローバルスタイル */
    .main .block-container {
        padding-top: 2rem;
        max-width: 1400px;
    }
    
    /* カンバンボードコンテナ */
    .kanban-container {
        display: flex;
        gap: 20px;
        padding: 20px 0;
        min-height: 600px;
    }
    
    /* カンバン列スタイル */
    .kanban-column {
        flex: 1;
        background: #fafbfc;
        border-radius: 12px;
        padding: 16px;
        border: 1px solid #dfe1e6;
        position: relative;
        min-height: 500px;
    }
    
    .kanban-header {
        font-weight: 600;
        font-size: 16px;
        color: #172b4d;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 2px solid #e4e6ea;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .task-count {
        background: #dfe1e6;
        color: #5e6c84;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 500;
    }
    
    /* タスクカードスタイル */
    .task-card {
        background: white;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
        border: 1px solid #dfe1e6;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .task-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transform: translateY(-2px);
        border-color: #0052cc;
    }
    
    .task-card:active {
        transform: translateY(0);
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    }
    
    .task-card-inner {
        position: relative;
        z-index: 2;
    }
    
    /* 優先度インジケーター */
    .priority-indicator {
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        border-radius: 8px 0 0 8px;
    }
    
    .priority-high { background: #de350b; }
    .priority-medium { background: #ff8b00; }
    .priority-low { background: #00875a; }
    
    /* タスクヘッダー */
    .task-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 8px;
    }
    
    .task-title {
        font-weight: 500;
        font-size: 14px;
        color: #172b4d;
        line-height: 1.4;
        margin: 0;
        flex: 1;
        padding-right: 8px;
    }
    
    .task-actions {
        display: flex;
        gap: 4px;
        opacity: 0;
        transition: opacity 0.2s ease;
    }
    
    .task-card:hover .task-actions {
        opacity: 1;
    }
    
    .action-btn {
        width: 24px;
        height: 24px;
        border-radius: 4px;
        border: none;
        background: #f4f5f7;
        color: #5e6c84;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        transition: all 0.2s ease;
    }
    
    .action-btn:hover {
        background: #e4e6ea;
        color: #172b4d;
    }
    
    /* タスクメタ情報 */
    .task-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 12px;
        font-size: 12px;
        color: #5e6c84;
    }
    
    .task-tags {
        display: flex;
        gap: 4px;
        flex-wrap: wrap;
        margin-bottom: 8px;
    }
    
    .tag {
        padding: 2px 6px;
        border-radius: 12px;
        font-size: 10px;
        font-weight: 500;
        white-space: nowrap;
    }
    
    .tag-ai {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
    }
    
    .tag-project {
        background: #e3fcef;
        color: #006644;
    }
    
    .tag-category {
        background: #deebff;
        color: #0052cc;
    }
    
    /* サブタスク進捗 */
    .subtask-progress {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 11px;
        color: #5e6c84;
    }
    
    .progress-bar {
        width: 60px;
        height: 4px;
        background: #dfe1e6;
        border-radius: 2px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: #00875a;
        transition: width 0.3s ease;
    }
    
    /* モーダルスタイル */
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: fadeIn 0.3s ease;
    }
    
    .modal-content {
        background: white;
        border-radius: 12px;
        box-shadow: 0 12px 24px rgba(0,0,0,0.3);
        max-width: 800px;
        width: 90%;
        max-height: 90vh;
        overflow-y: auto;
        animation: slideIn 0.3s ease;
    }
    
    .modal-header {
        padding: 24px 24px 0 24px;
        border-bottom: 1px solid #dfe1e6;
        margin-bottom: 24px;
    }
    
    .modal-body {
        padding: 0 24px 24px 24px;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideIn {
        from { transform: translateY(-50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    /* ステータス移動ボタン */
    .status-move-btn {
        background: linear-gradient(135deg, #0052cc, #2684ff);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 4px 8px;
        font-size: 11px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 1px 3px rgba(0,82,204,0.3);
    }
    
    .status-move-btn:hover {
        background: linear-gradient(135deg, #0065ff, #2684ff);
        transform: translateY(-1px);
        box-shadow: 0 2px 6px rgba(0,82,204,0.4);
    }
    
    /* 新規タスクボタン */
    .add-task-btn {
        width: 100%;
        padding: 12px;
        border: 2px dashed #dfe1e6;
        background: transparent;
        border-radius: 8px;
        color: #5e6c84;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.2s ease;
        margin-top: 8px;
    }
    
    .add-task-btn:hover {
        border-color: #0052cc;
        color: #0052cc;
        background: #f4f5f7;
    }
    
    /* レスポンシブ対応 */
    @media (max-width: 768px) {
        .kanban-container {
            flex-direction: column;
            gap: 16px;
        }
        
        .kanban-column {
            min-height: auto;
        }
        
        .modal-content {
            width: 95%;
            margin: 20px;
        }
    }
</style>
""", unsafe_allow_html=True)

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

**サブタスク:**
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

**サブタスク:**
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
        # サンプルタスクデータ
        st.session_state.ai_tasks = [
            {
                'id': 1,
                'name': '田中さんへの緊急返信',
                'description': '【緊急】プレゼン資料確認への返信対応。修正箇所の特定と迅速な対応が必要。',
                'status': 'To Do',
                'priority': '高',
                'project': 'プロジェクトX',
                'assignee': '自分',
                'due_date': '今日 18:00',
                'estimated_time': '15分',
                'created_from_message': True,
                'source_message': {'sender': '田中一郎', 'subject': '【緊急】プレゼン資料確認'},
                'subtasks': [
                    {'id': 1, 'name': 'メッセージ内容の詳細確認', 'completed': False},
                    {'id': 2, 'name': 'プレゼン資料の確認', 'completed': False},
                    {'id': 3, 'name': '修正箇所の特定と対応', 'completed': False}
                ],
                'comments': [],
                'tags': ['緊急', 'プレゼン', 'コミュニケーション'],
                'created_at': '2025-07-19 14:30',
                'completion_criteria': '田中さんへの返信送信完了'
            },
            {
                'id': 2,
                'name': 'マーケティング企画への回答',
                'description': '山田花子さんからのキャンペーン企画相談への対応。ターゲット層分析とKPI設定を含む包括的な回答が必要。',
                'status': '進行中',
                'priority': '中',
                'project': 'マーケティング戦略',
                'assignee': '自分',
                'due_date': '明日 17:00',
                'estimated_time': '45分',
                'created_from_message': True,
                'source_message': {'sender': '山田花子', 'subject': 'キャンペーン企画の件'},
                'subtasks': [
                    {'id': 1, 'name': 'ターゲット層の分析', 'completed': True},
                    {'id': 2, 'name': '予算配分の検討', 'completed': False},
                    {'id': 3, 'name': 'KPI設定の提案', 'completed': False}
                ],
                'comments': [
                    {'author': '自分', 'text': 'ターゲット層の分析完了。20代女性を中心に検討。', 'timestamp': '2025-07-19 15:30'}
                ],
                'tags': ['企画', 'マーケティング', 'コミュニケーション'],
                'created_at': '2025-07-19 13:15',
                'completion_criteria': '企画提案の回答送信完了'
            },
            {
                'id': 3,
                'name': 'クライアント向けプロポーザル作成',
                'description': '新規クライアント向けの提案資料作成。要件整理からデザイン調整まで含む完全版の作成。',
                'status': 'レビュー中',
                'priority': '高',
                'project': 'プロジェクトX',
                'assignee': '自分',
                'due_date': '明後日 12:00',
                'estimated_time': '3時間',
                'created_from_message': False,
                'subtasks': [
                    {'id': 1, 'name': '要件整理', 'completed': True},
                    {'id': 2, 'name': 'コンテンツ作成', 'completed': True},
                    {'id': 3, 'name': 'デザイン調整', 'completed': True},
                    {'id': 4, 'name': '最終レビュー', 'completed': False}
                ],
                'comments': [
                    {'author': '自分', 'text': 'プロポーザルのドラフト完成。レビュー待ち。', 'timestamp': '2025-07-19 16:00'}
                ],
                'tags': ['プロポーザル', '営業', 'ドキュメント'],
                'created_at': '2025-07-18 09:00',
                'completion_criteria': 'プロポーザル完成・提出完了'
            },
            {
                'id': 4,
                'name': 'システム進捗報告の確認',
                'description': '佐藤次郎さんからの進捗報告内容の確認と返信。システム更新の進行状況を把握し適切にフィードバック。',
                'status': '完了',
                'priority': '低',
                'project': 'システム開発',
                'assignee': '自分',
                'due_date': '今日 17:00',
                'estimated_time': '10分',
                'created_from_message': True,
                'source_message': {'sender': '佐藤次郎', 'subject': '進捗報告'},
                'subtasks': [
                    {'id': 1, 'name': '進捗内容の確認', 'completed': True},
                    {'id': 2, 'name': '質問事項の整理', 'completed': True},
                    {'id': 3, 'name': '確認返信の送信', 'completed': True}
                ],
                'comments': [
                    {'author': '自分', 'text': '80%進捗確認。予定通り完了見込み。', 'timestamp': '2025-07-19 11:30'}
                ],
                'tags': ['進捗', 'システム', '報告'],
                'created_at': '2025-07-19 11:00',
                'completion_criteria': '進捗確認と返信完了'
            }
        ]
    
    if 'task_counter' not in st.session_state:
        st.session_state.task_counter = 5
    
    if 'projects' not in st.session_state:
        st.session_state.projects = [
            {
                'id': 1,
                'name': 'プロジェクトX',
                'description': '新規事業立ち上げプロジェクト',
                'status': 'アクティブ',
                'progress': 65,
                'color': '#6f42c1'
            },
            {
                'id': 2,
                'name': 'マーケティング戦略',
                'description': '2025年マーケティング戦略策定',
                'status': 'アクティブ',
                'progress': 40,
                'color': '#20c997'
            },
            {
                'id': 3,
                'name': 'システム開発',
                'description': '社内システムの改修プロジェクト',
                'status': 'アクティブ',
                'progress': 80,
                'color': '#fd7e14'
            }
        ]
    
    if 'selected_task_id' not in st.session_state:
        st.session_state.selected_task_id = None
    
    if 'show_task_modal' not in st.session_state:
        st.session_state.show_task_modal = False

def add_ai_task(message_info, task_data):
    """AIタスクをセッションに追加"""
    initialize_session_state()
    
    # サブタスクの処理
    subtasks_text = task_data.get('サブタスク', '')
    subtasks = []
    if subtasks_text:
        subtask_lines = subtasks_text.split('\n')
        for i, line in enumerate(subtask_lines):
            if line.strip():
                subtasks.append({
                    'id': i + 1,
                    'name': line.strip(),
                    'completed': False
                })
    
    task = {
        'id': st.session_state.task_counter,
        'name': task_data.get('タスク名', f"{message_info['subject']}への対応"),
        'description': task_data.get('詳細説明', ''),
        'status': 'To Do',
        'priority': task_data.get('優先度', '中'),
        'project': task_data.get('カテゴリ', 'コミュニケーション'),
        'assignee': '自分',
        'due_date': task_data.get('期限', '明日 17:00'),
        'estimated_time': task_data.get('推定時間', '30分'),
        'created_from_message': True,
        'source_message': message_info,
        'subtasks': subtasks,
        'comments': [],
        'tags': ['AI生成', 'コミュニケーション'],
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'completion_criteria': task_data.get('完了条件', '')
    }
    
    st.session_state.ai_tasks.append(task)
    st.session_state.task_counter += 1
    
    return task

def get_task_by_id(task_id):
    """タスクIDからタスクを取得"""
    for task in st.session_state.ai_tasks:
        if task['id'] == task_id:
            return task
    return None

def update_task_status(task_id, new_status):
    """タスクのステータスを更新"""
    for task in st.session_state.ai_tasks:
        if task['id'] == task_id:
            task['status'] = new_status
            break

def get_next_status(current_status):
    """次のステータスを取得"""
    status_flow = {
        'To Do': '進行中',
        '進行中': 'レビュー中', 
        'レビュー中': '完了',
        '完了': '完了'
    }
    return status_flow.get(current_status, current_status)

def get_prev_status(current_status):
    """前のステータスを取得"""
    status_flow = {
        '進行中': 'To Do',
        'レビュー中': '進行中',
        '完了': 'レビュー中',
        'To Do': 'To Do'
    }
    return status_flow.get(current_status, current_status)

def show_dashboard():
    """ダッシュボード表示"""
    st.title("📊 BizFlow AI ダッシュボード")
    st.markdown("### 🤖 AI統合管理サマリー")
    
    initialize_session_state()
    
    # プロジェクト別タスク統計
    project_stats = {}
    for task in st.session_state.ai_tasks:
        project = task.get('project', 'その他')
        if project not in project_stats:
            project_stats[project] = {'total': 0, 'completed': 0}
        project_stats[project]['total'] += 1
        if task['status'] == '完了':
            project_stats[project]['completed'] += 1
    
    # 5列のレイアウト
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        todo_count = len([t for t in st.session_state.ai_tasks if t['status'] == 'To Do'])
        st.metric("📋 To Do", f"{todo_count}件", "新規タスク")
    
    with col2:
        progress_count = len([t for t in st.session_state.ai_tasks if t['status'] == '進行中'])
        st.metric("🔄 進行中", f"{progress_count}件", "作業中")
    
    with col3:
        review_count = len([t for t in st.session_state.ai_tasks if t['status'] == 'レビュー中'])
        st.metric("👀 レビュー中", f"{review_count}件", "確認待ち")
    
    with col4:
        completed_count = len([t for t in st.session_state.ai_tasks if t['status'] == '完了'])
        st.metric("✅ 完了", f"{completed_count}件", "今日")
    
    with col5:
        ai_count = len([t for t in st.session_state.ai_tasks if t['created_from_message']])
        st.metric("🤖 AI作成", f"{ai_count}件", "自動生成")
    
    st.markdown("---")
    
    # プロジェクト進捗サマリー
    st.markdown("### 📁 プロジェクト進捗サマリー")
    
    for project in st.session_state.projects:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**{project['name']}**")
            st.progress(project['progress'] / 100, text=f"全体進捗: {project['progress']}%")
            
            # プロジェクト別タスク統計
            if project['name'] in project_stats:
                stats = project_stats[project['name']]
                completion_rate = (stats['completed'] / stats['total']) * 100 if stats['total'] > 0 else 0
                st.caption(f"タスク: {stats['completed']}/{stats['total']} 完了 ({completion_rate:.0f}%)")
        
        with col2:
            st.markdown(f"**ステータス:** {project['status']}")
            if st.button(f"📋 タスク表示", key=f"show_project_{project['id']}"):
                st.session_state.selected_project_filter = project['name']
                st.info(f"タスク管理ページで{project['name']}のタスクを表示します")

def show_ultra_asana_kanban():
    """超リアルAsana風カンバンボード"""
    st.markdown("### 📋 カンバンボード")
    
    # ステータス列の定義
    statuses = [
        {'name': 'To Do', 'color': '#6c757d'},
        {'name': '進行中', 'color': '#007bff'},
        {'name': 'レビュー中', 'color': '#ffc107'},
        {'name': '完了', 'color': '#28a745'}
    ]
    
    # カンバンコンテナの開始
    st.markdown('<div class="kanban-container">', unsafe_allow_html=True)
    
    # 4列のカンバンボード
    cols = st.columns(4)
    
    for i, status_info in enumerate(statuses):
        with cols[i]:
            status = status_info['name']
            color = status_info['color']
            
            # カラムヘッダー
            tasks_in_status = [t for t in st.session_state.ai_tasks if t['status'] == status]
            task_count = len(tasks_in_status)
            
            st.markdown(f"""
            <div class="kanban-column">
                <div class="kanban-header" style="color: {color}">
                    <span>{status}</span>
                    <span class="task-count">({task_count})</span>
                </div>
            """, unsafe_allow_html=True)
            
            # タスクカード表示
            for task in tasks_in_status:
                show_ultra_task_card(task)
            
            # 新規タスク追加（To Doカラムのみ）
            if status == 'To Do':
                if st.button("➕ 新規タスク", key=f"add_task_{status}", help="新しいタスクを追加"):
                    st.session_state.show_new_task_form = True
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_ultra_task_card(task):
    """超リアルAsanaタスクカード"""
    # 優先度クラス
    priority_class = f"priority-{task['priority'].lower()}" if task['priority'] in ['高', '中', '低'] else "priority-medium"
    
    # サブタスク進捗計算
    subtask_progress = 0
    if task.get('subtasks'):
        completed_subtasks = len([s for s in task['subtasks'] if s['completed']])
        total_subtasks = len(task['subtasks'])
        subtask_progress = (completed_subtasks / total_subtasks) * 100 if total_subtasks > 0 else 0
        subtask_text = f"{completed_subtasks}/{total_subtasks}"
    else:
        subtask_text = "0/0"
    
    # タスクカードHTML
    card_id = f"task_card_{task['id']}"
    
    card_html = f"""
    <div class="task-card" id="{card_id}">
        <div class="priority-indicator {priority_class}"></div>
        <div class="task-card-inner">
            <div class="task-header">
                <h4 class="task-title">{task['name']}</h4>
                <div class="task-actions">
                    <button class="action-btn" title="詳細">👁️</button>
                </div>
            </div>
            
            <div class="task-tags">
                {('<span class="tag tag-ai">🤖 AI</span>' if task.get('created_from_message') else '')}
                <span class="tag tag-project">{task.get('project', '')}</span>
                <span class="tag tag-category">{task.get('priority', '')}</span>
            </div>
            
            <div class="task-meta">
                <div class="subtask-progress">
                    <span>📝 {subtask_text}</span>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {subtask_progress}%"></div>
                    </div>
                </div>
                <div>
                    <small>⏰ {task.get('due_date', '')} | 👤 {task.get('assignee', '')}</small>
                </div>
            </div>
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)
    
    # インタラクションボタン
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        if st.button("📖 詳細表示", key=f"detail_{task['id']}", help="タスク詳細をモーダルで表示"):
            st.session_state.selected_task_id = task['id']
            st.session_state.show_task_modal = True
            st.rerun()
    
    with col2:
        # 前のステータスに移動
        prev_status = get_prev_status(task['status'])
        if prev_status != task['status']:
            if st.button("◀️", key=f"prev_{task['id']}", help=f"{prev_status}に移動"):
                update_task_status(task['id'], prev_status)
                st.success(f"「{task['name']}」を「{prev_status}」に移動しました")
                st.rerun()
    
    with col3:
        # 次のステータスに移動
        next_status = get_next_status(task['status'])
        if next_status != task['status']:
            if st.button("▶️", key=f"next_{task['id']}", help=f"{next_status}に移動"):
                update_task_status(task['id'], next_status)
                st.success(f"「{task['name']}」を「{next_status}」に移動しました")
                st.rerun()
    
    with col4:
        if st.button("🗑️", key=f"delete_{task['id']}", help="タスクを削除"):
            if st.session_state.get(f"confirm_delete_{task['id']}", False):
                st.session_state.ai_tasks = [t for t in st.session_state.ai_tasks if t['id'] != task['id']]
                st.success("タスクを削除しました")
                st.rerun()
            else:
                st.session_state[f"confirm_delete_{task['id']}"] = True
                st.warning("もう一度クリックすると削除されます")

def show_task_modal():
    """タスク詳細モーダル"""
    if not st.session_state.show_task_modal or not st.session_state.selected_task_id:
        return
    
    task = get_task_by_id(st.session_state.selected_task_id)
    if not task:
        st.error("タスクが見つかりません")
        return
    
    # モーダルオーバーレイ
    st.markdown("""
    <div class="modal-overlay" onclick="closeModal()">
        <div class="modal-content" onclick="event.stopPropagation()">
    """, unsafe_allow_html=True)
    
    # モーダルヘッダー
    col1, col2 = st.columns([5, 1])
    
    with col1:
        st.markdown(f"# {task['name']}")
        if task.get('created_from_message'):
            st.caption(f"🤖 AIが自動生成 | 📧 {task['source_message']['sender']} - {task['source_message']['subject']}")
    
    with col2:
        if st.button("✖️", key="close_modal", help="モーダルを閉じる"):
            st.session_state.show_task_modal = False
            st.rerun()
    
    st.markdown("---")
    
    # 基本情報
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📊 基本情報")
        
        # ステータス変更
        current_status = task['status']
        new_status = st.selectbox(
            "ステータス",
            ['To Do', '進行中', 'レビュー中', '完了'],
            index=['To Do', '進行中', 'レビュー中', '完了'].index(current_status),
            key=f"modal_status_{task['id']}"
        )
        
        if new_status != current_status:
            update_task_status(task['id'], new_status)
            st.success(f"ステータスを「{new_status}」に変更しました")
            st.rerun()
        
        # その他の基本情報
        st.write(f"**優先度:** {task['priority']}")
        st.write(f"**担当者:** {task.get('assignee', '')}")
        st.write(f"**期限:** {task.get('due_date', '')}")
    
    with col2:
        st.markdown("#### 📁 プロジェクト情報")
        st.write(f"**プロジェクト:** {task.get('project', '')}")
        st.write(f"**推定時間:** {task.get('estimated_time', '')}")
        st.write(f"**作成日時:** {task.get('created_at', '')}")
    
    with col3:
        st.markdown("#### 🏷️ タグ")
        if task.get('tags'):
            for tag in task['tags']:
                st.markdown(f"`{tag}`")
    
    # 説明
    st.markdown("#### 📝 説明")
    st.text_area(
        "説明",
        value=task.get('description', ''),
        key=f"modal_desc_{task['id']}",
        height=100,
        label_visibility="collapsed"
    )
    
    # サブタスク
    st.markdown("#### ✅ サブタスク")
    
    if task.get('subtasks'):
        for i, subtask in enumerate(task['subtasks']):
            col1, col2 = st.columns([5, 1])
            
            with col1:
                # チェックボックスでサブタスクの完了状態を管理
                completed = st.checkbox(
                    subtask['name'], 
                    value=subtask['completed'],
                    key=f"modal_subtask_{task['id']}_{subtask['id']}"
                )
                
                # 状態が変更された場合
                if completed != subtask['completed']:
                    subtask['completed'] = completed
                    if completed:
                        st.success(f"サブタスク「{subtask['name']}」を完了しました！")
                    else:
                        st.info(f"サブタスク「{subtask['name']}」を未完了に戻しました")
                    st.rerun()
            
            with col2:
                st.write("✅" if subtask['completed'] else "⭕")
    
    # サブタスク追加
    with st.expander("➕ サブタスクを追加"):
        new_subtask_name = st.text_input("サブタスク名", key=f"modal_new_subtask_{task['id']}")
        if st.button("追加", key=f"modal_add_subtask_{task['id']}"):
            if new_subtask_name:
                if 'subtasks' not in task:
                    task['subtasks'] = []
                
                new_subtask = {
                    'id': len(task['subtasks']) + 1,
                    'name': new_subtask_name,
                    'completed': False
                }
                task['subtasks'].append(new_subtask)
                st.success(f"サブタスク「{new_subtask_name}」を追加しました！")
                st.rerun()
    
    # コメント
    st.markdown("#### 💬 コメント")
    
    # 既存コメント
    if task.get('comments'):
        for comment in task['comments']:
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 12px; border-radius: 8px; margin-bottom: 8px;">
                <strong>{comment['author']}</strong> <small>{comment['timestamp']}</small><br>
                {comment['text']}
            </div>
            """, unsafe_allow_html=True)
    
    # 新しいコメント
    new_comment = st.text_area("新しいコメント", key=f"modal_new_comment_{task['id']}")
    if st.button("コメント追加", key=f"modal_add_comment_{task['id']}"):
        if new_comment:
            if 'comments' not in task:
                task['comments'] = []
            
            comment = {
                'author': '自分',
                'text': new_comment,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
            task['comments'].append(comment)
            st.success("コメントを追加しました！")
            st.rerun()
    
    # 完了条件
    if task.get('completion_criteria'):
        st.markdown("#### 🎯 完了条件")
        st.info(task['completion_criteria'])
    
    # アクションボタン
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if task['status'] != '完了':
            if st.button("✅ 完了にする", type="primary", key=f"modal_complete_{task['id']}"):
                update_task_status(task['id'], '完了')
                st.success("タスクを完了にしました！")
                st.balloons()
                st.rerun()
    
    with col2:
        if st.button("📋 複製", key=f"modal_duplicate_{task['id']}"):
            # タスクの複製
            new_task = task.copy()
            new_task['id'] = st.session_state.task_counter
            new_task['name'] = f"{task['name']} (コピー)"
            new_task['status'] = 'To Do'
            new_task['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            
            st.session_state.ai_tasks.append(new_task)
            st.session_state.task_counter += 1
            st.success("タスクを複製しました！")
    
    with col3:
        if st.button("🗑️ 削除", key=f"modal_delete_{task['id']}"):
            st.session_state.ai_tasks = [t for t in st.session_state.ai_tasks if t['id'] != task['id']]
            st.session_state.show_task_modal = False
            st.success("タスクを削除しました")
            st.rerun()
    
    with col4:
        if st.button("📤 共有", key=f"modal_share_{task['id']}"):
            st.info("共有機能は開発中です")
    
    st.markdown('</div></div>', unsafe_allow_html=True)

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
    
    # メッセージ一覧表示（簡略版 - タスク管理に集中するため）
    for msg in messages:
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"{msg['priority']} **{msg['subject']}** - {msg['sender']} ({msg['time']})")
                st.caption(f"📝 AI要約: {msg['ai_summary']}")
                tag_text = " ".join([f"`{tag}`" for tag in msg['tags']])
                st.markdown(f"🏷️ {tag_text}")
            
            with col2:
                if st.button("📋 Asanaタスク作成", key=f"asana_task_{msg['sender']}", type="primary"):
                    # Asana風タスクを自動作成
                    task_data = {
                        'タスク名': f"{msg['subject']}への対応",
                        '詳細説明': f"{msg['sender']}さんからの{msg['subject']}に対して適切に対応する",
                        '期限': '明日 17:00',
                        '優先度': msg['priority'].split()[1] if len(msg['priority'].split()) > 1 else '中',
                        'カテゴリ': 'コミュニケーション',
                        '推定時間': msg['estimated_time'],
                        'サブタスク': f"メッセージ内容の確認\n対応方針の決定\n{msg['sender']}さんへの返信"
                    }
                    
                    created_task = add_ai_task(msg, task_data)
                    st.success(f"✅ Asana風タスク「{created_task['name']}」を作成しました！")
                    st.info("📋 タスク管理ページのカンバンボードで確認できます")
            
            st.markdown("---")

def show_tasks():
    """超リアルAsana風タスク管理表示"""
    st.title("📋 超リアルAsana風タスク管理")
    
    initialize_session_state()
    
    # タスクモーダルの表示
    if st.session_state.show_task_modal:
        show_task_modal()
    
    # ビュー切り替え
    view_tabs = st.tabs(["📋 カンバンボード", "📊 リストビュー", "📈 プロジェクトビュー"])
    
    with view_tabs[0]:
        # カンバンボード表示
        show_ultra_asana_kanban()
    
    with view_tabs[1]:
        st.markdown("### 📊 タスクリスト")
        
        # テーブル形式でタスク一覧表示
        if st.session_state.ai_tasks:
            for task in st.session_state.ai_tasks:
                col1, col2, col3, col4, col5, col6 = st.columns([3, 1, 1, 1, 1, 1])
                
                with col1:
                    task_name = task['name']
                    if task.get('created_from_message'):
                        task_name += " 🤖"
                    st.write(f"**{task_name}**")
                    st.caption(f"📁 {task.get('project', '')}")
                
                with col2:
                    priority_colors = {"高": "🔴", "中": "🟡", "低": "🟢"}
                    st.write(f"{priority_colors.get(task['priority'], '📊')} {task['priority']}")
                
                with col3:
                    status_colors = {
                        "To Do": "⭕", "進行中": "🔄", 
                        "レビュー中": "👀", "完了": "✅"
                    }
                    st.write(f"{status_colors.get(task['status'], '📋')} {task['status']}")
                
                with col4:
                    st.write(f"⏰ {task.get('due_date', '')}")
                
                with col5:
                    if task.get('subtasks'):
                        completed = len([s for s in task['subtasks'] if s['completed']])
                        total = len(task['subtasks'])
                        st.write(f"📝 {completed}/{total}")
                    else:
                        st.write("➖")
                
                with col6:
                    if st.button("📖", key=f"list_detail_{task['id']}", help="詳細表示"):
                        st.session_state.selected_task_id = task['id']
                        st.session_state.show_task_modal = True
                        st.rerun()
                
                st.markdown("---")
        else:
            st.info("タスクがありません")
    
    with view_tabs[2]:
        st.markdown("### 📈 プロジェクトビュー")
        
        for project in st.session_state.projects:
            with st.expander(f"📁 {project['name']}", expanded=True):
                # プロジェクト情報
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**説明:** {project['description']}")
                    st.progress(project['progress'] / 100, text=f"進捗: {project['progress']}%")
                
                with col2:
                    st.write(f"**ステータス:** {project['status']}")
                
                # プロジェクト関連タスク
                project_tasks = [t for t in st.session_state.ai_tasks if t.get('project') == project['name']]
                
                if project_tasks:
                    st.markdown("#### 関連タスク")
                    
                    for task in project_tasks:
                        col1, col2, col3 = st.columns([3, 1, 1])
                        
                        with col1:
                            st.write(f"• **{task['name']}**")
                        
                        with col2:
                            priority_colors = {"高": "🔴", "中": "🟡", "低": "🟢"}
                            st.write(f"{priority_colors.get(task['priority'], '📊')} {task['priority']}")
                        
                        with col3:
                            status_colors = {
                                "To Do": "⭕", "進行中": "🔄",
                                "レビュー中": "👀", "完了": "✅"
                            }
                            st.write(f"{status_colors.get(task['status'], '📋')} {task['status']}")
                else:
                    st.info("関連タスクがありません")

def show_projects():
    """プロジェクト管理表示"""
    st.title("📁 プロジェクト管理")
    
    initialize_session_state()
    
    st.markdown("### 📊 プロジェクト一覧")
    
    for project in st.session_state.projects:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"## {project['name']}")
                st.write(f"**説明:** {project['description']}")
                st.progress(project['progress'] / 100, text=f"進捗: {project['progress']}%")
                
                # プロジェクト関連統計
                project_tasks = [t for t in st.session_state.ai_tasks if t.get('project') == project['name']]
                completed_tasks = [t for t in project_tasks if t['status'] == '完了']
                
                st.caption(f"📋 タスク: {len(completed_tasks)}/{len(project_tasks)} 完了")
            
            with col2:
                st.markdown("#### ステータス")
                st.write(f"**{project['status']}**")
                
                st.markdown("#### アクション")
                if st.button("📋 タスク表示", key=f"project_tasks_{project['id']}"):
                    st.info(f"{project['name']}のタスクをフィルタリングしました")
            
            with col3:
                st.markdown("#### 進捗")
                status_icon = "🟢" if project['progress'] >= 80 else "🟡" if project['progress'] >= 50 else "🔴"
                st.write(f"{status_icon} {project['progress']}%")
            
            st.markdown("---")

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
        st.sidebar.success("🤖 AI: 超Asana統合")
        st.sidebar.write("📋 カンバン・詳細・分析・返信")
    else:
        st.sidebar.warning("🤖 AI: テストモード")
    
    st.sidebar.markdown("---")
    
    # ナビゲーション
    page = st.sidebar.selectbox(
        "メニュー",
        ["📊 ダッシュボード", "💬 コミュニケーション", "📋 タスク管理", "📁 プロジェクト管理"]
    )
    
    st.sidebar.markdown("---")
    
    # 超Asana風統計表示
    st.sidebar.markdown("### 📋 超Asana統計")
    
    todo_count = len([t for t in st.session_state.ai_tasks if t['status'] == 'To Do'])
    progress_count = len([t for t in st.session_state.ai_tasks if t['status'] == '進行中'])
    review_count = len([t for t in st.session_state.ai_tasks if t['status'] == 'レビュー中'])
    completed_count = len([t for t in st.session_state.ai_tasks if t['status'] == '完了'])
    
    st.sidebar.write(f"📋 To Do: {todo_count}件")
    st.sidebar.write(f"🔄 進行中: {progress_count}件") 
    st.sidebar.write(f"👀 レビュー中: {review_count}件")
    st.sidebar.write(f"✅ 完了: {completed_count}件")
    
    # 進捗表示
    total_tasks = len(st.session_state.ai_tasks)
    completion_rate = completed_count / total_tasks if total_tasks > 0 else 0
    
    st.sidebar.markdown("### 📈 超Asana効率")
    st.sidebar.progress(completion_rate, text=f"完了率: {int(completion_rate * 100)}%")
    st.sidebar.write("🎯 体験向上: 98%")
    
    st.sidebar.markdown("---")
    
    if st.sidebar.button("ログアウト"):
        st.session_state.authenticated = False
        st.rerun()
    
    # ページ表示
    if page == "📊 ダッシュボード":
        show_dashboard()
    elif page == "💬 コミュニケーション":
        show_communication()
    elif page == "📋 タスク管理":
        show_tasks()
    elif page == "📁 プロジェクト管理":
        show_projects()

if __name__ == "__main__":
    main()