import React from 'react'
import { exportCSV, exportExcel } from '../services/api'

function ReceiptTable({ receipts }) {
  const handleExportCSV = async () => {
    try {
      await exportCSV()
    } catch (error) {
      console.error('Export failed:', error)
      alert('Export failed. Please try again.')
    }
  }

  const handleExportExcel = async () => {
    try {
      await exportExcel()
    } catch (error) {
      console.error('Export failed:', error)
      alert('Export failed. Please try again.')
    }
  }

  const getTrustScoreColor = (score) => {
    if (score >= 80) return 'bg-green-100 text-green-800'
    if (score >= 60) return 'bg-yellow-100 text-yellow-800'
    return 'bg-red-100 text-red-800'
  }

  if (receipts.length === 0) {
    return (
      <div className="p-12 text-center">
        <p className="text-gray-500">No receipts yet. Upload your first receipt to get started!</p>
      </div>
    )
  }

  return (
    <div>
      {/* Export Buttons */}
      <div className="px-6 py-3 border-b border-gray-200 flex justify-end space-x-2">
        <button
          onClick={handleExportCSV}
          className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
        >
          Export CSV
        </button>
        <button
          onClick={handleExportExcel}
          className="px-4 py-2 text-sm font-medium text-white bg-primary-600 border border-transparent rounded-md hover:bg-primary-700"
        >
          Export Excel
        </button>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Vendor
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Date
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Total
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Trust Score
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Flags
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Created
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {receipts.map((receipt) => (
              <tr key={receipt.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-gray-900">
                    {receipt.data.vendor_name || 'Unknown'}
                  </div>
                  <div className="text-xs text-gray-500">{receipt.filename}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {receipt.data.transaction_date || '-'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {receipt.data.total_amount
                    ? `${receipt.data.currency || 'KES'} ${receipt.data.total_amount.toLocaleString()}`
                    : '-'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span
                    className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${getTrustScoreColor(
                      receipt.trust_score
                    )}`}
                  >
                    {receipt.trust_score}%
                  </span>
                </td>
                <td className="px-6 py-4">
                  <div className="flex flex-wrap gap-1">
                    {receipt.flags && receipt.flags.length > 0 ? (
                      receipt.flags.slice(0, 2).map((flag, idx) => (
                        <span
                          key={idx}
                          className="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs rounded"
                        >
                          {flag}
                        </span>
                      ))
                    ) : (
                      <span className="text-xs text-gray-400">None</span>
                    )}
                    {receipt.flags && receipt.flags.length > 2 && (
                      <span className="text-xs text-gray-500">
                        +{receipt.flags.length - 2} more
                      </span>
                    )}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {new Date(receipt.created_at).toLocaleDateString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default ReceiptTable
