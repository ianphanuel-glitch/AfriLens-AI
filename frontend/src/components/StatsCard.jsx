import React from 'react'

function StatsCard({ title, value, subtitle }) {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <p className="text-sm font-medium text-gray-500 mb-1">{title}</p>
      <p className="text-2xl font-bold text-gray-900 mb-1">{value}</p>
      {subtitle && (
        <p className="text-xs text-gray-400">{subtitle}</p>
      )}
    </div>
  )
}

export default StatsCard
