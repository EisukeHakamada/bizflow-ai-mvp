import React, { useEffect, useState } from 'react';
import KanbanBoard from './components/KanbanBoard';
import { setupInitialData } from './firebase/config';
import { Loader2, AlertCircle, Wifi, WifiOff } from 'lucide-react';
import './index.css';

function App() {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    // 初期データセットアップ
    const initializeApp = async () => {
      try {
        setIsLoading(true);
        await setupInitialData();
        setError(null);
      } catch (err) {
        console.error('アプリケーションの初期化に失敗しました:', err);
        setError('アプリケーションの初期化に失敗しました。ページを再読み込みしてください。');
      } finally {
        setIsLoading(false);
      }
    };

    initializeApp();
  }, []);

  useEffect(() => {
    // オンライン/オフライン状態の監視
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // URLパラメータから設定を取得
  const urlParams = new URLSearchParams(window.location.search);
  const isMobileView = urlParams.get('mobile') === 'true';
  const projectId = urlParams.get('project') || 'default';

  // ローディング状態
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="bg-white rounded-xl shadow-soft p-8 text-center">
          <Loader2 className="w-12 h-12 text-blue-600 animate-spin mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-800 mb-2">
            カンバンボードを読み込み中...
          </h2>
          <p className="text-gray-600">
            初期データを準備しています
          </p>
        </div>
      </div>
    );
  }

  // エラー状態
  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-red-50 to-pink-100 flex items-center justify-center">
        <div className="bg-white rounded-xl shadow-soft p-8 text-center max-w-md">
          <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-800 mb-2">
            エラーが発生しました
          </h2>
          <p className="text-gray-600 mb-6">
            {error}
          </p>
          <button
            onClick={() => window.location.reload()}
            className="btn btn-primary"
          >
            ページを再読み込み
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={`min-h-screen ${isMobileView ? 'mobile-view' : ''}`}>
      {/* オフライン通知 */}
      {!isOnline && (
        <div className="fixed top-0 left-0 right-0 bg-yellow-500 text-white px-4 py-2 text-center z-50">
          <div className="flex items-center justify-center gap-2">
            <WifiOff size={16} />
            <span className="text-sm font-medium">
              オフラインモードです。変更内容は接続復旧時に同期されます。
            </span>
          </div>
        </div>
      )}

      {/* オンライン復旧通知 */}
      {isOnline && (
        <div className="fixed top-0 left-0 right-0 bg-green-500 text-white px-4 py-2 text-center z-50 transition-all duration-300">
          <div className="flex items-center justify-center gap-2">
            <Wifi size={16} />
            <span className="text-sm font-medium">
              オンラインに復旧しました
            </span>
          </div>
        </div>
      )}

      {/* メインコンテンツ */}
      <div className={isOnline ? '' : 'pt-12'}>
        <KanbanBoard 
          projectId={projectId}
          isMobileView={isMobileView}
          isOffline={!isOnline}
        />
      </div>

      {/* フッター（デバッグ情報） */}
      {process.env.NODE_ENV === 'development' && (
        <div className="fixed bottom-4 right-4 bg-black bg-opacity-50 text-white text-xs px-3 py-2 rounded-lg">
          <div>Project: {projectId}</div>
          <div>Mobile: {isMobileView ? 'Yes' : 'No'}</div>
          <div>Online: {isOnline ? 'Yes' : 'No'}</div>
          <div>Env: {process.env.NODE_ENV}</div>
        </div>
      )}
    </div>
  );
}

export default App;