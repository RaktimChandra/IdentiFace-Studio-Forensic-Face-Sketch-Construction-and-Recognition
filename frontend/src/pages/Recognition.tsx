import { useState } from 'react'
import { useDropzone } from 'react-dropzone'
import axios from 'axios'
import { Upload, Search, AlertCircle, CheckCircle, User } from 'lucide-react'
import { useAuthStore } from '../stores/authStore'
import toast from 'react-hot-toast'

export default function Recognition() {
  const { token } = useAuthStore()
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [results, setResults] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg']
    },
    maxFiles: 1,
    onDrop: (acceptedFiles) => {
      const file = acceptedFiles[0]
      setUploadedFile(file)
      setPreviewUrl(URL.createObjectURL(file))
      setResults(null)
    }
  })

  const handleRecognition = async () => {
    if (!uploadedFile) {
      toast.error('Please upload an image first')
      return
    }

    setLoading(true)
    try {
      const formData = new FormData()
      formData.append('file', uploadedFile)

      const response = await axios.post('/api/v1/recognition/match-photo', formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data'
        },
        params: {
          min_score: 0.4,
          max_results: 10
        }
      })

      setResults(response.data)
      toast.success(`Found ${response.data.total_matches} matches!`)
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Recognition failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Face Recognition</h1>
          <p className="text-gray-600 mt-2">Upload a photo or sketch to find matches</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Upload Section */}
          <div>
            <div className="bg-white rounded-xl shadow-sm p-6 mb-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Upload Image</h2>
              
              <div
                {...getRootProps()}
                className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition ${
                  isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-blue-400'
                }`}
              >
                <input {...getInputProps()} />
                <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                {isDragActive ? (
                  <p className="text-blue-600 font-medium">Drop image here...</p>
                ) : (
                  <>
                    <p className="text-gray-900 font-medium mb-2">
                      Drag & drop an image here
                    </p>
                    <p className="text-sm text-gray-600">or click to browse</p>
                    <p className="text-xs text-gray-500 mt-2">PNG, JPG up to 10MB</p>
                  </>
                )}
              </div>

              {previewUrl && (
                <div className="mt-6">
                  <p className="text-sm font-medium text-gray-700 mb-2">Preview:</p>
                  <img src={previewUrl} alt="Preview" className="w-full rounded-lg border border-gray-200" />
                </div>
              )}
            </div>

            <button
              onClick={handleRecognition}
              disabled={!uploadedFile || loading}
              className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Search className="w-5 h-5" />
              {loading ? 'Searching...' : 'Run Face Recognition'}
            </button>
          </div>

          {/* Results Section */}
          <div>
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Results</h2>

              {!results ? (
                <div className="text-center py-12">
                  <AlertCircle className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-600">Upload an image to start recognition</p>
                </div>
              ) : results.total_matches === 0 ? (
                <div className="text-center py-12">
                  <AlertCircle className="w-12 h-12 text-yellow-500 mx-auto mb-4" />
                  <p className="text-gray-900 font-medium mb-2">No Matches Found</p>
                  <p className="text-sm text-gray-600">No suspects matched above the similarity threshold</p>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="flex items-center justify-between mb-4 p-4 bg-green-50 rounded-lg">
                    <div className="flex items-center gap-3">
                      <CheckCircle className="w-5 h-5 text-green-600" />
                      <span className="font-medium text-gray-900">
                        {results.total_matches} Match{results.total_matches > 1 ? 'es' : ''} Found
                      </span>
                    </div>
                    <span className="text-sm text-gray-600">
                      {results.processing_time.toFixed(2)}s
                    </span>
                  </div>

                  <div className="space-y-3 max-h-[600px] overflow-y-auto">
                    {results.matches.map((match: any, index: number) => (
                      <div key={index} className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition">
                        <div className="flex items-start gap-4">
                          <div className="w-16 h-16 bg-gray-100 rounded-lg flex items-center justify-center flex-shrink-0">
                            {match.suspect_info.photo_url ? (
                              <img src={match.suspect_info.photo_url} alt="Suspect" className="w-full h-full object-cover rounded-lg" />
                            ) : (
                              <User className="w-8 h-8 text-gray-400" />
                            )}
                          </div>
                          <div className="flex-1">
                            <div className="flex items-center justify-between mb-2">
                              <h3 className="font-semibold text-gray-900">
                                {match.suspect_info.first_name} {match.suspect_info.last_name}
                              </h3>
                              <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                                match.confidence === 'high' ? 'bg-green-100 text-green-700' :
                                match.confidence === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                                'bg-orange-100 text-orange-700'
                              }`}>
                                {match.confidence} confidence
                              </span>
                            </div>
                            {match.suspect_info.alias && (
                              <p className="text-sm text-gray-600 mb-2">Alias: {match.suspect_info.alias}</p>
                            )}
                            <div className="flex items-center gap-4">
                              <div className="flex-1">
                                <div className="flex items-center justify-between text-xs text-gray-600 mb-1">
                                  <span>Similarity</span>
                                  <span className="font-semibold">{(match.similarity_score * 100).toFixed(1)}%</span>
                                </div>
                                <div className="w-full bg-gray-200 rounded-full h-2">
                                  <div
                                    className="bg-blue-600 h-2 rounded-full"
                                    style={{ width: `${match.similarity_score * 100}%` }}
                                  />
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
