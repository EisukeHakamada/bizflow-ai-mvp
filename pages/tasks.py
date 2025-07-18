"""
BizFlow AI MVP - タスク管理ページ
"""

import streamlit as st
from utils.database import get_user_data, save_user_data, update_user_data, delete_user_data
from datetime import datetime, date
import uuid

def show():
    """タスク管理ページの表示"""
    
    st.title("✅ タスク管理")
    
    # タブ分け
    tab1, tab2, tab3 = st.tabs(["📋 タスク一覧", "➕ 新規作成", "🤖 AI提案"])
    
    with tab1:
        show_task_list()
    
    with tab2:
        show_new_task_form()
    
    with tab3:
        show_ai_suggestions()

def show_task_list():
    """タスク一覧の表示"""
    
    st.markdown("### タスク一覧")
    
    # フィルタリングオプション
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.selectbox(
            "ステータス",
            ["全て", "未着手", "進行中", "完了", "保留"]
        )
    
    with col2:
        business_filter = st.selectbox(
            "担当事業",
            ["全て", "事業A", "事業B", "事業C", "個人"]
        )
    
    with col3:
        priority_filter = st.selectbox(
            "優先度",
            ["全て", "高", "中", "低"]
        )
    
    # サンプルタスクデータ
    sample_tasks = [
        {
            "id": "task_1",
            "name": "クライアントA向けプロポーザル作成",
            "business": "事業A",
            "due_date": "2025-07-18",
            "status": "進行中",
            "priority": "高",
            "assignee": "自分",
            "project": "プロジェクトX",
            "notes": "技術仕様を詳しく記載する必要あり"
        },
        {
            "id": "task_2",
            "name": "週次ミーティング資料準備",
            "business": "事業B",
            "due_date": "2025-07-19",
            "status": "未着手",
            "priority": "中",
            "assignee": "自分",
            "project": "チーム運営",
            "notes": "前回の議事録を参考にする"
        },
        {
            "id": "task_3",
            "name": "競合調査レポート",
            "business": "事業A",
            "due_date": "2025-07-22",
            "status": "未着手",
            "priority": "低",
            "assignee": "自分",
            "project": "市場分析",
            "notes": "3社以上を詳細調査"
        }
    ]
    
    # タスク表示
    for task in sample_tasks:
        # フィルタリング
        if status_filter != "全て" and task["status"] != status_filter:
            continue
        if business_filter != "全て" and task["business"] != business_filter:
            continue
        if priority_filter != "全て" and task["priority"] != priority_filter:
            continue
        
        # 優先度に応じた色分け
        priority_color = {
            "高": "🔴",
            "中": "🟡", 
            "低": "🟢"
        }
        
        status_color = {
            "未着手": "⚪",
            "進行中": "🔵",
            "完了": "✅",
            "保留": "⏸️"
        }
        
        with st.expander(f"{priority_color[task['priority']]} {status_color[task['status']]} {task['name']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**担当事業:** {task['business']}")
                st.write(f"**期限:** {task['due_date']}")
                st.write(f"**ステータス:** {task['status']}")
                st.write(f"**優先度:** {task['priority']}")
            
            with col2:
                st.write(f"**担当者:** {task['assignee']}")
                st.write(f"**関連プロジェクト:** {task['project']}")
                st.write(f"**備考:** {task['notes']}")
            
            # アクションボタン
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("編集", key=f"edit_{task['id']}"):
                    st.session_state[f"editing_{task['id']}"] = True
            
            with col2:
                if st.button("完了", key=f"complete_{task['id']}"):
                    st.success(f"タスク「{task['name']}」を完了しました！")
            
            with col3:
                if st.button("🤖 次のアクション", key=f"ai_{task['id']}"):
                    show_ai_next_action(task)
            
            with col4:
                if st.button("削除", key=f"delete_{task['id']}"):
                    st.error(f"タスク「{task['name']}」を削除しました")

