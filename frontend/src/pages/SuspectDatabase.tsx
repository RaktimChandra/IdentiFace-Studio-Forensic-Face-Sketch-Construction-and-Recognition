import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import { Search, Plus, Filter, User, AlertCircle } from 'lucide-react'
import { useAuthStore } from '../stores/authStore'

export default function SuspectDatabase() {
  const { token } = useAuthStore()
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedStatus, setSelectedStatus] = useState('all')

  const { data: suspects, isLoading } = useQuery({
    queryKey: ['suspects', selectedStatus],
    queryFn: async () => {
      const params = selectedStatus !== 'all' ? `?status=${selectedStatus}` : ''
      const response = await axios.get(`/api/v1/suspects${params}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    }
  })

  const filteredSuspects = suspects?.filter((suspect: any) =>
    `${suspect.first_name} ${suspect.last_name} ${suspect.alias}`.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <div className="p-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Suspect Database</h1>
          <p className="text-gray-600 mt-2">Manage suspect records and photos</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
          <Plus className="w-5 h-5" />
          Add Suspect
        </button>
      </div>

      {/* Search & Filters */}
      <div className="bg-white rounded-xl shadow-sm p-6 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="md:col-span-2 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search by name or alias..."
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
            />
          </div>
          <select
            value={selectedStatus}
            onChange={(e) => setSelectedStatus(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
          >
            <option value="all">All Status</option>
            <option value="active">Active</option>
            <option value="arrested">Arrested</option>
            <option value="cleared">Cleared</option>
          </select>
        </div>
      </div>

      {/* Suspects Grid */}
      {isLoading ? (
        <div className="text-center py-12">
          <p className="text-gray-600">Loading suspects...</p>
        </div>
      ) : filteredSuspects?.length === 0 ? (
        <div className="bg-white rounded-xl shadow-sm p-12 text-center">
          <AlertCircle className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">No suspects found</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredSuspects?.map((suspect: any) => (
            <div key={suspect.id} className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition">
              <div className="aspect-square bg-gray-100 flex items-center justify-center">
                {suspect.photo_url ? (
                  <img src={suspect.photo_url} alt={suspect.first_name} className="w-full h-full object-cover" />
                ) : (
                  <User className="w-24 h-24 text-gray-400" />
                )}
              </div>
              <div className="p-4">
                <h3 className="font-semibold text-lg text-gray-900">
                  {suspect.first_name} {suspect.last_name}
                </h3>
                {suspect.alias && (
                  <p className="text-sm text-gray-600 mt-1">Alias: {suspect.alias}</p>
                )}
                <div className="mt-3 flex items-center justify-between">
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                    suspect.status === 'active' ? 'bg-red-100 text-red-700' :
                    suspect.status === 'arrested' ? 'bg-orange-100 text-orange-700' :
                    'bg-green-100 text-green-700'
                  }`}>
                    {suspect.status}
                  </span>
                  <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">
                    View Details
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
