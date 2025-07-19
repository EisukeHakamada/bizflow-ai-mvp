// Firebase設定とデータ操作
import { initializeApp } from 'firebase/app';
import { 
  getFirestore, 
  collection, 
  doc, 
  getDocs, 
  addDoc, 
  updateDoc, 
  deleteDoc, 
  onSnapshot,
  query,
  orderBy,
  where,
  Timestamp 
} from 'firebase/firestore';
import { Task, ColumnType } from '../types';

// Firebase設定
const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
  authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,
  storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.REACT_APP_FIREBASE_APP_ID
};

// Firebaseアプリの初期化
const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);

// コレクション参照
export const tasksCollection = collection(db, 'tasks');
export const columnsCollection = collection(db, 'columns');

// データ型変換ヘルパー
const convertFirestoreTask = (doc: any): Task => ({
  id: doc.id,
  title: doc.data().title,
  description: doc.data().description || '',
  priority: doc.data().priority || 'medium',
  columnId: doc.data().columnId,
  assignee: doc.data().assignee || '',
  dueDate: doc.data().dueDate || '',
  tags: doc.data().tags || [],
  createdAt: doc.data().createdAt?.toDate() || new Date(),
  updatedAt: doc.data().updatedAt?.toDate() || new Date(),
});

const convertFirestoreColumn = (doc: any): ColumnType => ({
  id: doc.id,
  title: doc.data().title,
  color: doc.data().color,
  order: doc.data().order || 0,
  taskIds: doc.data().taskIds || [],
});

// タスク操作
export const taskOperations = {
  // 全タスクを取得
  async getAllTasks(): Promise<Task[]> {
    try {
      const q = query(tasksCollection, orderBy('createdAt', 'desc'));
      const querySnapshot = await getDocs(q);
      return querySnapshot.docs.map(convertFirestoreTask);
    } catch (error) {
      console.error('タスクの取得に失敗しました:', error);
      throw error;
    }
  },

  // プロジェクト別タスクを取得
  async getTasksByProject(projectId: string): Promise<Task[]> {
    try {
      const q = query(
        tasksCollection, 
        where('projectId', '==', projectId),
        orderBy('createdAt', 'desc')
      );
      const querySnapshot = await getDocs(q);
      return querySnapshot.docs.map(convertFirestoreTask);
    } catch (error) {
      console.error('プロジェクトタスクの取得に失敗しました:', error);
      throw error;
    }
  },

  // タスクを追加
  async addTask(task: Omit<Task, 'id' | 'createdAt' | 'updatedAt'>): Promise<string> {
    try {
      const docRef = await addDoc(tasksCollection, {
        ...task,
        createdAt: Timestamp.now(),
        updatedAt: Timestamp.now(),
      });
      return docRef.id;
    } catch (error) {
      console.error('タスクの追加に失敗しました:', error);
      throw error;
    }
  },

  // タスクを更新
  async updateTask(taskId: string, updates: Partial<Task>): Promise<void> {
    try {
      const taskRef = doc(db, 'tasks', taskId);
      await updateDoc(taskRef, {
        ...updates,
        updatedAt: Timestamp.now(),
      });
    } catch (error) {
      console.error('タスクの更新に失敗しました:', error);
      throw error;
    }
  },

  // タスクを削除
  async deleteTask(taskId: string): Promise<void> {
    try {
      const taskRef = doc(db, 'tasks', taskId);
      await deleteDoc(taskRef);
    } catch (error) {
      console.error('タスクの削除に失敗しました:', error);
      throw error;
    }
  },

  // タスクのカラム移動
  async moveTask(taskId: string, newColumnId: string): Promise<void> {
    try {
      await this.updateTask(taskId, { columnId: newColumnId });
    } catch (error) {
      console.error('タスクの移動に失敗しました:', error);
      throw error;
    }
  },

  // リアルタイムリスナー
  onTasksChange(callback: (tasks: Task[]) => void): () => void {
    const q = query(tasksCollection, orderBy('createdAt', 'desc'));
    return onSnapshot(q, (querySnapshot) => {
      const tasks = querySnapshot.docs.map(convertFirestoreTask);
      callback(tasks);
    });
  },
};

