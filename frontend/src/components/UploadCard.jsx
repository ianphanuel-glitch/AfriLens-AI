import React, { useState, useRef } from 'react'
import { uploadReceipt } from '../services/api'

function UploadCard({ onUploadSuccess }) {
  const [dragging, setDragging] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const fileInputRef = useRef(null)

  const handleDragOver = (e) => {
    e.preventDefault()
    setDragging(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setDragging(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragging(false)
    
    const files = e.dataTransfer.files
    if (files.length > 0) {
      handleFile(files[0])
    }
  }

  const handleFileSelect = (e) => {
    const files = e.target.files
    if (files.length > 0) {
      handleFile(files[0])
    }
  }

  const handleFile = async (file) => {
    // Validate file type
    if (!file.type.startsWith('image/')) {
      setError('Please upload an image file')
      return
    }

    setUploading(true)
    setError(null)
    setResult(null)

    try {
      const response = await uploadReceipt(file)
      setResult(response)
      if (onUploadSuccess) {
        onUploadSuccess()
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed. Please try again.')
    } finally {
      setUploading(false)
    }
  }

  const getTrustScoreColor = (score) => {
    if (score >= 80) return 'bg-green-100 text-green-800'
    if (score >= 60) return 'bg-yellow-100 text-yellow-800'
    return 'bg-red-100 text-red-800'
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Upload Receipt</h2>
      
      {/* Upload Area */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
          dragging
            ? 'border-primary-500 bg-primary-50'
            : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
        } ${uploading ? 'opacity-50 cursor-not-allowed' : ''}`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleFileSelect}
          className="hidden"
          disabled={uploading}
        />
        
        {uploading ? (
          <div>
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
            <p className="text-gray-600 font-medium">AI Thinking...</p>
            <p className="text-sm text-gray-500 mt-2">Processing your receipt</p>
          </div>
        ) : (
          <div>
            <svg
              className="mx-auto h-12 w-12 text-gray-400"
              stroke="currentColor"
              fill="none"
              viewBox="0 0 48 48"
            >
              <path
                d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                strokeWidth={2}
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            <p className="mt-4 text-sm text-gray-600">
              <span className="font-semibold">Click to upload</span> or drag and drop
            </p>
            <p className="text-xs text-gray-500 mt-1">PNG, JPG, GIF up to 10MB</p>
          </div>
        )}
      </div>

      {/* Error Message */}
      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      {/* Result */}
      {result && (
        <div className="mt-4 p-4 bg-gray-50 rounded-lg">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-semibold text-gray-900">Extraction Results</h3>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${getTrustScoreColor(result.trust_score)}`}>
              Trust Score: {result.trust_score}%
            </span>
          </div>
          
          <div className="space-y-2 text-sm">
            {result.data.vendor_name && (
              <div>
                <span className="text-gray-600">Vendor:</span>{' '}
                <span className="font-medium text-gray-900">{result.data.vendor_name}</span>
              </div>
            )}
            {result.data.transaction_date && (
              <div>
                <span className="text-gray-600">Date:</span>{' '}
                <span className="font-medium text-gray-900">{result.data.transaction_date}</span>
              </div>
            )}
            {result.data.total_amount && (
              <div>
                <span className="text-gray-600">Total:</span>{' '}
                <span className="font-medium text-gray-900">
                  {result.data.currency} {result.data.total_amount.toLocaleString()}
                </span>
              </div>
            )}
          </div>

          {result.flags && result.flags.length > 0 && (
            <div className="mt-3 pt-3 border-t border-gray-200">
              <p className="text-xs text-gray-600 mb-1">Flags:</p>
              <div className="flex flex-wrap gap-1">
                {result.flags.map((flag, idx) => (
                  <span
                    key={idx}
                    className="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs rounded"
                  >
                    {flag}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default UploadCard
