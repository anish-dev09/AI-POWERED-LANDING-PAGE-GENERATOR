import { useEffect, useState } from 'react';
import { businessAPI } from '../services/api';
import { Plus, Edit2, Trash2, Search } from 'lucide-react';

export default function Businesses() {
  const [businesses, setBusinesses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingBusiness, setEditingBusiness] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    industry: '',
    target_audience: '',
    unique_value_proposition: '',
    tone: 'professional',
    goal: 'lead_generation',
  });

  useEffect(() => {
    fetchBusinesses();
  }, [searchQuery]);

  async function fetchBusinesses() {
    try {
      const params = searchQuery ? { search: searchQuery } : {};
      const response = await businessAPI.getAll(params);
      setBusinesses(response.data);
    } catch (error) {
      console.error('Failed to fetch businesses:', error);
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      if (editingBusiness) {
        await businessAPI.update(editingBusiness.id, formData);
      } else {
        await businessAPI.create(formData);
      }
      setShowForm(false);
      setEditingBusiness(null);
      resetForm();
      fetchBusinesses();
    } catch (error) {
      console.error('Failed to save business:', error);
      alert('Failed to save business. Please try again.');
    }
  }

  async function handleDelete(id) {
    if (!confirm('Are you sure you want to delete this business?')) return;
    try {
      await businessAPI.delete(id);
      fetchBusinesses();
    } catch (error) {
      console.error('Failed to delete business:', error);
      alert('Failed to delete business.');
    }
  }

  function handleEdit(business) {
    setEditingBusiness(business);
    setFormData({
      name: business.name,
      industry: business.industry,
      target_audience: business.target_audience,
      unique_value_proposition: business.unique_value_proposition,
      tone: business.tone,
      goal: business.goal,
    });
    setShowForm(true);
  }

  function resetForm() {
    setFormData({
      name: '',
      industry: '',
      target_audience: '',
      unique_value_proposition: '',
      tone: 'professional',
      goal: 'lead_generation',
    });
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Businesses</h1>
          <p className="text-gray-600 mt-2">Manage your business profiles</p>
        </div>
        <button
          onClick={() => {
            setShowForm(true);
            setEditingBusiness(null);
            resetForm();
          }}
          className="btn-primary flex items-center gap-2"
        >
          <Plus className="w-5 h-5" />
          Add Business
        </button>
      </div>

      {/* Search */}
      <div className="mb-6">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search businesses..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="input-field pl-10"
          />
        </div>
      </div>

      {/* Business Form Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6">
            <h2 className="text-2xl font-bold mb-6">
              {editingBusiness ? 'Edit Business' : 'Create Business'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Business Name *
                </label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="input-field"
                  placeholder="e.g., TechStart Solutions"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Industry *
                </label>
                <input
                  type="text"
                  required
                  value={formData.industry}
                  onChange={(e) => setFormData({ ...formData, industry: e.target.value })}
                  className="input-field"
                  placeholder="e.g., SaaS, E-commerce, Consulting"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Target Audience *
                </label>
                <input
                  type="text"
                  required
                  value={formData.target_audience}
                  onChange={(e) => setFormData({ ...formData, target_audience: e.target.value })}
                  className="input-field"
                  placeholder="e.g., Small business owners, Developers"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Unique Value Proposition
                </label>
                <textarea
                  value={formData.unique_value_proposition}
                  onChange={(e) => setFormData({ ...formData, unique_value_proposition: e.target.value })}
                  className="input-field"
                  rows={3}
                  placeholder="What makes your business unique?"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Tone
                  </label>
                  <select
                    value={formData.tone}
                    onChange={(e) => setFormData({ ...formData, tone: e.target.value })}
                    className="input-field"
                  >
                    <option value="professional">Professional</option>
                    <option value="casual">Casual</option>
                    <option value="friendly">Friendly</option>
                    <option value="formal">Formal</option>
                    <option value="playful">Playful</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Goal
                  </label>
                  <select
                    value={formData.goal}
                    onChange={(e) => setFormData({ ...formData, goal: e.target.value })}
                    className="input-field"
                  >
                    <option value="lead_generation">Lead Generation</option>
                    <option value="brand_awareness">Brand Awareness</option>
                    <option value="sales">Sales</option>
                    <option value="signup">Signup</option>
                  </select>
                </div>
              </div>

              <div className="flex gap-3 pt-4">
                <button type="submit" className="btn-primary flex-1">
                  {editingBusiness ? 'Update' : 'Create'} Business
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowForm(false);
                    setEditingBusiness(null);
                    resetForm();
                  }}
                  className="btn-secondary flex-1"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Business List */}
      {loading ? (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-gray-300 border-t-primary-600"></div>
        </div>
      ) : businesses.length === 0 ? (
        <div className="card text-center py-12">
          <p className="text-gray-600">No businesses found. Create your first one!</p>
        </div>
      ) : (
        <div className="grid gap-6">
          {businesses.map((business) => (
            <div key={business.id} className="card">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h3 className="text-xl font-semibold text-gray-900">{business.name}</h3>
                  <p className="text-gray-600 mt-1">{business.industry}</p>
                  <p className="text-sm text-gray-500 mt-2">
                    <span className="font-medium">Target:</span> {business.target_audience}
                  </p>
                  {business.unique_value_proposition && (
                    <p className="text-sm text-gray-700 mt-2">{business.unique_value_proposition}</p>
                  )}
                  <div className="flex gap-4 mt-3">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      {business.tone}
                    </span>
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      {business.goal.replace('_', ' ')}
                    </span>
                  </div>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleEdit(business)}
                    className="p-2 text-gray-600 hover:text-primary-600 hover:bg-gray-100 rounded-lg"
                  >
                    <Edit2 className="w-5 h-5" />
                  </button>
                  <button
                    onClick={() => handleDelete(business.id)}
                    className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
