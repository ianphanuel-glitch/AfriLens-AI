import React, { useState, useEffect } from 'react'
import UploadCard from '../components/UploadCard'
import ReceiptTable from '../components/ReceiptTable'
import InsightBanner from '../components/InsightBanner'
import StatsCard from '../components/StatsCard'
import { getReceipts, getStats } from '../services/api'

function Dashboard() {
  const [receipts, setReceipts] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)

  const fetchData = async () => {
    try {
      setRefreshing(true)
      const [receiptsData, statsData] = await Promise.all([
        getReceipts(),
        getStats()
      ])
      
      setReceipts(receiptsData.data || [])
      setStats(statsData.data || null)
    } catch (error) {
      console.error('Failed to fetch data:', error)
    } finally {
      setLoading(false)
      setRefreshing(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  const handleUploadSuccess = () => {
    // Refresh data after successful upload
    fetchData()
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading AfriLens AI...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">AfriLens AI</h1>
              <p className="text-sm text-gray-500">Vision Intelligence for African SMEs</p>
            </div>
            <div className="flex items-center space-x-4">
              {stats && (
                <div className="text-right">
                  <p className="text-xs text-gray-500">Total Receipts</p>
                  <p className="text-lg font-semibold text-gray-900">{stats.total_receipts}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Insight Banner */}
        {stats && <InsightBanner stats={stats} />}

        {/* Stats Cards */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <StatsCard
              title="Total Spent"
              value={`${stats.currency} ${stats.total_spent.toLocaleString()}`}
              subtitle="All time"
            />
            <StatsCard
              title="Average Trust Score"
              value={`${stats.average_trust_score}%`}
              subtitle="Receipt quality"
            />
            <StatsCard
              title="Today's Receipts"
              value={stats.receipts_today}
              subtitle="Uploaded today"
            />
          </div>
        )}

        {/* Upload Card */}
        <div className="mb-8">
          <UploadCard onUploadSuccess={handleUploadSuccess} />
        </div>

        {/* Receipts Table */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900">Receipts</h2>
            <button
              onClick={fetchData}
              disabled={refreshing}
              className="text-sm text-primary-600 hover:text-primary-700 disabled:opacity-50"
            >
              {refreshing ? 'Refreshing...' : 'Refresh'}
            </button>
          </div>
          <ReceiptTable receipts={receipts} />
        </div>
      </main>
    </div>
  )
}

export default Dashboard
