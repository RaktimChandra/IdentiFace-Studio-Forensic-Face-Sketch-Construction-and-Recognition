import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import { Plus, FileText, Calendar, AlertCircle, Filter } from 'lucide-react'
import { useAuthStore } from '../stores/authStore'
import { format } from 'date-fns'

export default function CaseManagement() {
  const { token } = useAuthStore()
  const [selectedStatus, setSelectedStatus] = useState('all')
  const [selectedPriority, setSelectedPriority] = useState('all')

  const { data: cases, isLoading } = useQuery({
    queryKey: ['cases', selectedStatus, selectedPriority],
    queryFn: async () => {
      const params = new URLSearchParams()
      if (selectedStatus !== 'all') params.append('status', selectedStatus)
      if (selectedPriority !== 'all') params.append('priority', selectedPriority)
      
      const response = await axios.get(`/api/v1/cases?${params.toString()}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    }
  })

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical': return 'bg-red-100 text-red-700 border-red-300'
      case 'high': return 'bg-orange-100 text-orange-700 border-orange-300'
      case 'medium': return 'bg-yellow-100 text-yellow-700 border-yellow-300'
      case 'low': return 'bg-green-100 text-green-700 border-green-300'
      default: return 'bg-gray-100 text-gray-700 border-gray-300'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'open': return 'bg-blue-100 text-blue-700'
      case 'under_investigation': return 'bg-purple-100 text-purple-700'
      case 'solved': return 'bg-green-100 text-green-700'
      case 'closed': return 'bg-gray-100 text-gray-700'
      case 'cold': return 'bg-slate-100 text-slate-700'
      default: return 'bg-gray-100 text-gray-700'
    }
  }

  return (
    <div className="p-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Case Management</h1>
          <p className="text-gray-600 mt-2">Track and manage investigation cases</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
          <Plus className="w-5 h-5" />
          New Case
        </button>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-xl shadow-sm p-6 mb-6">
        <div className="flex items-center gap-4">
          <Filter className="w-5 h-5 text-gray-600" />
          <select
            value={selectedStatus}
            onChange={(e) => setSelectedStatus(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
          >
            <option value="all">All Status</option>
            <option value="open">Open</option>
            <option value="under_investigation">Under Investigation</option>
            <option value="solved">Solved</option>
            <option value="closed">Closed</option>
            <option value="cold">Cold</option>
          </select>
          <select
            value={selectedPriority}
            onChange={(e) => setSelectedPriority(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
          >
            <option value="all">All Priority</option>
            <option value="critical">Critical</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
        </div>
      </div>

      {/* Cases List */}
      {isLoading ? (
        <div className="text-center py-12">
          <p className="text-gray-600">Loading cases...</p>
        </div>
      ) : cases?.length === 0 ? (
        <div className="bg-white rounded-xl shadow-sm p-12 text-center">
          <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">No cases found</p>
        </div>
      ) : (
        <div className="space-y-4">
          {cases?.map((caseItem: any) => (
            <div key={caseItem.id} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-lg font-semibold text-gray-900">{caseItem.title}</h3>
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${getPriorityColor(caseItem.priority)}`}>
                      {caseItem.priority}
                    </span>
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(caseItem.status)}`}>
                      {caseItem.status.replace('_', ' ')}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 font-mono mb-3">Case #{caseItem.case_number}</p>
                  {caseItem.description && (
                    <p className="text-gray-700 mb-4">{caseItem.description}</p>
                  )}
                  <div className="flex items-center gap-6 text-sm text-gray-600">
                    {caseItem.incident_date && (
                      <div className="flex items-center gap-2">
                        <Calendar className="w-4 h-4" />
                        <span>{format(new Date(caseItem.incident_date), 'MMM dd, yyyy')}</span>
                      </div>
                    )}
                    {caseItem.incident_location && (
                      <div className="flex items-center gap-2">
                        <AlertCircle className="w-4 h-4" />
                        <span>{caseItem.incident_location}</span>
                      </div>
                    )}
                  </div>
                </div>
                <button className="text-sm text-blue-600 hover:text-blue-700 font-medium ml-4">
                  View Details
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
