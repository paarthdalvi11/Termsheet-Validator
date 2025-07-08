export interface User {
  id: string;
  name: string;
  role: string;
  username: string;
}

export interface TermSheet {
  id: string;
  fileName: string;
  uploadDate: string;
  status: 'Validated' | 'Error' | 'Pending';
  actions?: string[];
}

export interface ValidationClause {
  id: string;
  clause: string;
  date: string;
  status: 'Valid' | 'Invalid' | 'Warning';
}

export interface DashboardStat {
  id: string;
  title: string;
  count: number;
  icon: string;
  bgColor: string;
}