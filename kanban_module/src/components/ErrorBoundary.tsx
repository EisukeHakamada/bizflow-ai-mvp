import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle, RefreshCw, Home } from 'lucide-react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  static getDerivedStateFromError(error: Error): State {
    return {
      hasError: true,
      error,
      errorInfo: null,
    };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
    
    this.setState({
      error,
      errorInfo,
    });

    // エラーログをサーバーに送信（本番環境では実装）
    if (process.env.NODE_ENV === 'production') {
      // TODO: エラーログ送信
      this.logErrorToService(error, errorInfo);
    }
  }

  private logErrorToService(error: Error, errorInfo: ErrorInfo) {
    // エラーログサービスへの送信
    try {
      // 例: Sentry, LogRocket, など
      console.log('Error logged to service:', { error, errorInfo });
    } catch (logError) {
      console.error('Failed to log error:', logError);
    }
  }

  private handleReload = () => {
    window.location.reload();
  };

  private handleGoHome = () => {
    window.location.href = '/';
  };

  private handleRetry = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    });
  };

  render() {
    if (this.state.hasError) {
      const { error, errorInfo } = this.state;
      const isDevelopment = process.env.NODE_ENV === 'development';

      return (
        <div className="min-h-screen bg-gradient-to-br from-red-50 to-pink-100 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-strong max-w-2xl w-full p-8">
            {/* ヘッダー */}
            <div className="text-center mb-8">
              <AlertTriangle className="w-16 h-16 text-red-500 mx-auto mb-4" />
              <h1 className="text-2xl font-bold text-gray-900 mb-2">
                申し訳ございません
              </h1>
              <p className="text-gray-600">
                予期しないエラーが発生しました。以下のボタンからお試しください。
              </p>
            </div>

            {/* アクションボタン */}
            <div className="flex flex-col sm:flex-row gap-4 mb-8">
              <button
                onClick={this.handleRetry}
                className="flex items-center justify-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <RefreshCw size={20} />
                再試行
              </button>
              <button
                onClick={this.handleReload}
                className="flex items-center justify-center gap-2 px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
              >
                <RefreshCw size={20} />
                ページを再読み込み
              </button>
              <button
                onClick={this.handleGoHome}
                className="flex items-center justify-center gap-2 px-6 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
              >
                <Home size={20} />
                ホームに戻る
              </button>
            </div>

            {/* 詳細情報（開発環境のみ） */}
            {isDevelopment && error && (
              <div className="border-t border-gray-200 pt-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">
                  開発者向け情報
                </h2>
                
                {/* エラーメッセージ */}
                <div className="mb-4">
                  <h3 className="text-sm font-medium text-gray-700 mb-2">
                    エラーメッセージ:
                  </h3>
                  <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                    <code className="text-red-800 text-sm">
                      {error.message}
                    </code>
                  </div>
                </div>

                {/* スタックトレース */}
                <div className="mb-4">
                  <h3 className="text-sm font-medium text-gray-700 mb-2">
                    スタックトレース:
                  </h3>
                  <div className="bg-gray-50 border border-gray-200 rounded-lg p-3 max-h-64 overflow-y-auto">
                    <pre className="text-gray-800 text-xs whitespace-pre-wrap">
                      {error.stack}
                    </pre>
                  </div>
                </div>

                {/* コンポーネントスタック */}
                {errorInfo && (
                  <div>
                    <h3 className="text-sm font-medium text-gray-700 mb-2">
                      コンポーネントスタック:
                    </h3>
                    <div className="bg-gray-50 border border-gray-200 rounded-lg p-3 max-h-64 overflow-y-auto">
                      <pre className="text-gray-800 text-xs whitespace-pre-wrap">
                        {errorInfo.componentStack}
                      </pre>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* ユーザー向け情報 */}
            {!isDevelopment && (
              <div className="border-t border-gray-200 pt-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">
                  問題が続く場合
                </h2>
                <div className="text-gray-600 space-y-2">
                  <p>• ブラウザのキャッシュをクリアしてください</p>
                  <p>• ブラウザを最新版にアップデートしてください</p>
                  <p>• 異なるブラウザでお試しください</p>
                  <p>• サポートチームにお問い合わせください</p>
                </div>
                
                <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                  <p className="text-blue-800 text-sm">
                    <strong>エラーID:</strong> {Date.now().toString(36)}
                  </p>
                  <p className="text-blue-700 text-sm mt-1">
                    サポートにお問い合わせの際は、このエラーIDをお伝えください。
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}