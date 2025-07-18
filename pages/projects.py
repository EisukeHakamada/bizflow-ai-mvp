"""
BizFlow AI MVP - プロジェクト管理ページ
"""

import streamlit as st
from datetime import datetime, date
import uuid

def show():
    """プロジェクト管理ページの表示"""
    
    st.title("📁 プロジェクト管理")
    
    # タブ分け
    tab1, tab2 = st.tabs(["📋 プロジェクト一覧", "➕ 新規作成"])
    
    with tab1:
        show_project_list()
    
    with tab2:
        show_new_project_form()

def show_project_list():
    """プロジェクト一覧の表示"""
    
    st.markdown("### プロジェクト一覧")
    
    # フィルタリングオプション
    col1, col2 = st.columns(2)
    
    with col1:
        phase_filter = st.selectbox(
            "フェーズ",
            ["全て", "企画", "設計", "開発", "テスト", "完了"]
        )
    
    with col2:
        business_filter = st.selectbox(
            "担当事業",
            ["全て", "事業A", "事業B", "事業C", "個人"]
        )
    
    # サンプルプロジェクトデータ
    sample_projects = [
        {
            "id": "project_1",
            "name": "プロジェクトX - AI活用システム開発",
            "business": "事業A",
            "phase": "開発",
            "description": "顧客向けAI活用システムの開発プロジェクト。機械学習モデルの実装と管理画面の構築が主な作業内容。",
            "goal": "3ヶ月以内にMVPをリリースし、月間売上300万円を達成",
            "start_date": "2025-06-01",
            "end_date": "2025-09-01",
            "progress": 65,
            "team_members": ["自分", "エンジニアA", "デザイナーB"],
            "related_tasks": 8,
            "related_contacts": 5
        },
        {
            "id": "project_2",
            "name": "マーケティング戦略立案",
            "business": "事業B",
            "phase": "設計",
            "description": "新サービスのマーケティング戦略を立案し、実行計画を策定するプロジェクト。",
            "goal": "6ヶ月以内に新規顧客100社獲得",
            "start_date": "2025-07-01",
            "end_date": "2025-12-31",
            "progress": 30,
            "team_members": ["自分", "マーケターC"],
            "related_tasks": 12,
            "related_contacts": 3
        },
        {
            "id": "project_3",
            "name": "業務効率化ツール導入",
            "business": "個人",
            "phase": "完了",
            "description": "個人の業務効率化のためのツール選定と導入。",
            "goal": "月間作業時間を20%削減",
            "start_date": "2025-05-01",
            "end_date": "2025-06-30",
            "progress": 100,
            "team_members": ["自分"],
            "related_tasks": 5,
            "related_contacts": 2
        }
    ]
    
    # プロジェクト表示
    for project in sample_projects:
        # フィルタリング
        if phase_filter != "全て" and project["phase"] != phase_filter:
            continue
        if business_filter != "全て" and project["business"] != business_filter:
            continue
        
        # フェーズに応じた色分け
        phase_color = {
            "企画": "🟣",
            "設計": "🔵", 
            "開発": "🟡",
            "テスト": "🟠",
            "完了": "🟢"
        }
        
        with st.expander(f"{phase_color[project['phase']]} {project['name']} ({project['progress']}%)"):
            # プロジェクト基本情報
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**担当事業:** {project['business']}")
                st.write(f"**現在のフェーズ:** {project['phase']}")
                st.write(f"**開始日:** {project['start_date']}")
                st.write(f"**終了予定:** {project['end_date']}")
                
                # 進捗バー
                st.progress(project['progress'] / 100)
                st.write(f"進捗: {project['progress']}%")
            
            with col2:
                st.write(f"**チームメンバー:** {', '.join(project['team_members'])}")
                st.write(f"**関連タスク:** {project['related_tasks']}件")
                st.write(f"**関連連絡先:** {project['related_contacts']}件")
            
            # プロジェクト詳細
            st.markdown("**プロジェクト概要:**")
            st.write(project['description'])
            
            st.markdown("**目標:**")
            st.write(project['goal'])
            
            # アクションボタン
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("編集", key=f"edit_proj_{project['id']}"):
                    st.info("編集機能は開発中です")
            
            with col2:
                if st.button("タスク表示", key=f"tasks_proj_{project['id']}"):
                    show_project_tasks(project)
            
            with col3:
                if st.button("🤖 進捗分析", key=f"ai_proj_{project['id']}"):
                    show_ai_project_analysis(project)
            
            with col4:
                if st.button("レポート", key=f"report_proj_{project['id']}"):
                    show_project_report(project)

