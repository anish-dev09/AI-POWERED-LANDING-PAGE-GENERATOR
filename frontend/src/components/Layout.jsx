import { Outlet, NavLink } from 'react-router-dom';
import { LayoutDashboard, Building2, Sparkles, FileText } from 'lucide-react';
import clsx from 'clsx';

const navigation = [
  { name: 'Dashboard', to: '/dashboard', icon: LayoutDashboard },
  { name: 'Businesses', to: '/businesses', icon: Building2 },
  { name: 'Generate Page', to: '/generate', icon: Sparkles },
  { name: 'Landing Pages', to: '/landing-pages', icon: FileText },
];

export default function Layout() {
  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
        <div className="p-6 border-b border-gray-200">
          <h1 className="text-2xl font-bold text-primary-600">Landing Page AI</h1>
          <p className="text-sm text-gray-600 mt-1">Generator Dashboard</p>
        </div>
        
        <nav className="flex-1 p-4 space-y-2">
          {navigation.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                clsx(
                  'flex items-center gap-3 px-4 py-3 rounded-lg transition-colors',
                  isActive
                    ? 'bg-primary-50 text-primary-700 font-medium'
                    : 'text-gray-700 hover:bg-gray-100'
                )
              }
            >
              <item.icon className="w-5 h-5" />
              {item.name}
            </NavLink>
          ))}
        </nav>
        
        <div className="p-4 border-t border-gray-200">
          <div className="text-xs text-gray-500">
            <p>Version 1.0.0</p>
            <p className="mt-1">© 2025 Landing Page AI</p>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        <div className="max-w-7xl mx-auto p-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
