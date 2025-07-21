// 型定義ファイル - TaskStatus型追加

export type TaskStatus = 'todo' | 'in-progress' | 'review' | 'done';

export interface Task {
  id: string;
  title: string;
  description: string;
  priority: 'low' | 'medium' | 'high';
  status?: TaskStatus;
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
  limit?: number;
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

export interface ProjectStats {
  totalTasks: number;
  completedTasks: number;
  inProgressTasks: number;
  todoTasks: number;
  completionRate: number;
  averageCompletionTime?: number;
  overdueTasks?: number;
  tasksCompletedThisWeek?: number;
  tasksCreatedThisWeek?: number;
  burndownData?: BurndownPoint[];
  velocityData?: VelocityPoint[];
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

export type TaskPriority = Task['priority'];
export type ColumnColor = ColumnType['color'];
export type UserRole = User['role'];
export type ProjectStatus = Project['status'];
export type NotificationType = Notification['type'];
export type ActivityAction = ActivityLog['action'];
export type EntityType = ActivityLog['entityType'];