def show_new_project_form():
    """新規プロジェクト作成フォーム"""
    
    st.markdown("### 新規プロジェクト作成")
    
    with st.form("new_project_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input("プロジェクト名 *", placeholder="例: 新サービス開発プロジェクト")
            business = st.selectbox("担当事業 *", ["事業A", "事業B", "事業C", "個人"])
            phase = st.selectbox("現在のフェーズ", ["企画", "設計", "開発", "テスト", "完了"])
            start_date = st.date_input("開始日", value=date.today())
        
        with col2:
            end_date = st.date_input("終了予定日")
            progress = st.slider("現在の進捗 (%)", 0, 100, 0)
            team_members = st.text_input("チームメンバー", placeholder="例: 自分, メンバーA, メンバーB")
        
        description = st.text_area("プロジェクト概要 *", placeholder="プロジェクトの詳細な説明...")
        goal = st.text_area("目標", placeholder="具体的な成果目標...")
        
        submitted = st.form_submit_button("プロジェクトを作成")
        
        if submitted:
            if project_name and description:
                # 新規プロジェクトの保存処理
                new_project = {
                    "id": str(uuid.uuid4()),
                    "name": project_name,
                    "business": business,
                    "phase": phase,
                    "description": description,
                    "goal": goal,
                    "start_date": str(start_date),
                    "end_date": str(end_date),
                    "progress": progress,
                    "team_members": [member.strip() for member in team_members.split(",") if member.strip()],
                    "created_at": datetime.now().isoformat()
                }
                
                st.success(f"プロジェクト「{project_name}」を作成しました！")
                st.balloons()
            else:
                st.error("プロジェクト名と概要を入力してください。")

def show_project_tasks(project):
    """プロジェクト関連タスクの表示"""
    
    st.info(f"**{project['name']}** の関連タスク:\n\n"
            f"📋 進行中: 3件\n"
            f"✅ 完了: 4件\n"
            f"⏸️ 保留: 1件\n\n"
            f"最新タスク: API仕様書作成 (進行中)")

def show_ai_project_analysis(project):
    """AIによるプロジェクト分析"""
    
    with st.spinner("AIがプロジェクトを分析中..."):
        import time
        time.sleep(2)
    
    st.success(f"**{project['name']} AIプロジェクト分析結果:**")
    
    analysis_result = f"""
    📊 **進捗状況:** 順調 ({project['progress']}%完了)
    
    🎯 **次のマイルストーン:**
    - API設計完了 (予定: 来週)
    - フロントエンド実装開始 (予定: 2週間後)
    
    ⚠️ **リスク要因:**
    - チームメンバーの作業負荷が高い
    - 外部API連携の技術的課題
    
    💡 **推奨アクション:**
    1. チームミーティングでタスク分散を検討
    2. 技術的課題の早期解決のための専門家相談
    3. バッファ期間の確保
    
    📈 **成功確率:** 85%
    """
    
    st.markdown(analysis_result)

def show_project_report(project):
    """プロジェクトレポートの生成"""
    
    st.info(f"**{project['name']}** プロジェクトレポート:\n\n"
            f"📅 **期間:** {project['start_date']} ～ {project['end_date']}\n"
            f"👥 **チーム:** {len(project['team_members'])}名\n"
            f"📊 **進捗:** {project['progress']}%\n"
            f"🎯 **目標達成見込み:** 85%\n\n"
            f"詳細レポートの生成機能は開発中です。")