def show_new_task_form():
    """新規タスク作成フォーム"""
    
    st.markdown("### 新規タスク作成")
    
    with st.form("new_task_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            task_name = st.text_input("タスク名 *", placeholder="例: クライアント向け資料作成")
            business = st.selectbox("担当事業 *", ["事業A", "事業B", "事業C", "個人"])
            due_date = st.date_input("期限", value=date.today())
            priority = st.selectbox("優先度", ["高", "中", "低"], index=1)
        
        with col2:
            status = st.selectbox("ステータス", ["未着手", "進行中", "完了", "保留"])
            assignee = st.text_input("担当者", value="自分")
            project = st.text_input("関連プロジェクト", placeholder="例: プロジェクトX")
            
        notes = st.text_area("備考", placeholder="タスクに関する詳細情報...")
        
        submitted = st.form_submit_button("タスクを作成")
        
        if submitted:
            if task_name:
                # 新規タスクの保存処理
                new_task = {
                    "id": str(uuid.uuid4()),
                    "name": task_name,
                    "business": business,
                    "due_date": str(due_date),
                    "status": status,
                    "priority": priority,
                    "assignee": assignee,
                    "project": project,
                    "notes": notes,
                    "created_at": datetime.now().isoformat()
                }
                
                st.success(f"タスク「{task_name}」を作成しました！")
                st.balloons()
            else:
                st.error("タスク名を入力してください。")

def show_ai_suggestions():
    """AI提案の表示"""
    
    st.markdown("### 🤖 AI による優先度提案")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button("🔄 優先度を再計算"):
            with st.spinner("AIが優先度を計算中..."):
                import time
                time.sleep(2)  # 処理時間をシミュレート
            st.success("優先度を更新しました！")
    
    with col2:
        ai_model = st.selectbox("使用するAIモデル", ["Gemini", "Claude", "GPT-4"])
    
    st.markdown("---")
    
    # AI提案結果
    st.markdown("#### 📊 現在の優先度ランキング")
    
    ai_rankings = [
        {
            "rank": 1,
            "task": "クライアントA向けプロポーザル作成",
            "priority": "高",
            "reason": "明日が締切で、売上に直結する重要案件のため",
            "next_action": "技術仕様セクションの詳細化と最終レビュー",
            "estimated_time": "2-3時間"
        },
        {
            "rank": 2,
            "task": "週次ミーティング資料準備",
            "priority": "中",
            "reason": "明後日のミーティングで必要、チーム運営に重要",
            "next_action": "前回の議事録確認とアジェンダ作成",
            "estimated_time": "1時間"
        },
        {
            "rank": 3,
            "task": "競合調査レポート",
            "priority": "低",
            "reason": "期限まで余裕があり、他のタスクより優先度が低い",
            "next_action": "調査対象企業のリストアップから開始",
            "estimated_time": "3-4時間"
        }
    ]
    
    for ranking in ai_rankings:
        priority_emoji = {"高": "🔴", "中": "🟡", "低": "🟢"}
        
        st.markdown(f"""
        <div class="metric-card priority-{ranking['priority'].lower()}">
            <h4>{ranking['rank']}位. {priority_emoji[ranking['priority']]} {ranking['task']}</h4>
            <p><strong>🎯 次のアクション:</strong> {ranking['next_action']}</p>
            <p><strong>💭 AIの判断理由:</strong> {ranking['reason']}</p>
            <p><strong>⏰ 推定時間:</strong> {ranking['estimated_time']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 個別アクション提案
    st.markdown("#### 🎯 個別タスクのアクション提案")
    
    selected_task = st.selectbox(
        "アクション提案を見たいタスクを選択:",
        ["クライアントA向けプロポーザル作成", "週次ミーティング資料準備", "競合調査レポート"]
    )
    
    if st.button("このタスクのアクション提案を取得"):
        with st.spinner("AIがアクション提案を生成中..."):
            import time
            time.sleep(1)
        
        task_actions = {
            "クライアントA向けプロポーザル作成": [
                "📝 技術仕様セクションの詳細化（30分）",
                "📋 価格設定の最終確認（15分）",
                "👥 チームメンバーによる内容レビュー（45分）",
                "📧 クライアントへの事前確認事項をメール送信（10分）",
                "📄 最終フォーマット調整とPDF化（20分）"
            ],
            "週次ミーティング資料準備": [
                "📰 前回議事録の確認と課題整理（20分）",
                "📊 今週の進捗データを収集・整理（30分）",
                "📝 アジェンダ作成と時間配分設定（15分）",
                "📈 来週の目標設定（20分）"
            ],
            "競合調査レポート": [
                "🔍 調査対象企業のリストアップ（30分）",
                "🌐 各社のWebサイトと公開情報の収集（2時間）",
                "📊 価格・サービス比較表の作成（1時間）",
                "📝 分析結果のまとめと考察（1時間）"
            ]
        }
        
        st.markdown(f"**{selected_task}** の推奨アクション:")
        for action in task_actions[selected_task]:
            st.markdown(f"- {action}")

def show_ai_next_action(task):
    """個別タスクのAI提案"""
    st.info(f"**{task['name']}** の次のアクション提案:\n\n"
            f"🎯 **推奨アクション:** {task['notes']}を完了させるため、まず関連資料を収集してください\n\n"
            f"⏰ **推定時間:** 30-45分\n\n"
            f"💡 **ヒント:** 過去の類似プロジェクトを参考にすると効率的です")