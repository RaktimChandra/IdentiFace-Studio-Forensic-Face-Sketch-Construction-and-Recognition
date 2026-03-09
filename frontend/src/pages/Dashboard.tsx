import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import { Users, FileText, Image, CheckCircle, TrendingUp, AlertTriangle } from 'lucide-react'
import { useAuthStore } from '../stores/authStore'

export default function Dashboard() {
  const { token, user } = useAuthStore()

  const { data: stats } = useQuery({
    queryKey: ['recognition-stats'],
    queryFn: async () => {
      const response = await axios.get('/api/v1/recognition/stats', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    }
  })

  const statCards = [
    {
      title: 'Total Suspects',
      value: stats?.total_suspects || 0,
      icon: Users,
      color: 'bg-blue-500',
      change: '+12%'
    },
    {
      title: 'Active Cases',
      value: stats?.total_cases || 0,
      icon: FileText,
      color: 'bg-purple-500',
      change: '+8%'
    },
    {
      title: 'Sketches Created',
      value: stats?.total_sketches || 0,
      icon: Image,
      color: 'bg-green-500',
      change: '+24%'
    },
    {
      title: 'Successful Matches',
      value: stats?.sketches_with_matches || 0,
      icon: CheckCircle,
      color: 'bg-orange-500',
      change: '+18%'
    }
  ]

  return (
    <div className="p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">Welcome back, {user?.full_name || user?.username}</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {statCards.map((stat, index) => (
          <div key={index} className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <div className="flex items-center justify-between mb-4">
              <div className={`${stat.color} p-3 rounded-lg`}>
                <stat.icon className="w-6 h-6 text-white" />
              </div>
              <span className="text-sm font-medium text-green-600 flex items-center gap-1">
                <TrendingUp className="w-4 h-4" />
                {stat.change}
              </span>
            </div>
            <h3 className="text-gray-600 text-sm font-medium">{stat.title}</h3>
            <p className="text-3xl font-bold text-gray-900 mt-2">{stat.value}</p>
          </div>
        ))}
      </div>

      {/* Recognition Status */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* System Status */}
        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">System Status</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-green-50 rounded-lg">
              <div className="flex items-center gap-3">
                <CheckCircle className="w-5 h-5 text-green-600" />
                <span className="font-medium text-gray-900">Face Recognition</span>
              </div>
              <span className="text-sm text-green-600 font-medium">Operational</span>
            </div>
            <div className="flex items-center justify-between p-4 bg-green-50 rounded-lg">
              <div className="flex items-center gap-3">
                <CheckCircle className="w-5 h-5 text-green-600" />
                <span className="font-medium text-gray-900">Database</span>
              </div>
              <span className="text-sm text-green-600 font-medium">Connected</span>
            </div>
            <div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg">
              <div className="flex items-center gap-3">
                <Users className="w-5 h-5 text-blue-600" />
                <span className="font-medium text-gray-900">Suspects with Encodings</span>
              </div>
              <span className="text-sm text-blue-600 font-medium">
                {stats?.suspects_with_encodings || 0}
              </span>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
          <div className="grid grid-cols-2 gap-4">
            <button className="p-4 border-2 border-blue-200 hover:border-blue-400 rounded-lg transition group">
              <Image className="w-8 h-8 text-blue-600 mb-2 mx-auto" />
              <p className="text-sm font-medium text-gray-900">New Sketch</p>
            </button>
            <button className="p-4 border-2 border-purple-200 hover:border-purple-400 rounded-lg transition group">
              <Users className="w-8 h-8 text-purple-600 mb-2 mx-auto" />
              <p className="text-sm font-medium text-gray-900">Add Suspect</p>
            </button>
            <button className="p-4 border-2 border-green-200 hover:border-green-400 rounded-lg transition group">
              <FileText className="w-8 h-8 text-green-600 mb-2 mx-auto" />
              <p className="text-sm font-medium text-gray-900">New Case</p>
            </button>
            <button className="p-4 border-2 border-orange-200 hover:border-orange-400 rounded-lg transition group">
              <CheckCircle className="w-8 h-8 text-orange-600 mb-2 mx-auto" />
              <p className="text-sm font-medium text-gray-900">Run Match</p>
            </button>
          </div>
        </div>
      </div>

      {/* Recognition Ready Status */}
      {stats && !stats.recognition_ready && (
        <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
          <div>
            <p className="font-medium text-yellow-900">Recognition System Not Ready</p>
            <p className="text-sm text-yellow-800 mt-1">
              Upload suspect photos to enable face matching capabilities.
            </p>
          </div>
        </div>
      )}
    </div>
  )
}
