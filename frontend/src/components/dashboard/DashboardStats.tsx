import React from 'react';
import { CheckSquare, AlertTriangle, Clock } from 'lucide-react';
import Card from '../ui/Card';
import Button from '../ui/Button';
import { DashboardStat } from '../../types';

const DashboardStats: React.FC = () => {
  const stats: DashboardStat[] = [
    {
      id: '1',
      title: 'Validated Term Sheets',
      count: 42,
      icon: 'check',
      bgColor: 'bg-green-50',
    },
    {
      id: '2',
      title: 'Errors Caught',
      count: 12,
      icon: 'alert',
      bgColor: 'bg-red-50',
    },
    {
      id: '3',
      title: 'Pending Validations',
      count: 5,
      icon: 'clock',
      bgColor: 'bg-yellow-50',
    },
  ];

  const renderIcon = (iconName: string) => {
    switch (iconName) {
      case 'check':
        return <CheckSquare className="w-6 h-6 text-green-600" />;
      case 'alert':
        return <AlertTriangle className="w-6 h-6 text-red-600" />;
      case 'clock':
        return <Clock className="w-6 h-6 text-yellow-600" />;
      default:
        return null;
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      {stats.map((stat) => (
        <Card key={stat.id} bgColor={stat.bgColor} className="flex flex-col items-center">
          {renderIcon(stat.icon)}
          <h3 className="text-lg font-medium mt-2">{stat.count}</h3>
          <p className="text-gray-700">{stat.title}</p>
          <Button variant="outline" size="sm" className="mt-4">
            View all
          </Button>
        </Card>
      ))}
    </div>
  );
};

export default DashboardStats;