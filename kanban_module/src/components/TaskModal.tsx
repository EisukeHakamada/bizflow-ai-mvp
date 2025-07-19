import React, { useState, useEffect, useRef } from 'react';
import { Task, ColumnType } from '../types';
import { 
  X, 
  Calendar, 
  User, 
  Tag, 
  AlertCircle, 
  Clock,
  Plus,
  Paperclip,
  Trash2,
  Save,
  Loader2
} from 'lucide-react';

interface TaskModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (task: Omit<Task, 'id' | 'createdAt' | 'updatedAt'>) => Promise<void>;
  task?: Task | null;
  columns: ColumnType[];
}

export const TaskModal: React.FC<TaskModalProps> = ({
  isOpen,
  onClose,
  onSave,
  task,
  columns,
}) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    priority: 'medium' as 'low' | 'medium' | 'high',
    columnId: '',
    assignee: '',
    dueDate: '',
    tags: [] as string[],
    estimatedHours: '',
    projectId: '',
  });
  
  const [tagInput, setTagInput] = useState('');
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showAdvanced, setShowAdvanced] = useState(false);
  
  const titleInputRef = useRef<HTMLInputElement>(null);
  const modalRef = useRef<HTMLDivElement>(null);

  // フォームデータの初期化
  useEffect(() => {
    if (task) {
      setFormData({
        title: task.title,
        description: task.description,
        priority: task.priority,
        columnId: task.columnId,
        assignee: task.assignee || '',
        dueDate: task.dueDate || '',
        tags: task.tags || [],
        estimatedHours: task.estimatedHours?.toString() || '',
        projectId: task.projectId || '',
      });
    } else {
      setFormData({
        title: '',
        description: '',
        priority: 'medium',
        columnId: columns[0]?.id || '',
        assignee: '',
        dueDate: '',
        tags: [],
        estimatedHours: '',
        projectId: '',
      });
    }
    setTagInput('');
    setErrors({});
    setIsSubmitting(false);
    setShowAdvanced(false);
  }, [task, columns, isOpen]);

  // モーダルが開いたときにタイトル入力欄にフォーカス
  useEffect(() => {
    if (isOpen && titleInputRef.current) {
      setTimeout(() => titleInputRef.current?.focus(), 100);
    }
  }, [isOpen]);

  // ESCキーでモーダルを閉じる
  useEffect(() => {
    const handleEscKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && isOpen) {
        onClose();
      }
    };

    document.addEventListener('keydown', handleEscKey);
    return () => document.removeEventListener('keydown', handleEscKey);
  }, [isOpen, onClose]);

  // バリデーション
  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.title.trim()) {
      newErrors.title = 'タスク名は必須です';
    } else if (formData.title.length > 100) {
      newErrors.title = 'タスク名は100文字以内で入力してください';
    }

    if (!formData.columnId) {
      newErrors.columnId = 'カラムを選択してください';
    }

    if (formData.description.length > 1000) {
      newErrors.description = '説明は1000文字以内で入力してください';
    }

    if (formData.dueDate) {
      const dueDate = new Date(formData.dueDate);
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      
      if (dueDate < today) {
        newErrors.dueDate = '期限は今日以降の日付を選択してください';
      }
    }

    if (formData.estimatedHours) {
      const hours = parseFloat(formData.estimatedHours);
      if (isNaN(hours) || hours <= 0 || hours > 1000) {
        newErrors.estimatedHours = '見積時間は1〜1000時間の範囲で入力してください';
      }
    }

    if (formData.assignee.length > 50) {
      newErrors.assignee = '担当者名は50文字以内で入力してください';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // フォーム送信
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);

    try {
      const taskData = {
        ...formData,
        estimatedHours: formData.estimatedHours ? parseFloat(formData.estimatedHours) : undefined,
        projectId: formData.projectId || undefined,
      };

      await onSave(taskData);
    } catch (error) {
      console.error('タスクの保存に失敗しました:', error);
      setErrors({ submit: 'タスクの保存に失敗しました。もう一度お試しください。' });
    } finally {
      setIsSubmitting(false);
    }
  };

  // タグ関連の処理
  const handleAddTag = () => {
    const trimmedTag = tagInput.trim();
    if (trimmedTag && !formData.tags.includes(trimmedTag) && formData.tags.length < 10) {
      setFormData(prev => ({
        ...prev,
        tags: [...prev.tags, trimmedTag],
      }));
      setTagInput('');
    }
  };

  const handleRemoveTag = (tagToRemove: string) => {
    setFormData(prev => ({
      ...prev,
      tags: prev.tags.filter(tag => tag !== tagToRemove),
    }));
  };

  const handleTagKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddTag();
    }
  };

  // モーダル外クリックで閉じる
  const handleBackdropClick = (e: React.MouseEvent) => {
    if (modalRef.current && !modalRef.current.contains(e.target as Node)) {
      onClose();
    }
  };

  // 担当者の候補
  const assigneeSuggestions = [
    '田中太郎',
    '鈴木花子',
    '佐藤次郎',
    '山田美里',
    '伊藤健一',
  ];

  if (!isOpen) return null;

  return (
    <div 
      className="modal-backdrop" 
      onClick={handleBackdropClick}
    >
      <div 
        ref={modalRef}
        className="modal-content"
        onClick={(e) => e.stopPropagation()}
      >
        {/* ヘッダー */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900">
            {task ? 'タスクを編集' : '新しいタスクを作成'}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors focus-visible"
            disabled={isSubmitting}
          >
            <X size={24} />
          </button>
        </div>

        {/* フォーム */}
        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {/* 基本情報 */}
          <div className="space-y-4">
            <h3 className="text-lg font-medium text-gray-900">基本情報</h3>
            
            {/* タスク名 */}
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
                タスク名 *
              </label>
              <input
                ref={titleInputRef}
                type="text"
                id="title"
                value={formData.title}
                onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
                className={`form-input ${errors.title ? 'error' : ''}`}
                placeholder="例: ユーザー画面のデザイン作成"
                maxLength={100}
                disabled={isSubmitting}
              />
              {errors.title && (
                <p className="mt-1 text-sm text-red-600 flex items-center gap-1">
                  <AlertCircle size={16} />
                  {errors.title}
                </p>
              )}
            </div>

            {/* 説明 */}
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
                説明
              </label>
              <textarea
                id="description"
                value={formData.description}
                onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                rows={4}
                className={`form-input ${errors.description ? 'error' : ''}`}
                placeholder="タスクの詳細な説明を入力してください..."
                maxLength={1000}
                disabled={isSubmitting}
              />
              <div className="flex justify-between mt-1">
                {errors.description && (
                  <p className="text-sm text-red-600 flex items-center gap-1">
                    <AlertCircle size={16} />
                    {errors.description}
                  </p>
                )}
                <p className="text-xs text-gray-500 ml-auto">
                  {formData.description.length}/1000
                </p>
              </div>
            </div>

            {/* カラムと優先度 */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="columnId" className="block text-sm font-medium text-gray-700 mb-2">
                  カラム *
                </label>
                <select
                  id="columnId"
                  value={formData.columnId}
                  onChange={(e) => setFormData(prev => ({ ...prev, columnId: e.target.value }))}
                  className={`form-input ${errors.columnId ? 'error' : ''}`}
                  disabled={isSubmitting}
                >
                  <option value="">カラムを選択</option>
                  {columns.map(column => (
                    <option key={column.id} value={column.id}>
                      {column.title}
                    </option>
                  ))}
                </select>
                {errors.columnId && (
                  <p className="mt-1 text-sm text-red-600 flex items-center gap-1">
                    <AlertCircle size={16} />
                    {errors.columnId}
                  </p>
                )}
              </div>

              <div>
                <label htmlFor="priority" className="block text-sm font-medium text-gray-700 mb-2">
                  優先度
                </label>
                <select
                  id="priority"
                  value={formData.priority}
                  onChange={(e) => setFormData(prev => ({ 
                    ...prev, 
                    priority: e.target.value as 'low' | 'medium' | 'high' 
                  }))}
                  className="form-input"
                  disabled={isSubmitting}
                >
                  <option value="low">低</option>
                  <option value="medium">中</option>
                  <option value="high">高</option>
                </select>
              </div>
            </div>
          </div>

          {/* 担当者と期限 */}
          <div className="space-y-4">
            <h3 className="text-lg font-medium text-gray-900">担当・スケジュール</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="assignee" className="block text-sm font-medium text-gray-700 mb-2">
                  <User size={16} className="inline mr-1" />
                  担当者
                </label>
                <input
                  type="text"
                  id="assignee"
                  value={formData.assignee}
                  onChange={(e) => setFormData(prev => ({ ...prev, assignee: e.target.value }))}
                  className={`form-input ${errors.assignee ? 'error' : ''}`}
                  placeholder="例: 田中太郎"
                  maxLength={50}
                  list="assignee-suggestions"
                  disabled={isSubmitting}
                />
                <datalist id="assignee-suggestions">
                  {assigneeSuggestions.map(suggestion => (
                    <option key={suggestion} value={suggestion} />
                  ))}
                </datalist>
                {errors.assignee && (
                  <p className="mt-1 text-sm text-red-600 flex items-center gap-1">
                    <AlertCircle size={16} />
                    {errors.assignee}
                  </p>
                )}
              </div>

              <div>
                <label htmlFor="dueDate" className="block text-sm font-medium text-gray-700 mb-2">
                  <Calendar size={16} className="inline mr-1" />
                  期限
                </label>
                <input
                  type="date"
                  id="dueDate"
                  value={formData.dueDate}
                  onChange={(e) => setFormData(prev => ({ ...prev, dueDate: e.target.value }))}
                  className={`form-input ${errors.dueDate ? 'error' : ''}`}
                  min={new Date().toISOString().split('T')[0]}
                  disabled={isSubmitting}
                />
                {errors.dueDate && (
                  <p className="mt-1 text-sm text-red-600 flex items-center gap-1">
                    <AlertCircle size={16} />
                    {errors.dueDate}
                  </p>
                )}
              </div>
            </div>
          </div>

          {/* タグ */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <Tag size={16} className="inline mr-1" />
              タグ ({formData.tags.length}/10)
            </label>
            <div className="flex gap-2 mb-2">
              <input
                type="text"
                value={tagInput}
                onChange={(e) => setTagInput(e.target.value)}
                onKeyPress={handleTagKeyPress}
                className="flex-1 form-input"
                placeholder="タグを入力してEnterキーを押す"
                maxLength={20}
                disabled={isSubmitting || formData.tags.length >= 10}
              />
              <button
                type="button"
                onClick={handleAddTag}
                className="btn btn-secondary"
                disabled={isSubmitting || !tagInput.trim() || formData.tags.length >= 10}
              >
                <Plus size={16} />
              </button>
            </div>
            {formData.tags.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {formData.tags.map((tag, index) => (
                  <span
                    key={index}
                    className="bg-blue-100 text-blue-700 text-sm px-3 py-1 rounded-full flex items-center gap-1"
                  >
                    {tag}
                    <button
                      type="button"
                      onClick={() => handleRemoveTag(tag)}
                      className="text-blue-500 hover:text-blue-700"
                      disabled={isSubmitting}
                    >
                      <X size={14} />
                    </button>
                  </span>
                ))}
              </div>
            )}
          </div>

          {/* 高度な設定 */}
          <div>
            <button
              type="button"
              onClick={() => setShowAdvanced(!showAdvanced)}
              className="text-sm text-blue-600 hover:text-blue-700 font-medium"
            >
              {showAdvanced ? '▼' : '▶'} 高度な設定
            </button>
            
            {showAdvanced && (
              <div className="mt-4 space-y-4 pl-4 border-l-2 border-gray-200">
                <div>
                  <label htmlFor="estimatedHours" className="block text-sm font-medium text-gray-700 mb-2">
                    <Clock size={16} className="inline mr-1" />
                    見積時間（時間）
                  </label>
                  <input
                    type="number"
                    id="estimatedHours"
                    value={formData.estimatedHours}
                    onChange={(e) => setFormData(prev => ({ ...prev, estimatedHours: e.target.value }))}
                    className={`form-input ${errors.estimatedHours ? 'error' : ''}`}
                    placeholder="例: 8"
                    min="0.5"
                    max="1000"
                    step="0.5"
                    disabled={isSubmitting}
                  />
                  {errors.estimatedHours && (
                    <p className="mt-1 text-sm text-red-600 flex items-center gap-1">
                      <AlertCircle size={16} />
                      {errors.estimatedHours}
                    </p>
                  )}
                </div>

                <div>
                  <label htmlFor="projectId" className="block text-sm font-medium text-gray-700 mb-2">
                    プロジェクトID
                  </label>
                  <input
                    type="text"
                    id="projectId"
                    value={formData.projectId}
                    onChange={(e) => setFormData(prev => ({ ...prev, projectId: e.target.value }))}
                    className="form-input"
                    placeholder="例: project-001"
                    disabled={isSubmitting}
                  />
                </div>
              </div>
            )}
          </div>

          {/* エラーメッセージ */}
          {errors.submit && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-red-800 flex items-center gap-2">
                <AlertCircle size={16} />
                {errors.submit}
              </p>
            </div>
          )}

          {/* ボタン */}
          <div className="flex justify-end gap-3 pt-4 border-t border-gray-200">
            <button
              type="button"
              onClick={onClose}
              className="btn btn-secondary"
              disabled={isSubmitting}
            >
              キャンセル
            </button>
            <button
              type="submit"
              className="btn btn-primary flex items-center gap-2"
              disabled={isSubmitting}
            >
              {isSubmitting ? (
                <>
                  <Loader2 size={16} className="animate-spin" />
                  保存中...
                </>
              ) : (
                <>
                  <Save size={16} />
                  {task ? '更新' : '作成'}
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};