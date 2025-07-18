class DummyDatabase:
    """開発用のダミーデータベース（Firebase接続できない場合）"""
    
    def __init__(self):
        self.data = {
            'tasks': {},
            'projects': {},
            'contacts': {},
            'messages': {}
        }
    
    def collection(self, collection_name):
        return DummyCollection(self.data, collection_name)

class DummyCollection:
    """ダミーコレクション"""
    
    def __init__(self, data, collection_name):
        self.data = data
        self.collection_name = collection_name
    
    def add(self, document):
        """ドキュメントを追加"""
        doc_id = f"doc_{len(self.data[self.collection_name]) + 1}"
        self.data[self.collection_name][doc_id] = document
        return type('obj', (object,), {'id': doc_id})
    
    def document(self, doc_id):
        return DummyDocument(self.data, self.collection_name, doc_id)
    
    def stream(self):
        """全てのドキュメントを取得"""
        results = []
        for doc_id, doc_data in self.data[self.collection_name].items():
            doc = type('obj', (object,), {
                'id': doc_id,
                'to_dict': lambda: doc_data
            })
            results.append(doc)
        return results

class DummyDocument:
    """ダミードキュメント"""
    
    def __init__(self, data, collection_name, doc_id):
        self.data = data
        self.collection_name = collection_name
        self.doc_id = doc_id
    
    def set(self, document):
        """ドキュメントを設定"""
        self.data[self.collection_name][self.doc_id] = document
    
    def get(self):
        """ドキュメントを取得"""
        doc_data = self.data[self.collection_name].get(self.doc_id, {})
        return type('obj', (object,), {
            'exists': bool(doc_data),
            'to_dict': lambda: doc_data
        })
    
    def update(self, updates):
        """ドキュメントを更新"""
        if self.doc_id in self.data[self.collection_name]:
            self.data[self.collection_name][self.doc_id].update(updates)
    
    def delete(self):
        """ドキュメントを削除"""
        if self.doc_id in self.data[self.collection_name]:
            del self.data[self.collection_name][self.doc_id]

# データベースヘルパー関数
def get_user_data(db, collection_name, user_id):
    """ユーザーのデータを取得"""
    try:
        docs = db.collection(collection_name).stream()
        results = []
        for doc in docs:
            doc_data = doc.to_dict()
            doc_data['id'] = doc.id
            results.append(doc_data)
        return results
    except Exception as e:
        st.error(f"データ取得エラー: {str(e)}")
        return []

def save_user_data(db, collection_name, doc_id, data):
    """ユーザーのデータを保存"""
    try:
        db.collection(collection_name).document(doc_id).set(data)
        return True
    except Exception as e:
        st.error(f"データ保存エラー: {str(e)}")
        return False

def update_user_data(db, collection_name, doc_id, updates):
    """ユーザーのデータを更新"""
    try:
        db.collection(collection_name).document(doc_id).update(updates)
        return True
    except Exception as e:
        st.error(f"データ更新エラー: {str(e)}")
        return False

def delete_user_data(db, collection_name, doc_id):
    """ユーザーのデータを削除"""
    try:
        db.collection(collection_name).document(doc_id).delete()
        return True
    except Exception as e:
        st.error(f"データ削除エラー: {str(e)}")
        return False