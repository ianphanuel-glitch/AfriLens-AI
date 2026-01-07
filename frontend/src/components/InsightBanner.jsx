import React from 'react'

function InsightBanner({ stats }) {
  if (!stats) return null

  // Calculate today's spending
  const todaySpending = stats.receipts_today > 0
    ? `You've processed ${stats.receipts_today} receipt${stats.receipts_today > 1 ? 's' : ''} today.`
    : 'No receipts processed today.'

  // Top vendor insight
  const topVendor = stats.top_vendors && stats.top_vendors.length > 0
    ? stats.top_vendors[0]
    : null

  const insight = topVendor
    ? `You've spent ${stats.currency} ${topVendor.total_spent.toLocaleString()} at ${topVendor.name} across ${topVendor.receipt_count} receipt${topVendor.receipt_count > 1 ? 's' : ''}.`
    : todaySpending

  return (
    <div className="mb-6 bg-gradient-to-r from-primary-500 to-primary-600 rounded-lg shadow-lg p-6 text-white">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold mb-1">💡 AI Insight</h3>
          <p className="text-primary-50">{insight}</p>
        </div>
        <div className="hidden md:block">
          <div className="text-right">
            <p className="text-2xl font-bold">{stats.total_receipts}</p>
            <p className="text-sm text-primary-100">Total Receipts</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default InsightBanner
