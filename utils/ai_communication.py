"""
BizFlow AI MVP - AI コミュニケーション支援
"""

import streamlit as st
import google.generativeai as genai
from config.config import AI_MODELS
import json
from datetime import datetime

class AICommunicationHelper:
    def __init__(self):
        self.setup_ai()
    
    def setup_ai(self):
        """AI APIの設定"""
        try:
            # Gemini API設定
            if AI_MODELS["models"]["gemini"]["api_key"] and AI_MODELS["models"]["gemini"]["api_key"] != "test-gemini-api-key-12345":
                genai.configure(api_key=AI_MODELS["models"]["gemini"]["api_key"])
                self.ai_available = True
            else:
                self.ai_available = False
        except Exception as e:
            self.ai_available = False
            st.error(f"AI設定エラー: {str(e)}")
    
    def analyze_message_priority(self, message):
        """メッセージの重要度を分析"""
        
        # 緊急度判定キーワード
        urgent_keywords = ['緊急', '至急', '今日中', 'ASAP', '急ぎ', '重要', '締切']
        high_priority_senders = ['クライアント', '顧客', 'CEO', '重要']
        
        importance_score = 1  # デフォルト：低
        
        # キーワードチェック
        for keyword in urgent_keywords:
            if keyword in message.get('subject', '') or keyword in message.get('preview', ''):
                importance_score = max(importance_score, 3)  # 高
        
        # 送信者チェック
        sender = message.get('sender', '').lower()
        for priority_sender in high_priority_senders:
            if priority_sender.lower() in sender:
                importance_score = max(importance_score, 2)  # 中
        
        # 時間的要素
        if 'today' in message.get('preview', '').lower() or '今日' in message.get('preview', ''):
            importance_score = max(importance_score, 3)
        
        priority_labels = {1: '低', 2: '中', 3: '高'}
        return priority_labels.get(importance_score, '低')
    
    def generate_reply_suggestions(self, message, reply_tone='丁寧・フォーマル', context=None):
        """AI返信案生成"""
        
        if not self.ai_available:
            return self._generate_template_replies(message, reply_tone)
        
        try:
            # Gemini用プロンプト作成
            prompt = self._create_reply_prompt(message, reply_tone, context)
            
            # Gemini API呼び出し（実際のAPIキーが設定されている場合）
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            
            # 返信案をパース
            replies = self._parse_ai_response(response.text)
            return replies
            
        except Exception as e:
            st.warning(f"AI生成中にエラーが発生しました: {str(e)}")
            return self._generate_template_replies(message, reply_tone)
    
    def _create_reply_prompt(self, message, tone, context):
        """AI用プロンプト作成"""
        
        tone_instructions = {
            '丁寧・フォーマル': '敬語を使い、ビジネスマナーに配慮した丁寧な返信',
            'カジュアル・親しみやすい': 'フレンドリーで親しみやすく、でもプロフェッショナルな返信',
            '簡潔・ビジネスライク': '要点を簡潔にまとめた効率的な返信'
        }
        
        prompt = f"""
あなたは優秀なビジネスアシスタントです。以下のメッセージに対する返信を作成してください。

## 受信メッセージ情報
送信者: {message.get('sender', 'Unknown')}
件名: {message.get('subject', 'No Subject')}
内容: {message.get('preview', 'No Content')}
送信元: {message.get('source', 'Unknown')}

## 返信の要件
- トーン: {tone_instructions.get(tone, '丁寧・フォーマル')}
- 3つの異なるバリエーションを作成
- 各返信は100-200文字程度
- 相手の質問やリクエストに適切に応答

## 出力形式
以下のJSON形式で出力してください：
{{
    "replies": [
        {{
            "version": "即座に対応版",
            "content": "返信内容1"
        }},
        {{
            "version": "詳細確認版", 
            "content": "返信内容2"
        }},
        {{
            "version": "簡潔回答版",
            "content": "返信内容3"
        }}
    ]
}}
"""
        return prompt
    
    def _parse_ai_response(self, response_text):
        """AI応答をパース"""
        try:
            # JSON部分を抽出
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            json_str = response_text[start:end]
            
            data = json.loads(json_str)
            return data.get('replies', [])
        except:
            # パースに失敗した場合はテンプレート返信
            return []
    
    def _generate_template_replies(self, message, tone):
        """テンプレート返信生成（AI利用不可時）"""
        
        sender_name = message.get('sender', '').split('(')[0].strip()
        
        if tone == '丁寧・フォーマル':
            return [
                {
                    "version": "確認・対応版",
                    "content": f"{sender_name}さん\n\nお疲れ様です。ご連絡いただきありがとうございます。\n内容を確認し、後ほど詳細をお返事いたします。\n\nよろしくお願いいたします。"
                },
                {
                    "version": "質問・詳細確認版",
                    "content": f"{sender_name}さん\n\nお疲れ様です。\nご連絡の件について、いくつか確認させていただきたい点がございます。お時間のある時にお聞かせください。\n\nよろしくお願いいたします。"
                },
                {
                    "version": "承諾・進行版",
                    "content": f"{sender_name}さん\n\nお疲れ様です。\n承知いたしました。こちらで対応させていただきます。\n進捗については改めてご報告いたします。\n\nよろしくお願いいたします。"
                }
            ]
        
        elif tone == 'カジュアル・親しみやすい':
            return [
                {
                    "version": "確認・対応版", 
                    "content": f"{sender_name}さん\n\nお疲れ様です！\nメッセージありがとうございます。確認して返事しますね。\n\nよろしくお願いします。"
                },
                {
                    "version": "質問・詳細確認版",
                    "content": f"{sender_name}さん\n\nお疲れ様です！\nいくつか確認したいことがあるので、お時間のある時に教えてください。\n\nよろしくお願いします。"
                },
                {
                    "version": "承諾・進行版",
                    "content": f"{sender_name}さん\n\nお疲れ様です！\n了解しました。こちらで進めさせていただきますね。\n\nありがとうございます。"
                }
            ]
        
        else:  # 簡潔・ビジネスライク
            return [
                {
                    "version": "確認・対応版",
                    "content": f"{sender_name}さん\n\n確認いたします。後ほど回答いたします。"
                },
                {
                    "version": "質問・詳細確認版", 
                    "content": f"{sender_name}さん\n\n詳細を確認させてください。追ってご連絡いたします。"
                },
                {
                    "version": "承諾・進行版",
                    "content": f"{sender_name}さん\n\n承知いたしました。対応いたします。"
                }
            ]
    
    def suggest_reply_timing(self, message, current_time=None):
        """返信タイミングの提案"""
        
        if current_time is None:
            current_time = datetime.now()
        
        priority = self.analyze_message_priority(message)
        
        suggestions = []
        
        if priority == '高':
            suggestions = [
                {'timing': '今すぐ', 'reason': '緊急度が高いため'},
                {'timing': '30分以内', 'reason': '詳細確認後に返信'},
                {'timing': '1時間以内', 'reason': '関係者と相談後に返信'}
            ]
        elif priority == '中':
            suggestions = [
                {'timing': '今すぐ', 'reason': '簡潔に確認の返信'},
                {'timing': '今日中', 'reason': '詳細を準備してから返信'},
                {'timing': '明日朝一', 'reason': '翌営業日に丁寧に対応'}
            ]
        else:  # 低
            suggestions = [
                {'timing': '今日中', 'reason': '本日中に返信'},
                {'timing': '明日', 'reason': '翌営業日に返信'},
                {'timing': '3日以内', 'reason': '週内に返信で十分'}
            ]
        
        return suggestions
    
    def create_followup_task(self, message, reply_content, followup_timing):
        """フォローアップタスクの作成"""
        
        task = {
            'name': f"{message.get('sender', 'Unknown')}への回答フォローアップ",
            'description': f"件名「{message.get('subject', '')}」に関する追加対応",
            'due_date': followup_timing,
            'priority': self.analyze_message_priority(message),
            'status': '未着手',
            'related_message': message,
            'original_reply': reply_content
        }
        
        return task