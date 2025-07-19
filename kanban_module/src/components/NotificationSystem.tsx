import React, { useEffect } from 'react';
import { CheckCircle, AlertTriangle, XCircle, Info, X } from 'lucide-react';

interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message: string;
  timestamp: Date;
  autoClose?: boolean;
  duration?: number;
}

interface NotificationSystemProps {
  notifications: Notification[];
  onRemove?: (id: string) => void;
}

const NotificationSystem: React.FC<NotificationSystemProps> = ({
  notifications,
  onRemove,
}) => {
  // 自動削除の処理
  useEffect(() => {
    notifications.forEach((notification) => {
      if (notification.autoClose !== false && onRemove) {
        const duration = notification.duration || 5000;
        const timer = setTimeout(() => {
          onRemove(notification.id);
        }, duration);

        return () => clearTimeout(timer);
      }
    });
  }, [notifications, onRemove]);

  const getIcon = (type: string) => {
    switch (type) {
      case 'success':
        return <CheckCircle size={20} className="text-green-500" />;
      case 'error':
        return <XCircle size={20} className="text-red-500" />;
      case 'warning':
        return <AlertTriangle size={20} className="text-yellow-500" />;
      case 'info':
        return <Info size={20} className="text-blue-500" />;
      default:
        return <Info size={20} className="text-gray-500" />;
    }
  };

  const getStyle = (type: string) => {
    switch (type) {
      case 'success':
        return 'bg-green-50 border-green-200 text-green-800';
      case 'error':
        return 'bg-red-50 border-red-200 text-red-800';
      case 'warning':
        return 'bg-yellow-50 border-yellow-200 text-yellow-800';
      case 'info':
        return 'bg-blue-50 border-blue-200 text-blue-800';
      default:
        return 'bg-gray-50 border-gray-200 text-gray-800';
    }
  };

  if (notifications.length === 0) return null;

  return (
    <div className="fixed top-4 right-4 z-50 space-y-2 max-w-sm">
      {notifications.map((notification) => (
        <div
          key={notification.id}
          className={`
            notification
            ${getStyle(notification.type)}
            border rounded-lg shadow-lg p-4
            transform transition-all duration-300 ease-in-out
            animate-slideIn
          `}
          role="alert"
          aria-live="polite"
        >
          <div className="flex items-start gap-3">
            <div className="flex-shrink-0">
              {getIcon(notification.type)}
            </div>
            
            <div className="flex-1 min-w-0">
              <h4 className="font-medium text-sm leading-tight">
                {notification.title}
              </h4>
              {notification.message && (
                <p className="text-sm mt-1 opacity-90">
                  {notification.message}
                </p>
              )}
              <p className="text-xs mt-2 opacity-75">
                {notification.timestamp.toLocaleTimeString('ja-JP')}
              </p>
            </div>
            
            {onRemove && (
              <button
                onClick={() => onRemove(notification.id)}
                className="flex-shrink-0 text-gray-400 hover:text-gray-600 transition-colors"
                aria-label="通知を閉じる"
              >
                <X size={16} />
              </button>
            )}
          </div>
          
          {/* プログレスバー（自動削除の場合） */}
          {notification.autoClose !== false && (
            <div className="mt-3 h-1 bg-black bg-opacity-10 rounded-full overflow-hidden">
              <div
                className="h-full bg-current rounded-full animate-shrink"
                style={{
                  animationDuration: `${notification.duration || 5000}ms`,
                }}
              />
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export { NotificationSystem };
export type { Notification };