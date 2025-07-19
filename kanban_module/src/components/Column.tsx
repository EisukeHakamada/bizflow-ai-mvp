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
    <div className="column relative">
      <div 
        className="column-header"
        style={{
          borderTopColor: column.color,
          borderTopWidth: '4px',
        }}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 flex-1 min-w-0">
            <button
              onClick={handleToggleCollapse}
              className="text-gray-400 hover:text-gray-600 flex-shrink-0"
            >
              <span className={`transform transition-transform ${isCollapsed ? '' : 'rotate-90'}`}>
                ▶
              </span>
            </button>
            
            <h3 className="font-semibold text-gray-800 truncate">
              {column.title}
            </h3>
            
            <div className="flex items-center gap-1">
              <span 
                className={`text-sm px-2 py-1 rounded-full ${
                  wipLimitWarning 
                    ? 'bg-yellow-100 text-yellow-800' 
                    : 'bg-gray-100 text-gray-600'
                }`}
              >
                {tasks.length}
                {column.limit && ` / ${column.limit}`}
              </span>
              
              {isWipLimitExceeded && (
                <span className="w-2 h-2 bg-red-500 rounded-full" title="WIP制限を超過" />
              )}
            </div>
          </div>

          <div className="flex items-center gap-1">
            <button
              onClick={onAddTask}
              className="text-gray-400 hover:text-gray-600 hover:bg-gray-100 p-1 rounded"
              title="新しいタスクを追加"
              disabled={isOffline}
            >
              <Plus size={16} />
            </button>
            
            <div className="relative">
              <button
                onClick={() => setShowMenu(!showMenu)}
                className="text-gray-400 hover:text-gray-600 hover:bg-gray-100 p-1 rounded"
                title="カラムメニュー"
              >
                <MoreHorizontal size={16} />
              </button>
              
              {showMenu && (
                <div className="absolute right-0 top-8 bg-white border border-gray-200 rounded-lg shadow-medium z-10 min-w-[120px]">
                  <button
                    onClick={handleColumnEdit}
                    className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-2"
                    disabled={isOffline}
                  >
                    <Edit3 size={14} />
                    編集
                  </button>
                  <button
                    onClick={handleColumnSettings}
                    className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-2"
                    disabled={isOffline}
                  >
                    <Settings size={14} />
                    設定
                  </button>
                  <hr className="my-1" />
                  <button
                    onClick={handleColumnDelete}
                    className="w-full text-left px-3 py-2 text-sm text-red-600 hover:bg-red-50 flex items-center gap-2"
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

        {isWipLimitExceeded && (
          <div className="mt-2 text-xs text-red-600 bg-red-50 px-2 py-1 rounded">
            ⚠️ WIP制限を超過しています
          </div>
        )}

        {column.limit && (
          <div className="mt-2">
            <div className="w-full bg-gray-200 rounded-full h-1">
              <div
                className={`h-1 rounded-full transition-all ${
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

      {!isCollapsed && (
        <div
          ref={setNodeRef}
          className={`column-content custom-scrollbar ${
            isOver ? 'drag-over' : ''
          } ${isWipLimitExceeded ? 'border-red-200' : ''}`}
        >
          <div className="space-y-3">
            {tasks.map(task => (
              <TaskCard
                key={task.id}
                task={task}
                onEdit={() => onEditTask(task)}
                onDelete={() => onDeleteTask(task.id)}
                isOffline={isOffline}
              />
            ))}
            
            {tasks.length === 0 && (
              <div className="text-center py-8 text-gray-400">
                <div className="mb-4">
                  <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-2">
                    <Plus size={24} className="text-gray-400" />
                  </div>
                  <p className="text-sm">タスクがありません</p>
                </div>
                <button
                  onClick={onAddTask}
                  className="text-blue-500 hover:text-blue-600 text-sm font-medium"
                  disabled={isOffline}
                >
                  最初のタスクを追加
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {isCollapsed && (
        <div className="p-4 bg-gray-50 border-t border-gray-200">
          <div className="flex justify-between items-center text-sm text-gray-600">
            <span>{tasks.length} タスク</span>
            <div className="flex gap-1">
              {tasks.filter(t => t.priority === 'high').length > 0 && (
                <span className="w-2 h-2 bg-red-500 rounded-full" title="高優先度タスクあり" />
              )}
              {tasks.filter(t => t.dueDate && new Date(t.dueDate) < new Date()).length > 0 && (
                <span className="w-2 h-2 bg-orange-500 rounded-full" title="期限切れタスクあり" />
              )}
            </div>
          </div>
        </div>
      )}

      {isOver && (
        <div className="absolute inset-0 bg-blue-100 bg-opacity-50 border-2 border-blue-300 border-dashed rounded-lg pointer-events-none">
          <div className="flex items-center justify-center h-full">
            <div className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium">
              ここにドロップ
            </div>
          </div>
        </div>
      )}

      {isOffline && (
        <div className="absolute top-2 right-2 w-2 h-2 bg-yellow-500 rounded-full" title="オフライン" />
      )}
    </div>
  );
};