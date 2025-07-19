// 型定義ファイル

export interface Task {
    id: string;
    title: string;
    description: string;
    priority: 'low' | 'medium' | 'high';
    columnId: string;
    assignee?: string;
    dueDate?: string;
    tags?: string[];
    createdAt: Date;
    updatedAt: Date;
    projectId?: string;
    estimatedHours?: number;
    actualHours?: number;
    attachments?: Attachment[];
    comments?: Comment[];
  }
  
  export interface ColumnType {
    id: string;
    title: string;
    color: string;
    order: number;
    taskIds: string[];
    limit?: number; // WIP制限
    isCollapsed?: boolean;
  }
  
  export interface Attachment {
    id: string;
    name: string;
    url: string;
    type: string;
    size: number;
    uploadedAt: Date;
    uploadedBy: string;
  }
  
  export interface Comment {
    id: string;
    content: string;
    author: string;
    createdAt: Date;
    updatedAt?: Date;
    mentions?: string[];
  }
  
  export interface Project {
    id: string;
    name: string;
    description: string;
    color: string;
    owner: string;
    members: string[];
    createdAt: Date;
    updatedAt: Date;
    deadline?: string;
    status: 'active' | 'completed' | 'archived';
  }
  
  export interface User {
    id: string;
    name: string;
    email: string;
    avatar?: string;
    role: 'admin' | 'member' | 'viewer';
    joinedAt: Date;
    lastActivity?: Date;
  }
  
  export interface KanbanSettings {
    theme: 'light' | 'dark' | 'auto';
    language: 'ja' | 'en';
    timezone: string;
    autoRefresh: boolean;
    notifications: boolean;
    compactView: boolean;
    enableDragDrop: boolean;
    enableBulkOperations: boolean;
    enableAdvancedFilters: boolean;
    enableTimeTracking: boolean;
    enableComments: boolean;
    enableFileAttachments: boolean;
    googleCalendarIntegration: boolean;
    slackIntegration: boolean;
    emailNotifications: boolean;
  }
  
  export interface Filter {
    assignee?: string[];
    priority?: ('low' | 'medium' | 'high')[];
    tags?: string[];
    dueDate?: {
      from?: string;
      to?: string;
    };
    createdDate?: {
      from?: string;
      to?: string;
    };
    search?: string;
  }
  
  export interface ProjectStats {
    totalTasks: number;
    completedTasks: number;
    inProgressTasks: number;
    todoTasks: number;
    completionRate: number;
    averageCompletionTime: number;
    overdueTasks: number;
    tasksCompletedThisWeek: number;
    tasksCreatedThisWeek: number;
    burndownData: BurndownPoint[];
    velocityData: VelocityPoint[];
  }
  
  export interface BurndownPoint {
    date: string;
    planned: number;
    actual: number;
  }
  
  export interface VelocityPoint {
    sprint: string;
    completed: number;
    planned: number;
  }
  
  export interface Notification {
    id: string;
    type: 'info' | 'success' | 'warning' | 'error';
    title: string;
    message: string;
    timestamp: Date;
    read: boolean;
    actionUrl?: string;
    actionText?: string;
  }
  
  export interface ActivityLog {
    id: string;
    userId: string;
    userName: string;
    action: 'created' | 'updated' | 'deleted' | 'moved' | 'commented';
    entityType: 'task' | 'column' | 'project';
    entityId: string;
    entityTitle: string;
    details: string;
    timestamp: Date;
  }
  
  export interface KanbanState {
    tasks: Task[];
    columns: ColumnType[];
    projects: Project[];
    users: User[];
    settings: KanbanSettings;
    filters: Filter;
    notifications: Notification[];
    activityLogs: ActivityLog[];
    isLoading: boolean;
    error: string | null;
  }
  
  // イベント型
  export interface TaskEvent {
    type: 'task_created' | 'task_updated' | 'task_deleted' | 'task_moved';
    task: Task;
    previousData?: Partial<Task>;
    userId: string;
    timestamp: Date;
  }
  
  export interface ColumnEvent {
    type: 'column_created' | 'column_updated' | 'column_deleted' | 'column_reordered';
    column: ColumnType;
    previousData?: Partial<ColumnType>;
    userId: string;
    timestamp: Date;
  }
  
  // API レスポンス型
  export interface ApiResponse<T> {
    success: boolean;
    data?: T;
    error?: string;
    message?: string;
  }
  
  export interface PaginatedResponse<T> {
    items: T[];
    total: number;
    page: number;
    pageSize: number;
    hasMore: boolean;
  }
  
  // フォーム型
  export interface TaskFormData {
    title: string;
    description: string;
    priority: 'low' | 'medium' | 'high';
    columnId: string;
    assignee: string;
    dueDate: string;
    tags: string[];
    estimatedHours?: number;
    projectId?: string;
  }
  
  export interface ColumnFormData {
    title: string;
    color: string;
    limit?: number;
  }
  
  export interface ProjectFormData {
    name: string;
    description: string;
    color: string;
    deadline?: string;
    members: string[];
  }
  
  // ドラッグ&ドロップ型
  export interface DragItem {
    id: string;
    type: 'task' | 'column';
    data: Task | ColumnType;
  }
  
  export interface DropResult {
    sourceId: string;
    destinationId: string;
    sourceIndex: number;
    destinationIndex: number;
  }
  
  // カスタムフック型
  export interface UseKanban {
    tasks: Task[];
    columns: ColumnType[];
    isLoading: boolean;
    error: string | null;
    addTask: (task: Omit<Task, 'id' | 'createdAt' | 'updatedAt'>) => Promise<void>;
    updateTask: (taskId: string, updates: Partial<Task>) => Promise<void>;
    deleteTask: (taskId: string) => Promise<void>;
    moveTask: (taskId: string, newColumnId: string) => Promise<void>;
    addColumn: (column: Omit<ColumnType, 'id'>) => Promise<void>;
    updateColumn: (columnId: string, updates: Partial<ColumnType>) => Promise<void>;
    deleteColumn: (columnId: string) => Promise<void>;
    reorderColumns: (columnIds: string[]) => Promise<void>;
  }
  
  export interface UseTaskFilters {
    filteredTasks: Task[];
    filters: Filter;
    setFilters: (filters: Filter) => void;
    clearFilters: () => void;
    activeFiltersCount: number;
  }
  
  export interface UseNotifications {
    notifications: Notification[];
    unreadCount: number;
    addNotification: (notification: Omit<Notification, 'id' | 'timestamp' | 'read'>) => void;
    markAsRead: (notificationId: string) => void;
    markAllAsRead: () => void;
    clearNotifications: () => void;
  }
  
  // エクスポート用のユーティリティ型
  export type TaskPriority = Task['priority'];
  export type ColumnColor = ColumnType['color'];
  export type UserRole = User['role'];
  export type ProjectStatus = Project['status'];
  export type NotificationType = Notification['type'];
  export type ActivityAction = ActivityLog['action'];
  export type EntityType = ActivityLog['entityType'];