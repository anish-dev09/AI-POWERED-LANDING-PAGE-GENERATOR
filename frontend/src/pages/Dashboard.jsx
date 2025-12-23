import { useEffect, useState } from 'react';
import { businessAPI, landingPageAPI } from '../services/api';
import { TrendingUp, Building2, FileText, Eye } from 'lucide-react';

export default function Dashboard() {
  const [stats, setStats] = useState({
    businesses: 0,
    landingPages: 0,
    published: 0,
    loading: true,
  });

  useEffect(() => {
    async function fetchStats() {
      try {
        const [businessCount, pageCount] = await Promise.all([
          businessAPI.getCount(),
          landingPageAPI.getCount(),
        ]);
        
        // Get published count
        const pagesRes = await landingPageAPI.getAll({ published_only: true });
        
        setStats({
          businesses: businessCount.data.count,
          landingPages: pageCount.data.count,
          published: pagesRes.data.length,
          loading: false,
        });
      } catch (error) {
        console.error('Failed to fetch stats:', error);
        setStats(prev => ({ ...prev, loading: false }));
      }
    }
    
    fetchStats();
  }, []);

  const statCards = [
    {
      name: 'Total Businesses',
      value: stats.businesses,
      icon: Building2,
      color: 'bg-blue-500',
    },
    {
      name: 'Landing Pages',
      value: stats.landingPages,
      icon: FileText,
      color: 'bg-purple-500',
    },
    {
      name: 'Published Pages',
      value: stats.published,
      icon: Eye,
      color: 'bg-green-500',
    },
    {
      name: 'Total Views',
      value: '0',
      icon: TrendingUp,
      color: 'bg-orange-500',
    },
  ];

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">Welcome to your AI Landing Page Generator</p>
      </div>

      {stats.loading ? (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-gray-300 border-t-primary-600"></div>
          <p className="mt-4 text-gray-600">Loading statistics...</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {statCards.map((stat) => (
              <div key={stat.name} className="card">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">{stat.name}</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">{stat.value}</p>
                  </div>
                  <div className={`${stat.color} p-3 rounded-lg`}>
                    <stat.icon className="w-6 h-6 text-white" />
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <a
                href="/businesses"
                className="p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition-colors text-center"
              >
                <Building2 className="w-8 h-8 mx-auto text-gray-400 mb-2" />
                <p className="font-medium text-gray-900">Create Business</p>
                <p className="text-sm text-gray-600 mt-1">Add a new business profile</p>
              </a>
              
              <a
                href="/generate"
                className="p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition-colors text-center"
              >
                <FileText className="w-8 h-8 mx-auto text-gray-400 mb-2" />
                <p className="font-medium text-gray-900">Generate Page</p>
                <p className="text-sm text-gray-600 mt-1">Create AI landing page</p>
              </a>
              
              <a
                href="/landing-pages"
                className="p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition-colors text-center"
              >
                <Eye className="w-8 h-8 mx-auto text-gray-400 mb-2" />
                <p className="font-medium text-gray-900">View Pages</p>
                <p className="text-sm text-gray-600 mt-1">Browse all landing pages</p>
              </a>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
