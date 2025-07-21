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
  horizontalListSortingStrategy,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import { Column } from './Column';
import { TaskCard } from './TaskCard';
import { TaskModal } from './TaskModal';
import { NotificationSystem } from './NotificationSystem';
import { Task, ColumnType, ProjectStats, TaskStatus } from '../types';
import { taskOperations, columnOperations, projectOperations } from '../firebase/config';
import { Plus, Settings, BarChart3, Filter, Search, Download, Grid3X3, List } from 'lucide-react';

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
  const [currentColumnId, setCurrentColumnId] = useState<string>('');
  const [viewMode, setViewMode] = useState<'board' | 'list'>('board');

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
    setCurrentColumnId(columnId);
    setEditingTask(null);
    setIsTaskModalOpen(true);
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setIsTaskModalOpen(true);
  };

  const handleSaveTask = async (taskData: Omit<Task, 'id' | 'createdAt' | 'updatedAt'>) => {
    try {
      const dataToSave = {
        ...taskData,
        columnId: currentColumnId || taskData.columnId,
      };

      if (editingTask) {
        await taskOperations.updateTask(editingTask.id, dataToSave);
        addNotification({
          type: 'success',
          title: 'タスクを更新しました',
          message: `「${dataToSave.title}」を更新しました`,
        });
      } else {
        const taskId = await taskOperations.addTask({
          ...dataToSave,
          projectId: projectId === 'default' ? undefined : projectId,
        });
        addNotification({
          type: 'success',
          title: 'タスクを作成しました',
          message: `「${dataToSave.title}」を作成しました`,
        });
      }
      
      setIsTaskModalOpen(false);
      setEditingTask(null);
      setCurrentColumnId('');
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
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-blue-600 border-t-transparent mx-auto mb-4"></div>
          <p className="text-gray-600 text-lg">カンバンボードを読み込み中...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center bg-white rounded-lg shadow-lg p-8 max-w-md">
          <div className="text-red-600 text-xl mb-4">⚠️ エラーが発生しました</div>
          <p className="text-gray-600 mb-6">{error}</p>
          <button
            onClick={loadKanbanData}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors"
          >
            再試行
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-full mx-auto">
        {/* ヘッダー */}
        <div className="bg-white border-b border-gray-200 shadow-sm">
          <div className="max-w-7xl mx-auto px-4 py-4">
            <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
              <div className="flex items-center gap-4">
                <div>
                  <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-3">
                    <span className="text-3xl">🚀</span>
                    BizFlow カンバンボード
                  </h1>
                  <p className="text-sm text-gray-600 mt-1">
                    プロジェクト: <span className="font-medium">{projectId === 'default' ? '全体' : projectId}</span>
                    {isOffline && <span className="text-yellow-600 ml-2 font-medium">(オフライン)</span>}
                  </p>
                </div>
              </div>

              {/* ツールバー */}
              <div className="flex items-center gap-2 flex-wrap">
                {/* ビューモード切り替え */}
                <div className="flex bg-gray-100 rounded-lg p-1">
                  <button
                    onClick={() => setViewMode('board')}
                    className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                      viewMode === 'board'
                        ? 'bg-white text-gray-900 shadow-sm'
                        : 'text-gray-600 hover:text-gray-900'
                    }`}
                  >
                    <Grid3X3 size={16} className="inline mr-1" />
                    ボード
                  </button>
                  <button
                    onClick={() => setViewMode('list')}
                    className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                      viewMode === 'list'
                        ? 'bg-white text-gray-900 shadow-sm'
                        : 'text-gray-600 hover:text-gray-900'
                    }`}
                  >
                    <List size={16} className="inline mr-1" />
                    リスト
                  </button>
                </div>

                <div className="h-6 border-l border-gray-300 mx-1"></div>

                <button
                  onClick={handleAddColumn}
                  className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium text-sm transition-colors shadow-sm"
                  disabled={isOffline}
                >
                  <Plus size={16} />
                  カラム追加
                </button>
                
                <button
                  onClick={handleExportData}
                  className="inline-flex items-center gap-2 bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg font-medium text-sm transition-colors"
                >
                  <Download size={16} />
                  エクスポート
                </button>
                
                <button className="inline-flex items-center gap-2 bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-lg font-medium text-sm transition-colors">
                  <BarChart3 size={16} />
                  分析
                </button>
                
                <button className="inline-flex items-center gap-2 bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-lg font-medium text-sm transition-colors">
                  <Settings size={16} />
                  設定
                </button>
              </div>
            </div>

            {/* 検索・フィルター */}
            <div className="flex flex-col sm:flex-row gap-4 mt-4">
              <div className="flex-1">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                  <input
                    type="text"
                    placeholder="タスクを検索..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>
              <div className="flex gap-2">
                <select
                  value={filterPriority}
                  onChange={(e) => setFilterPriority(e.target.value)}
                  className="px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white"
                >
                  <option value="all">全ての優先度</option>
                  <option value="high">高</option>
                  <option value="medium">中</option>
                  <option value="low">低</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        {/* 統計情報 */}
        {projectStats && (
          <div className="bg-white border-b border-gray-200">
            <div className="max-w-7xl mx-auto px-4 py-4">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg p-4 text-center border border-blue-200">
                  <div className="text-2xl font-bold text-blue-600 mb-1">
                    {projectStats.totalTasks}
                  </div>
                  <div className="text-sm text-blue-700 font-medium">総タスク数</div>
                </div>
                <div className="bg-gradient-to-r from-green-50 to-green-100 rounded-lg p-4 text-center border border-green-200">
                  <div className="text-2xl font-bold text-green-600 mb-1">
                    {projectStats.completionRate.toFixed(1)}%
                  </div>
                  <div className="text-sm text-green-700 font-medium">完了率</div>
                </div>
                <div className="bg-gradient-to-r from-orange-50 to-orange-100 rounded-lg p-4 text-center border border-orange-200">
                  <div className="text-2xl font-bold text-orange-600 mb-1">
                    {projectStats.inProgressTasks}
                  </div>
                  <div className="text-sm text-orange-700 font-medium">進行中</div>
                </div>
                <div className="bg-gradient-to-r from-purple-50 to-purple-100 rounded-lg p-4 text-center border border-purple-200">
                  <div className="text-2xl font-bold text-purple-600 mb-1">
                    {projectStats.todoTasks}
                  </div>
                  <div className="text-sm text-purple-700 font-medium">待機中</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* カンバンボード */}
        <div className="p-4">
          <DndContext
            sensors={sensors}
            collisionDetection={closestCorners}
            onDragStart={handleDragStart}
            onDragOver={handleDragOver}
            onDragEnd={handleDragEnd}
          >
            {/* 横並びレイアウト（重要！） */}
            <div style={{display: "flex", gap: "24px", overflowX: "auto", paddingBottom: "16px", minHeight: "calc(100vh - 300px)", width: "100%"}}>
              {columns
                .sort((a, b) => a.order - b.order)
                .map(column => {
                  const columnTasks = filteredTasks.filter(task => task.columnId === column.id);
                  
                  return (
                    <div key={column.id} style={{flexShrink: 0, width: "320px", minWidth: "320px"}}>
                      <SortableContext
                        items={columnTasks.map(task => task.id)}
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
                    </div>
                  );
                })}
            </div>

            {/* ドラッグオーバーレイ */}
            <DragOverlay>
              {activeTask ? (
                <div className="transform rotate-3 scale-105">
                  <TaskCard
                    task={activeTask}
                    onEdit={() => {}}
                    onDelete={() => {}}
                    isDragging
                  />
                </div>
              ) : null}
            </DragOverlay>
          </DndContext>
        </div>

        {/* タスク作成・編集モーダル */}
        <TaskModal
          isOpen={isTaskModalOpen}
          onClose={() => {
            setIsTaskModalOpen(false);
            setEditingTask(null);
            setCurrentColumnId('');
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