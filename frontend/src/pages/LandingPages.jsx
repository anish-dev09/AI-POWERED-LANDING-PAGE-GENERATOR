import { useEffect, useState } from 'react';
import { landingPageAPI } from '../services/api';
import { Eye, EyeOff, Trash2, FileText, ExternalLink } from 'lucide-react';

export default function LandingPages() {
  const [pages, setPages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedPage, setSelectedPage] = useState(null);

  useEffect(() => {
    fetchPages();
  }, []);

  async function fetchPages() {
    try {
      const response = await landingPageAPI.getAll();
      setPages(response.data);
    } catch (error) {
      console.error('Failed to fetch pages:', error);
    } finally {
      setLoading(false);
    }
  }

  async function handlePublish(id, isPublished) {
    try {
      if (isPublished) {
        await landingPageAPI.unpublish(id);
      } else {
        await landingPageAPI.publish(id);
      }
      fetchPages();
    } catch (error) {
      console.error('Failed to update publish status:', error);
      alert('Failed to update publish status');
    }
  }

  async function handleDelete(id) {
    if (!confirm('Are you sure you want to delete this landing page?')) return;
    try {
      await landingPageAPI.delete(id);
      fetchPages();
    } catch (error) {
      console.error('Failed to delete page:', error);
      alert('Failed to delete page');
    }
  }

  async function handleView(page) {
    try {
      // Track view
      await landingPageAPI.trackView(page.id);
      
      // Get full page details
      const response = await landingPageAPI.getById(page.id);
      setSelectedPage(response.data);
    } catch (error) {
      console.error('Failed to load page details:', error);
    }
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Landing Pages</h1>
        <p className="text-gray-600 mt-2">Manage and preview your generated landing pages</p>
      </div>

      {loading ? (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-gray-300 border-t-primary-600"></div>
        </div>
      ) : pages.length === 0 ? (
        <div className="card text-center py-12">
          <FileText className="w-16 h-16 mx-auto text-gray-300 mb-4" />
          <p className="text-gray-600">No landing pages yet. Generate your first one!</p>
          <a href="/generate" className="btn-primary inline-flex items-center gap-2 mt-4">
            Generate Page
          </a>
        </div>
      ) : (
        <div className="grid gap-6">
          {pages.map((page) => (
            <div key={page.id} className="card">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h3 className="text-xl font-semibold text-gray-900">{page.headline}</h3>
                  <p className="text-gray-600 mt-1">{page.subheadline}</p>
                  
                  <div className="flex items-center gap-4 mt-4">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      page.is_published
                        ? 'bg-green-100 text-green-800'
                        : 'bg-gray-100 text-gray-800'
                    }`}>
                      {page.is_published ? 'Published' : 'Draft'}
                    </span>
                    <span className="text-sm text-gray-500">
                      Theme: {page.theme}
                    </span>
                    <span className="text-sm text-gray-500 flex items-center gap-1">
                      <Eye className="w-4 h-4" />
                      {page.views} views
                    </span>
                  </div>

                  {page.html_file_path && (
                    <p className="text-xs text-gray-500 mt-3">
                      {page.html_file_path}
                    </p>
                  )}
                </div>

                <div className="flex gap-2 ml-4">
                  <button
                    onClick={() => handleView(page)}
                    className="p-2 text-gray-600 hover:text-primary-600 hover:bg-gray-100 rounded-lg"
                    title="View Details"
                  >
                    <ExternalLink className="w-5 h-5" />
                  </button>
                  <button
                    onClick={() => handlePublish(page.id, page.is_published)}
                    className="p-2 text-gray-600 hover:text-green-600 hover:bg-green-50 rounded-lg"
                    title={page.is_published ? 'Unpublish' : 'Publish'}
                  >
                    {page.is_published ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                  <button
                    onClick={() => handleDelete(page.id)}
                    className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg"
                    title="Delete"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Preview Modal */}
      {selectedPage && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="sticky top-0 bg-white border-b border-gray-200 p-6 flex items-center justify-between">
              <h2 className="text-2xl font-bold">{selectedPage.headline}</h2>
              <button
                onClick={() => setSelectedPage(null)}
                className="text-gray-500 hover:text-gray-700 text-2xl"
              >
                ×
              </button>
            </div>

            <div className="p-6 space-y-6">
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Subheadline</h3>
                <p className="text-gray-700">{selectedPage.subheadline}</p>
              </div>

              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Call to Action</h3>
                <p className="text-gray-700">{selectedPage.cta_text}</p>
              </div>

              {selectedPage.features && selectedPage.features.length > 0 && (
                <div>
                  <h3 className="font-semibold text-gray-900 mb-3">Features</h3>
                  <div className="grid gap-3">
                    {selectedPage.features.map((feature, idx) => (
                      <div key={idx} className="border border-gray-200 rounded-lg p-4">
                        <h4 className="font-medium text-gray-900">{feature.title}</h4>
                        <p className="text-sm text-gray-600 mt-1">{feature.description}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {selectedPage.testimonials && selectedPage.testimonials.length > 0 && (
                <div>
                  <h3 className="font-semibold text-gray-900 mb-3">Testimonials</h3>
                  <div className="grid gap-3">
                    {selectedPage.testimonials.map((testimonial, idx) => (
                      <div key={idx} className="border border-gray-200 rounded-lg p-4">
                        <p className="text-gray-700 italic">"{testimonial.text}"</p>
                        <p className="text-sm font-medium text-gray-900 mt-2">
                          {testimonial.author}
                          {testimonial.role && ` - ${testimonial.role}`}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="grid grid-cols-2 gap-4 pt-4 border-t border-gray-200">
                <div>
                  <p className="text-sm text-gray-600">Theme</p>
                  <p className="font-medium text-gray-900 capitalize">{selectedPage.theme}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Views</p>
                  <p className="font-medium text-gray-900">{selectedPage.views}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Status</p>
                  <p className="font-medium text-gray-900">
                    {selectedPage.is_published ? 'Published' : 'Draft'}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Colors</p>
                  <div className="flex gap-2 mt-1">
                    <div
                      className="w-6 h-6 rounded border border-gray-300"
                      style={{ backgroundColor: selectedPage.primary_color }}
                      title="Primary"
                    ></div>
                    <div
                      className="w-6 h-6 rounded border border-gray-300"
                      style={{ backgroundColor: selectedPage.secondary_color }}
                      title="Secondary"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
