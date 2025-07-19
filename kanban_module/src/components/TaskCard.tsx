import React, { useState } from 'react';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { Task } from '../types';
import { 
  Calendar, 
  User, 
  Edit3, 
  Trash2, 
  Clock, 
  MessageCircle, 
  Paperclip,
  AlertTriangle,
  CheckCircle2,
  MoreHorizontal
} from 'lucide-react';

interface TaskCardProps {
  task: Task;
  onEdit: () => void;
  onDelete: () => void;
  isDragging?: boolean;
  isOffline?: boolean;
}

export const TaskCard: React.FC<TaskCardProps> = ({ 
  task, 
  onEdit, 
  onDelete, 
  isDragging = false,
  isOffline = false 
}) => {
  const [showMenu, setShowMenu] = useState(false);
  
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging: isSortableDragging,
  } = useSortable({
    id: task.id,
  });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  // 優先度のスタイルを取得
  const getPriorityStyle = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'priority-high';
      case 'medium':
        return 'priority-medium';
      case 'low':
        return 'priority-low';
      default:
        return 'priority-medium';
    }
  };

  const getPriorityText = (priority: string) => {
    switch (priority) {
      case 'high':
        return '高';
      case 'medium':
        return '中';
      case 'low':
        return '低';
      default:
        return priority;
    }
  };

  // 期限の表示テキストと状態を取得
  const getDueDateInfo = (dateString?: string) => {
    if (!dateString) return null;
    
    const date = new Date(dateString);
    const now = new Date();
    const diffDays = Math.ceil((date.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
    
    let text = '';
    let status = 'normal';
    
    if (diffDays < 0) {
      text = `${Math.abs(diffDays)}日前に期限切れ`;
      status = 'overdue';
    } else if (diffDays === 0) {
      text = '今日が期限';
      status = 'today';
    } else if (diffDays === 1) {
      text = '明日が期限';
      status = 'tomorrow';
    } else if (diffDays <= 3) {
      text = `${diffDays}日後`;
      status = 'soon';
    } else {
      text = `${diffDays}日後`;
      status = 'normal';
    }
    
    return { text, status, diffDays };
  };

  const dueDateInfo = getDueDateInfo(task.dueDate);

  // 進捗状況の計算
  const getProgressPercentage = () => {
    if (!task.estimatedHours || !task.actualHours) return 0;
    return Math.min((task.actualHours / task.estimatedHours) * 100, 100);
  };

  const progressPercentage = getProgressPercentage();

  // タスクの状態を判定
  const isOverdue = dueDateInfo && dueDateInfo.status === 'overdue';
  const isUrgent = dueDateInfo && ['today', 'tomorrow', 'soon'].includes(dueDateInfo.status);
  const hasAttachments = task.attachments && task.attachments.length > 0;
  const hasComments = task.comments && task.comments.length > 0;

  const handleMenuToggle = (e: React.MouseEvent) => {
    e.stopPropagation();
    setShowMenu(!showMenu);
  };

  const handleEdit = (e: React.MouseEvent) => {
    e.stopPropagation();
    onEdit();
    setShowMenu(false);
  };

  const handleDelete = (e: React.MouseEvent) => {
    e.stopPropagation();
    onDelete();
    setShowMenu(false);
  };

  const handleQuickComplete = (e: React.MouseEvent) => {
    e.stopPropagation();
    // TODO: クイック完了処理
    console.log('Quick complete task:', task.id);
    setShowMenu(false);
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className={`
        task-card group relative
        ${isDragging || isSortableDragging ? 'dragging' : ''}
        ${isOverdue ? 'border-l-4 border-l-red-500' : ''}
        ${isUrgent ? 'border-l-4 border-l-orange-500' : ''}
      `}
    >
      {/* カードヘッダー */}
      <div className="flex items-start justify-between mb-2">
        <h4 className="font-medium text-gray-900 text-sm leading-tight pr-2 flex-1">
          {task.title}
        </h4>
        
        {/* アクションメニュー */}
        <div className="relative opacity-0 group-hover:opacity-100 transition-opacity">
          <button
            onClick={handleMenuToggle}
            className="text-gray-400 hover:text-gray-600 p-1 rounded"
            title="アクション"
          >
            <MoreHorizontal size={14} />
          </button>
          
          {showMenu && (
            <div className="absolute right-0 top-6 bg-white border border-gray-200 rounded-lg shadow-medium z-20 min-w-[120px]">
              <button
                onClick={handleEdit}
                className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-2"
                disabled={isOffline}
              >
                <Edit3 size={12} />
                編集
              </button>
              <button
                onClick={handleQuickComplete}
                className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-2"
                disabled={isOffline}
              >
                <CheckCircle2 size={12} />
                完了
              </button>
              <hr className="my-1" />
              <button
                onClick={handleDelete}
                className="w-full text-left px-3 py-2 text-sm text-red-600 hover:bg-red-50 flex items-center gap-2"
                disabled={isOffline}
              >
                <Trash2 size={12} />
                削除
              </button>
            </div>
          )}
        </div>
      </div>

      {/* タスク説明 */}
      {task.description && (
        <p className="text-gray-600 text-xs mb-3 line-clamp-2">
          {task.description}
        </p>
      )}

      {/* 進捗バー */}
      {task.estimatedHours && task.actualHours !== undefined && (
        <div className="mb-3">
          <div className="flex justify-between items-center text-xs text-gray-500 mb-1">
            <span>進捗</span>
            <span>{task.actualHours}h / {task.estimatedHours}h</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-1.5">
            <div
              className={`h-1.5 rounded-full transition-all ${
                progressPercentage >= 100 
                  ? 'bg-green-500' 
                  : progressPercentage >= 80 
                  ? 'bg-blue-500' 
                  : 'bg-gray-400'
              }`}
              style={{ width: `${progressPercentage}%` }}
            />
          </div>
        </div>
      )}

      {/* タグ */}
      {task.tags && task.tags.length > 0 && (
        <div className="flex flex-wrap gap-1 mb-3">
          {task.tags.slice(0, 3).map((tag, index) => (
            <span
              key={index}
              className="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded-full"
            >
              {tag}
            </span>
          ))}
          {task.tags.length > 3 && (
            <span className="text-xs text-gray-500">
              +{task.tags.length - 3}
            </span>
          )}
        </div>
      )}

      {/* カードフッター */}
      <div className="space-y-2">
        {/* 優先度と期限 */}
        <div className="flex items-center justify-between">
          <span className={`priority-badge ${getPriorityStyle(task.priority)}`}>
            {getPriorityText(task.priority)}
          </span>
          
          {dueDateInfo && (
            <div className={`flex items-center gap-1 text-xs ${
              dueDateInfo.status === 'overdue' 
                ? 'text-red-600 font-medium' 
                : dueDateInfo.status === 'today' || dueDateInfo.status === 'tomorrow'
                ? 'text-orange-600 font-medium'
                : dueDateInfo.status === 'soon'
                ? 'text-yellow-600'
                : 'text-gray-500'
            }`}>
              {dueDateInfo.status === 'overdue' && <AlertTriangle size={12} />}
              <Clock size={12} />
              <span>{dueDateInfo.text}</span>
            </div>
          )}
        </div>

        {/* 担当者とアクション */}
        <div className="flex items-center justify-between">
          {task.assignee && (
            <div className="flex items-center gap-1 text-xs text-gray-500">
              <User size={12} />
              <span className="truncate max-w-20">{task.assignee}</span>
            </div>
          )}
          
          <div className="flex items-center gap-2">
            {hasAttachments && (
              <div className="flex items-center gap-1 text-xs text-gray-400">
                <Paperclip size={12} />
                <span>{task.attachments!.length}</span>
              </div>
            )}
            
            {hasComments && (
              <div className="flex items-center gap-1 text-xs text-gray-400">
                <MessageCircle size={12} />
                <span>{task.comments!.length}</span>
              </div>
            )}
          </div>
        </div>

        {/* 作成日 */}
        <div className="flex items-center gap-1 text-xs text-gray-400">
          <Calendar size={12} />
          <span>{new Date(task.createdAt).toLocaleDateString('ja-JP')}</span>
        </div>
      </div>

      {/* ステータス指示器 */}
      <div className="absolute top-2 right-2 flex gap-1">
        {isOverdue && (
          <div className="w-2 h-2 bg-red-500 rounded-full" title="期限切れ" />
        )}
        {isUrgent && !isOverdue && (
          <div className="w-2 h-2 bg-orange-500 rounded-full" title="緊急" />
        )}
        {task.priority === 'high' && (
          <div className="w-2 h-2 bg-red-400 rounded-full" title="高優先度" />
        )}
        {isOffline && (
          <div className="w-2 h-2 bg-yellow-500 rounded-full" title="オフライン" />
        )}
      </div>

      {/* ドラッグハンドル（モバイル用） */}
      <div className="absolute left-1 top-1/2 transform -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity md:hidden">
        <div className="w-1 h-6 bg-gray-300 rounded-full flex flex-col justify-center gap-0.5">
          <div className="w-0.5 h-0.5 bg-gray-500 rounded-full mx-auto" />
          <div className="w-0.5 h-0.5 bg-gray-500 rounded-full mx-auto" />
          <div className="w-0.5 h-0.5 bg-gray-500 rounded-full mx-auto" />
        </div>
      </div>
    </div>
  );
};