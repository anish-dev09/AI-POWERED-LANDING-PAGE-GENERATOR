import { useEffect, useState } from 'react';
import { businessAPI, landingPageAPI } from '../services/api';
import { Sparkles, Palette, Loader2 } from 'lucide-react';

const THEMES = ['modern', 'minimal', 'bold', 'elegant'];
const COLORS = [
  { name: 'Purple', primary: '#8B5CF6', secondary: '#EC4899' },
  { name: 'Blue', primary: '#3B82F6', secondary: '#06B6D4' },
  { name: 'Green', primary: '#10B981', secondary: '#14B8A6' },
  { name: 'Orange', primary: '#F97316', secondary: '#EAB308' },
  { name: 'Red', primary: '#EF4444', secondary: '#F59E0B' },
];

export default function GeneratePage() {
  const [businesses, setBusinesses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedBusiness, setSelectedBusiness] = useState('');
  const [selectedTheme, setSelectedTheme] = useState('modern');
  const [selectedColor, setSelectedColor] = useState(COLORS[0]);
  const [generatedPage, setGeneratedPage] = useState(null);

  useEffect(() => {
    async function fetchBusinesses() {
      try {
        const response = await businessAPI.getAll();
        setBusinesses(response.data);
      } catch (error) {
        console.error('Failed to fetch businesses:', error);
      }
    }
    fetchBusinesses();
  }, []);

  async function handleGenerate() {
    if (!selectedBusiness) {
      alert('Please select a business first');
      return;
    }

    setLoading(true);
    setGeneratedPage(null);

    try {
      const customization = {
        theme: selectedTheme,
        primary_color: selectedColor.primary,
        secondary_color: selectedColor.secondary,
      };

      const response = await landingPageAPI.generate(selectedBusiness, customization);
      setGeneratedPage(response.data);
      alert('Landing page generated successfully!');
    } catch (error) {
      console.error('Failed to generate page:', error);
      alert('Failed to generate landing page. Please try again.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Generate Landing Page</h1>
        <p className="text-gray-600 mt-2">Create an AI-powered landing page for your business</p>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        {/* Configuration */}
        <div className="space-y-6">
          {/* Business Selection */}
          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Select Business</h2>
            {businesses.length === 0 ? (
              <p className="text-gray-600">No businesses found. Create one first.</p>
            ) : (
              <select
                value={selectedBusiness}
                onChange={(e) => setSelectedBusiness(e.target.value)}
                className="input-field"
              >
                <option value="">Choose a business...</option>
                {businesses.map((business) => (
                  <option key={business.id} value={business.id}>
                    {business.name} - {business.industry}
                  </option>
                ))}
              </select>
            )}
          </div>

          {/* Theme Selection */}
          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <Palette className="w-5 h-5" />
              Choose Theme
            </h2>
            <div className="grid grid-cols-2 gap-3">
              {THEMES.map((theme) => (
                <button
                  key={theme}
                  onClick={() => setSelectedTheme(theme)}
                  className={`p-4 border-2 rounded-lg capitalize transition-all ${
                    selectedTheme === theme
                      ? 'border-primary-600 bg-primary-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  {theme}
                </button>
              ))}
            </div>
          </div>

          {/* Color Selection */}
          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Color Scheme</h2>
            <div className="grid grid-cols-5 gap-3">
              {COLORS.map((color) => (
                <button
                  key={color.name}
                  onClick={() => setSelectedColor(color)}
                  className={`relative aspect-square rounded-lg border-2 transition-all ${
                    selectedColor.name === color.name
                      ? 'border-gray-900 scale-110'
                      : 'border-gray-200 hover:scale-105'
                  }`}
                  style={{
                    background: `linear-gradient(135deg, ${color.primary} 0%, ${color.secondary} 100%)`,
                  }}
                  title={color.name}
                >
                  {selectedColor.name === color.name && (
                    <div className="absolute inset-0 flex items-center justify-center">
                      <div className="w-3 h-3 bg-white rounded-full border-2 border-gray-900"></div>
                    </div>
                  )}
                </button>
              ))}
            </div>
            <p className="text-sm text-gray-600 mt-3">Selected: {selectedColor.name}</p>
          </div>

          {/* Generate Button */}
          <button
            onClick={handleGenerate}
            disabled={loading || !selectedBusiness}
            className="btn-primary w-full flex items-center justify-center gap-2 py-4 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <>
                <Loader2 className="w-6 h-6 animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <Sparkles className="w-6 h-6" />
                Generate Landing Page
              </>
            )}
          </button>
        </div>

        {/* Preview */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Preview</h2>
          {loading ? (
            <div className="text-center py-12">
              <Loader2 className="w-12 h-12 animate-spin text-primary-600 mx-auto" />
              <p className="text-gray-600 mt-4">AI is generating your landing page...</p>
              <p className="text-sm text-gray-500 mt-2">This may take 30-60 seconds</p>
            </div>
          ) : generatedPage ? (
            <div className="space-y-4">
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <p className="text-green-800 font-medium">✓ Page Generated Successfully!</p>
                <p className="text-sm text-green-600 mt-1">ID: {generatedPage.id}</p>
              </div>
              
              <div className="border border-gray-200 rounded-lg p-4">
                <h3 className="font-semibold text-gray-900">{generatedPage.headline}</h3>
                <p className="text-sm text-gray-600 mt-2">{generatedPage.subheadline}</p>
                <div className="flex gap-2 mt-4">
                  <span className="text-xs px-2 py-1 bg-gray-100 rounded">
                    Theme: {generatedPage.theme}
                  </span>
                  <span className="text-xs px-2 py-1 bg-gray-100 rounded">
                    {generatedPage.is_published ? 'Published' : 'Draft'}
                  </span>
                </div>
              </div>

              {generatedPage.html_file_path && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <p className="text-sm text-blue-800">
                    <span className="font-medium">HTML:</span> {generatedPage.html_file_path}
                  </p>
                  <p className="text-sm text-blue-800 mt-1">
                    <span className="font-medium">CSS:</span> {generatedPage.css_file_path}
                  </p>
                </div>
              )}

              <a
                href="/landing-pages"
                className="btn-primary w-full inline-block text-center"
              >
                View All Pages
              </a>
            </div>
          ) : (
            <div className="text-center py-12 text-gray-500">
              <Sparkles className="w-16 h-16 mx-auto text-gray-300 mb-4" />
              <p>Configure settings and click generate to create your landing page</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
