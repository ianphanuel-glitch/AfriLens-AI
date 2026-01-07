/**
 * API service for AfriLens AI frontend.
 * Handles all backend communication.
 */
import axios from 'axios'

// Use environment variable or default to localhost
const API_BASE_URL = import.meta.env.VITE_API_URL || 
  (import.meta.env.MODE === 'production' ? '' : 'http://localhost:8000')

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * Upload a receipt image
 */
export const uploadReceipt = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await api.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  
  return response.data
}

/**
 * Get all receipts
 */
export const getReceipts = async () => {
  const response = await api.get('/receipts')
  return response.data
}

/**
 * Get statistics
 */
export const getStats = async () => {
  const response = await api.get('/stats')
  return response.data
}

/**
 * Export receipts as CSV
 */
export const exportCSV = async () => {
  const response = await api.get('/export/csv', {
    responseType: 'blob',
  })
  
  // Create download link
  const url = window.URL.createObjectURL(new Blob([response.data]))
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', 'afrilens_receipts.csv')
  document.body.appendChild(link)
  link.click()
  link.remove()
}

/**
 * Export receipts as Excel
 */
export const exportExcel = async () => {
  const response = await api.get('/export/excel', {
    responseType: 'blob',
  })
  
  // Create download link
  const url = window.URL.createObjectURL(new Blob([response.data]))
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', 'afrilens_receipts.xlsx')
  document.body.appendChild(link)
  link.click()
  link.remove()
}
