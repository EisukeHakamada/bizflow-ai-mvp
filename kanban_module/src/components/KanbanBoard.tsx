import React, { useState, useEffect } from 'react';
import {
  DndContext,
  DragEndEvent,
  DragOverEvent,
  DragStartEvent,
  PointerSensor,
  useSensor,
  useSensors,
  closestCorners,
  DragOverlay,
} from '@dnd-kit/core';
import {
  SortableContext,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import { Column } from './Column';
import { TaskCard } from './TaskCard';
import { TaskModal } from './TaskModal';
import { NotificationSystem } from './NotificationSystem';
import { Task, ColumnType, ProjectStats } from '../types';
import { taskOperations, columnOperations, projectOperations } from '../firebase/config';
import { Plus, Settings, BarChart3, Filter, Search, Download } from 'lucide-react';

interface KanbanBoardProps {
  projectId?: string;
  isMobileView?: boolean;
  isOffline?: boolean;
}

const KanbanBoard: React.FC<KanbanBoardProps> = ({
  projectId = 'default',
  isMobileView = false,
  isOffline = false,
}) => {
  // State管理
  const [columns, setColumns] = useState<ColumnType[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [activeTask, setActiveTask] = useState<Task | null>(null);
  const [isTaskModalOpen, setIsTaskModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [projectStats, setProjectStats] = useState<ProjectStats | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterPriority, setFilterPriority] = useState<string>('all');
  const [notifications, setNotifications] = useState<any[]>([]);

  // ドラッグ&ドロップセンサー
  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    })
  );

  // 初期データ読み込み
  useEffect(() => {
    loadKanbanData();
  }, [projectId]);

  // リアルタイムリスナー設定
  useEffect(() => {
    if (isOffline) return;

    const unsubscribeTasks = taskOperations.onTasksChange((updatedTasks) => {
      setTasks(updatedTasks);
      updateProjectStats(updatedTasks);
    });

    const unsubscribeColumns = columnOperations.onColumnsChange((updatedColumns) => {
      setColumns(updatedColumns);
    });

    return () => {
      unsubscribeTasks();
      unsubscribeColumns();
    };
  }, [isOffline]);

  const loadKanbanData = async () => {
    try {
      setIsLoading(true);
      setError(null);

      const [loadedTasks, loadedColumns] = await Promise.all([
        projectId === 'default' 
          ? taskOperations.getAllTasks()
          : taskOperations.getTasksByProject(projectId),
        columnOperations.getAllColumns(),
      ]);

      setTasks(loadedTasks);
      setColumns(loadedColumns);
      
      // プロジェクト統計を更新
      await updateProjectStats(loadedTasks);

    } catch (err) {
      console.error('データの読み込みに失敗しました:', err);
      setError('データの読み込みに失敗しました');
    } finally {
      setIsLoading(false);
    }
  };

  const updateProjectStats = async (currentTasks: Task[]) => {
    try {
      const stats = await projectOperations.getProjectStats(
        projectId === 'default' ? undefined : projectId
      );
      setProjectStats(stats);
    } catch (err) {
      console.error('統計の更新に失敗しました:', err);
    }
  };

  const addNotification = (notification: {
    type: 'success' | 'error' | 'warning' | 'info';
    title: string;
    message: string;
  }) => {
    const newNotification = {
      id: Date.now().toString(),
      ...notification,
      timestamp: new Date(),
    };
    setNotifications(prev => [...prev, newNotification]);

    // 5秒後に自動削除
    setTimeout(() => {
      setNotifications(prev => prev.filter(n => n.id !== newNotification.id));
    }, 5000);
  };

  // ドラッグ&ドロップイベント
  const handleDragStart = (event: DragStartEvent) => {
    const { active } = event;
    const task = tasks.find(t => t.id === active.id);
    setActiveTask(task || null);
  };

  const handleDragOver = (event: DragOverEvent) => {
    const { active, over } = event;
    if (!over) return;

    const activeId = active.id as string;
    const overId = over.id as string;

    const activeTask = tasks.find(t => t.id === activeId);
    if (!activeTask) return;

    const overColumn = columns.find(c => c.id === overId);
    if (overColumn && activeTask.columnId !== overId) {
      setTasks(prev =>
        prev.map(task =>
          task.id === activeId
            ? { ...task, columnId: overId, updatedAt: new Date() }
            : task
        )
      );
    }
  };

  const handleDragEnd = async (event: DragEndEvent) => {
    const { active, over } = event;
    setActiveTask(null);

    if (!over) return;

    const activeId = active.id as string;
    const overId = over.id as string;

    const activeTask = tasks.find(t => t.id === activeId);
    if (!activeTask) return;

    const overColumn = columns.find(c => c.id === overId);
    if (overColumn && activeTask.columnId !== overId) {
      try {
        await taskOperations.moveTask(activeId, overId);
        addNotification({
          type: 'success',
          title: 'タスクを移動しました',
          message: `「${activeTask.title}」を「${overColumn.title}」に移動しました`,
        });
      } catch (err) {
        console.error('タスクの移動に失敗しました:', err);
        addNotification({
          type: 'error',
          title: 'エラー',
          message: 'タスクの移動に失敗しました',
        });
        // エラー時は元の状態に戻す
        loadKanbanData();
      }
    }
  };

  // タスク操作
  const handleAddTask = (columnId: string) => {
    setEditingTask(null);
    setIsTaskModalOpen(true);
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setIsTaskModalOpen(true);
  };

  const handleSaveTask = async (taskData: Omit<Task, 'id' | 'createdAt' | 'updatedAt'>) => {
    try {
      if (editingTask) {
        await taskOperations.updateTask(editingTask.id, taskData);
        addNotification({
          type: 'success',
          title: 'タスクを更新しました',
          message: `「${taskData.title}」を更新しました`,
        });
      } else {
        const taskId = await taskOperations.addTask({
          ...taskData,
          projectId: projectId === 'default' ? undefined : projectId,
        });
        addNotification({
          type: 'success',
          title: 'タスクを作成しました',
          message: `「${taskData.title}」を作成しました`,
        });
      }
      
      setIsTaskModalOpen(false);
      setEditingTask(null);
    } catch (err) {
      console.error('タスクの保存に失敗しました:', err);
      addNotification({
        type: 'error',
        title: 'エラー',
        message: 'タスクの保存に失敗しました',
      });
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    const task = tasks.find(t => t.id === taskId);
    if (!task) return;

    if (window.confirm(`「${task.title}」を削除しますか？`)) {
      try {
        await taskOperations.deleteTask(taskId);
        addNotification({
          type: 'success',
          title: 'タスクを削除しました',
          message: `「${task.title}」を削除しました`,
        });
      } catch (err) {
        console.error('タスクの削除に失敗しました:', err);
        addNotification({
          type: 'error',
          title: 'エラー',
          message: 'タスクの削除に失敗しました',
        });
      }
    }
  };

  const handleAddColumn = async () => {
    const title = window.prompt('新しいカラム名を入力してください:');
    if (title) {
      try {
        await columnOperations.addColumn({
          title,
          color: '#6b7280',
          order: columns.length,
          taskIds: [],
        });
        addNotification({
          type: 'success',
          title: 'カラムを追加しました',
          message: `「${title}」カラムを追加しました`,
        });
      } catch (err) {
        console.error('カラムの追加に失敗しました:', err);
        addNotification({
          type: 'error',
          title: 'エラー',
          message: 'カラムの追加に失敗しました',
        });
      }
    }
  };

  // フィルタリング
  const filteredTasks = tasks.filter(task => {
    const matchesSearch = task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         task.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesPriority = filterPriority === 'all' || task.priority === filterPriority;
    return matchesSearch && matchesPriority;
  });

  // データエクスポート
  const handleExportData = () => {
    const exportData = {
      tasks: filteredTasks,
      columns,
      stats: projectStats,
      exportDate: new Date().toISOString(),
    };
    
    const blob = new Blob([JSON.stringify(exportData, null, 2)], {
      type: 'application/json',
    });
    
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `kanban-export-${projectId}-${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    addNotification({
      type: 'success',
      title: 'データをエクスポートしました',
      message: 'ファイルのダウンロードを開始しました',
    });
  };

  if (isLoading) {
    return (
      <div className="kanban-container p-6">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">カンバンボードを読み込み中...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="kanban-container p-6">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error}</p>
          <button
            onClick={loadKanbanData}
            className="btn btn-primary"
          >
            再試行
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={`kanban-container ${isMobileView ? 'mobile-view' : ''}`}>
      <div className="max-w-7xl mx-auto p-4">
        {/* ヘッダー */}
        <div className="mb-6">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-800 mb-2">
                🚀 BizFlow カンバンボード
              </h1>
              <p className="text-gray-600">
                プロジェクト: {projectId === 'default' ? '全体' : projectId}
                {isOffline && <span className="text-yellow-600 ml-2">(オフライン)</span>}
              </p>
            </div>

            {/* ツールバー */}
            <div className="flex flex-wrap gap-2">
              <button
                onClick={handleAddColumn}
                className="btn btn-primary"
                disabled={isOffline}
              >
                <Plus size={20} />
                <span className="hidden sm:inline ml-2">カラム追加</span>
              </button>
              <button
                onClick={handleExportData}
                className="btn btn-secondary"
              >
                <Download size={20} />
                <span className="hidden sm:inline ml-2">エクスポート</span>
              </button>
              <button className="btn btn-secondary">
                <BarChart3 size={20} />
                <span className="hidden sm:inline ml-2">分析</span>
              </button>
              <button className="btn btn-secondary">
                <Settings size={20} />
                <span className="hidden sm:inline ml-2">設定</span>
              </button>
            </div>
          </div>

          {/* フィルターと検索 */}
          <div className="flex flex-col sm:flex-row gap-4 mb-6">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                <input
                  type="text"
                  placeholder="タスクを検索..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="form-input pl-10"
                />
              </div>
            </div>
            <div className="flex gap-2">
              <select
                value={filterPriority}
                onChange={(e) => setFilterPriority(e.target.value)}
                className="form-input"
              >
                <option value="all">全ての優先度</option>
                <option value="high">高</option>
                <option value="medium">中</option>
                <option value="low">低</option>
              </select>
            </div>
          </div>

          {/* 統計情報 */}
          {projectStats && (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div className="card p-4 text-center">
                <div className="text-2xl font-bold text-blue-600 mb-1">
                  {projectStats.totalTasks}
                </div>
                <div className="text-sm text-gray-600">総タスク数</div>
              </div>
              <div className="card p-4 text-center">
                <div className="text-2xl font-bold text-green-600 mb-1">
                  {projectStats.completionRate.toFixed(1)}%
                </div>
                <div className="text-sm text-gray-600">完了率</div>
              </div>
              <div className="card p-4 text-center">
                <div className="text-2xl font-bold text-orange-600 mb-1">
                  {projectStats.inProgressTasks}
                </div>
                <div className="text-sm text-gray-600">進行中</div>
              </div>
              <div className="card p-4 text-center">
                <div className="text-2xl font-bold text-purple-600 mb-1">
                  {projectStats.todoTasks}
                </div>
                <div className="text-sm text-gray-600">待機中</div>
              </div>
            </div>
          )}
        </div>

        {/* カンバンボード */}
        <DndContext
          sensors={sensors}
          collisionDetection={closestCorners}
          onDragStart={handleDragStart}
          onDragOver={handleDragOver}
          onDragEnd={handleDragEnd}
        >
          <div className={`grid gap-6 ${
            isMobileView 
              ? 'grid-cols-1' 
              : 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4'
          }`}>
            {columns
              .sort((a, b) => a.order - b.order)
              .map(column => {
                const columnTasks = filteredTasks.filter(task => task.columnId === column.id);
                
                return (
                  <SortableContext
                    key={column.id}
                    items={column.taskIds}
                    strategy={verticalListSortingStrategy}
                  >
                    <Column
                      column={column}
                      tasks={columnTasks}
                      onAddTask={() => handleAddTask(column.id)}
                      onEditTask={handleEditTask}
                      onDeleteTask={handleDeleteTask}
                      isOffline={isOffline}
                    />
                  </SortableContext>
                );
              })}
          </div>

          {/* ドラッグオーバーレイ */}
          <DragOverlay>
            {activeTask ? (
              <TaskCard
                task={activeTask}
                onEdit={() => {}}
                onDelete={() => {}}
                isDragging
              />
            ) : null}
          </DragOverlay>
        </DndContext>

        {/* タスク作成・編集モーダル */}
        <TaskModal
          isOpen={isTaskModalOpen}
          onClose={() => {
            setIsTaskModalOpen(false);
            setEditingTask(null);
          }}
          onSave={handleSaveTask}
          task={editingTask}
          columns={columns}
        />

        {/* 通知システム */}
        <NotificationSystem notifications={notifications} />
      </div>
    </div>
  );
};

export default KanbanBoard;