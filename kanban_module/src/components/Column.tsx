import React, { useState } from 'react';
import { useDroppable } from '@dnd-kit/core';
import { TaskCard } from './TaskCard';
import { Task, ColumnType } from '../types';
import { Plus, MoreHorizontal, Edit3, Trash2, Settings } from 'lucide-react';

interface ColumnProps {
  column: ColumnType;
  tasks: Task[];
  onAddTask: () => void;
  onEditTask: (task: Task) => void;
  onDeleteTask: (taskId: string) => void;
  isOffline?: boolean;
}

export const Column: React.FC<ColumnProps> = ({
  column,
  tasks,
  onAddTask,
  onEditTask,
  onDeleteTask,
  isOffline = false,
}) => {
  const [showMenu, setShowMenu] = useState(false);
  const [isCollapsed, setIsCollapsed] = useState(column.isCollapsed || false);
  
  const { isOver, setNodeRef } = useDroppable({
    id: column.id,
  });

  const handleColumnEdit = () => {
    const newTitle = window.prompt('カラム名を編集:', column.title);
    if (newTitle && newTitle.trim()) {
      console.log('Update column:', { id: column.id, title: newTitle.trim() });
    }
    setShowMenu(false);
  };

  const handleColumnDelete = () => {
    if (tasks.length > 0) {
      alert('タスクが含まれているカラムは削除できません');
      return;
    }
    
    if (window.confirm(`「${column.title}」カラムを削除しますか？`)) {
      console.log('Delete column:', column.id);
    }
    setShowMenu(false);
  };

  const handleColumnSettings = () => {
    console.log('Open column settings:', column.id);
    setShowMenu(false);
  };

  const handleToggleCollapse = () => {
    setIsCollapsed(!isCollapsed);
  };

  const isWipLimitExceeded = column.limit && tasks.length >= column.limit;
  const wipLimitWarning = column.limit && tasks.length >= column.limit * 0.8;

  return (
    <div style={{width: "320px", minWidth: "320px", height: "100%", background: "white", borderRadius: "12px", boxShadow: "0 2px 8px rgba(0,0,0,0.1)", border: "1px solid #e5e7eb", display: "flex", flexDirection: "column"}}>
      {/* カラムヘッダー */}
      <div 
        className="kanban-column-header px-4 py-3 border-b border-gray-200 bg-gray-50 rounded-t-lg"
        style={{
          borderTop: `4px solid ${column.color}`,
        }}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 flex-1 min-w-0">
            <button
              onClick={handleToggleCollapse}
              className="text-gray-400 hover:text-gray-600 flex-shrink-0 p-1 rounded hover:bg-gray-200 transition-colors"
            >
              <span className={`transform transition-transform text-xs ${isCollapsed ? '' : 'rotate-90'}`}>
                ▶
              </span>
            </button>
            
            <h3 className="kanban-column-title font-semibold text-gray-800 truncate text-sm">
              {column.title}
            </h3>
            
            <div className="flex items-center gap-1">
              <span 
                className={`kanban-column-count text-xs px-2 py-1 rounded-full font-medium ${
                  wipLimitWarning 
                    ? 'bg-yellow-100 text-yellow-800 border border-yellow-200' 
                    : 'bg-gray-100 text-gray-600 border border-gray-200'
                }`}
              >
                {tasks.length}
                {column.limit && ` / ${column.limit}`}
              </span>
              
              {isWipLimitExceeded && (
                <span className="w-2 h-2 bg-red-500 rounded-full animate-pulse" title="WIP制限を超過" />
              )}
            </div>
          </div>

          <div className="flex items-center gap-1">
            <button
              onClick={onAddTask}
              className="text-gray-400 hover:text-gray-600 hover:bg-gray-200 p-1.5 rounded transition-colors"
              title="新しいタスクを追加"
              disabled={isOffline}
            >
              <Plus size={16} />
            </button>
            
            <div className="relative">
              <button
                onClick={() => setShowMenu(!showMenu)}
                className="text-gray-400 hover:text-gray-600 hover:bg-gray-200 p-1.5 rounded transition-colors"
                title="カラムメニュー"
              >
                <MoreHorizontal size={16} />
              </button>
              
              {showMenu && (
                <div className="absolute right-0 top-8 bg-white border border-gray-200 rounded-lg shadow-lg z-20 min-w-[140px] py-1">
                  <button
                    onClick={handleColumnEdit}
                    className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-2 transition-colors"
                    disabled={isOffline}
                  >
                    <Edit3 size={14} />
                    編集
                  </button>
                  <button
                    onClick={handleColumnSettings}
                    className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-2 transition-colors"
                    disabled={isOffline}
                  >
                    <Settings size={14} />
                    設定
                  </button>
                  <hr className="my-1 border-gray-100" />
                  <button
                    onClick={handleColumnDelete}
                    className="w-full text-left px-3 py-2 text-sm text-red-600 hover:bg-red-50 flex items-center gap-2 transition-colors"
                    disabled={isOffline}
                  >
                    <Trash2 size={14} />
                    削除
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* WIP制限警告 */}
        {isWipLimitExceeded && (
          <div className="mt-2 text-xs text-red-600 bg-red-50 px-2 py-1 rounded border border-red-200">
            ⚠️ WIP制限を超過しています
          </div>
        )}

        {/* プログレスバー */}
        {column.limit && (
          <div className="mt-2">
            <div className="w-full bg-gray-200 rounded-full h-1.5">
              <div
                className={`h-1.5 rounded-full transition-all duration-300 ${
                  isWipLimitExceeded
                    ? 'bg-red-500'
                    : wipLimitWarning
                    ? 'bg-yellow-500'
                    : 'bg-blue-500'
                }`}
                style={{
                  width: `${Math.min((tasks.length / column.limit) * 100, 100)}%`,
                }}
              />
            </div>
          </div>
        )}
      </div>

      {/* カラムコンテンツ */}
      {!isCollapsed && (
        <div
          ref={setNodeRef}
          className={`kanban-column-tasks flex-1 p-3 overflow-y-auto min-h-0 ${
            isOver ? 'bg-blue-50 border-blue-200' : ''
          } ${isWipLimitExceeded ? 'border-red-200' : ''}`}
        >
          <div className="space-y-3 min-h-full">
            {tasks.map(task => (
              <TaskCard
                key={task.id}
                task={task}
                onEdit={() => onEditTask(task)}
                onDelete={() => onDeleteTask(task.id)}
                isOffline={isOffline}
              />
            ))}
            
            {/* 空の状態 */}
            {tasks.length === 0 && (
              <div className="text-center py-12 text-gray-400">
                <div className="mb-4">
                  <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-3 border-2 border-dashed border-gray-300">
                    <Plus size={24} className="text-gray-400" />
                  </div>
                  <p className="text-sm font-medium text-gray-500 mb-1">タスクがありません</p>
                  <p className="text-xs text-gray-400">ここにタスクをドロップするか、</p>
                  <p className="text-xs text-gray-400">下のボタンで新規作成できます</p>
                </div>
                <button
                  onClick={onAddTask}
                  className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 text-sm font-medium px-4 py-2 rounded-lg border border-blue-200 hover:bg-blue-50 transition-colors"
                  disabled={isOffline}
                >
                  <Plus size={16} />
                  最初のタスクを追加
                </button>
              </div>
            )}

            {/* ドロップゾーン（タスクがある場合） */}
            {tasks.length > 0 && (
              <div className="h-16 opacity-0 hover:opacity-100 transition-opacity">
                <button
                  onClick={onAddTask}
                  className="w-full h-full border-2 border-dashed border-gray-300 rounded-lg flex items-center justify-center text-gray-400 hover:border-blue-400 hover:text-blue-600 transition-colors"
                  disabled={isOffline}
                >
                  <Plus size={20} />
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {/* 折りたたみ時の表示 */}
      {isCollapsed && (
        <div className="p-4 bg-gray-50 border-t border-gray-200 rounded-b-lg">
          <div className="flex justify-between items-center text-sm text-gray-600">
            <span className="font-medium">{tasks.length} タスク</span>
            <div className="flex gap-1">
              {tasks.filter(t => t.priority === 'high').length > 0 && (
                <span className="w-2 h-2 bg-red-500 rounded-full animate-pulse" title="高優先度タスクあり" />
              )}
              {tasks.filter(t => t.dueDate && new Date(t.dueDate) < new Date()).length > 0 && (
                <span className="w-2 h-2 bg-orange-500 rounded-full animate-pulse" title="期限切れタスクあり" />
              )}
            </div>
          </div>
        </div>
      )}

      {/* ドラッグオーバーレイ */}
      {isOver && (
        <div className="absolute inset-0 bg-blue-100 bg-opacity-50 border-2 border-blue-400 border-dashed rounded-lg pointer-events-none z-10">
          <div className="flex items-center justify-center h-full">
            <div className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium shadow-lg">
              <Plus size={16} className="inline mr-2" />
              ここにドロップ
            </div>
          </div>
        </div>
      )}

      {/* オフライン表示 */}
      {isOffline && (
        <div className="absolute top-2 right-2 w-3 h-3 bg-yellow-500 rounded-full border-2 border-white shadow-sm" title="オフライン" />
      )}
    </div>
  );
};