// カラム操作
export const columnOperations = {
  // 全カラムを取得
  async getAllColumns(): Promise<ColumnType[]> {
    try {
      const q = query(columnsCollection, orderBy('order', 'asc'));
      const querySnapshot = await getDocs(q);
      return querySnapshot.docs.map(convertFirestoreColumn);
    } catch (error) {
      console.error('カラムの取得に失敗しました:', error);
      throw error;
    }
  },

  // カラムを追加
  async addColumn(column: Omit<ColumnType, 'id'>): Promise<string> {
    try {
      const docRef = await addDoc(columnsCollection, column);
      return docRef.id;
    } catch (error) {
      console.error('カラムの追加に失敗しました:', error);
      throw error;
    }
  },

  // カラムを更新
  async updateColumn(columnId: string, updates: Partial<ColumnType>): Promise<void> {
    try {
      const columnRef = doc(db, 'columns', columnId);
      await updateDoc(columnRef, updates);
    } catch (error) {
      console.error('カラムの更新に失敗しました:', error);
      throw error;
    }
  },

  // カラムを削除
  async deleteColumn(columnId: string): Promise<void> {
    try {
      const columnRef = doc(db, 'columns', columnId);
      await deleteDoc(columnRef);
    } catch (error) {
      console.error('カラムの削除に失敗しました:', error);
      throw error;
    }
  },

  // リアルタイムリスナー
  onColumnsChange(callback: (columns: ColumnType[]) => void): () => void {
    const q = query(columnsCollection, orderBy('order', 'asc'));
    return onSnapshot(q, (querySnapshot) => {
      const columns = querySnapshot.docs.map(convertFirestoreColumn);
      callback(columns);
    });
  },
};

// 初期データセットアップ
export const setupInitialData = async (): Promise<void> => {
  try {
    // 既存のカラムを確認
    const existingColumns = await columnOperations.getAllColumns();
    
    if (existingColumns.length === 0) {
      // 初期カラムを作成
      const initialColumns = [
        { title: 'To Do', color: '#ef4444', order: 0, taskIds: [] },
        { title: 'In Progress', color: '#f97316', order: 1, taskIds: [] },
        { title: 'Review', color: '#3b82f6', order: 2, taskIds: [] },
        { title: 'Done', color: '#10b981', order: 3, taskIds: [] },
      ];

      for (const column of initialColumns) {
        await columnOperations.addColumn(column);
      }

      console.log('初期カラムを作成しました');
    }

    // 既存のタスクを確認
    const existingTasks = await taskOperations.getAllTasks();
    
    if (existingTasks.length === 0) {
      // 再度カラムを取得（IDが必要）
      const columns = await columnOperations.getAllColumns();
      
      // 初期タスクを作成
      const initialTasks = [
        {
          title: 'プロジェクト企画書作成',
          description: '新規プロジェクトの企画書を作成する',
          priority: 'high' as const,
          columnId: columns[0]?.id || '',
          assignee: '田中太郎',
          dueDate: '2025-07-25',
          tags: ['企画', '優先'],
        },
        {
          title: 'UIデザイン検討',
          description: 'ユーザーインターフェースのデザインを検討',
          priority: 'medium' as const,
          columnId: columns[0]?.id || '',
          assignee: '鈴木花子',
          dueDate: '2025-07-30',
          tags: ['デザイン'],
        },
        {
          title: 'API仕様書作成',
          description: 'バックエンドAPIの仕様書を作成',
          priority: 'high' as const,
          columnId: columns[1]?.id || '',
          assignee: '佐藤次郎',
          dueDate: '2025-07-28',
          tags: ['API', '技術'],
        },
      ];

      for (const task of initialTasks) {
        await taskOperations.addTask(task);
      }

      console.log('初期タスクを作成しました');
    }
  } catch (error) {
    console.error('初期データのセットアップに失敗しました:', error);
  }
};

// プロジェクト管理
export const projectOperations = {
  // プロジェクト統計を取得
  async getProjectStats(projectId?: string): Promise<{
    totalTasks: number;
    completedTasks: number;
    inProgressTasks: number;
    todoTasks: number;
    completionRate: number;
  }> {
    try {
      const tasks = projectId 
        ? await taskOperations.getTasksByProject(projectId)
        : await taskOperations.getAllTasks();
      
      const totalTasks = tasks.length;
      const completedTasks = tasks.filter(task => task.columnId.includes('done') || task.columnId.includes('完了')).length;
      const inProgressTasks = tasks.filter(task => task.columnId.includes('progress') || task.columnId.includes('進行')).length;
      const todoTasks = tasks.filter(task => task.columnId.includes('todo') || task.columnId.includes('待機')).length;
      const completionRate = totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0;

      return {
        totalTasks,
        completedTasks,
        inProgressTasks,
        todoTasks,
        completionRate,
      };
    } catch (error) {
      console.error('プロジェクト統計の取得に失敗しました:', error);
      throw error;
    }
  },
};

export default app;