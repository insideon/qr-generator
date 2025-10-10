import { useState } from 'react'
import axios from 'axios'

function App() {
  const [formData, setFormData] = useState({
    store_name: '',
    ssid: '',
    security: 'WPA',
    password: ''
  })

  const [qrImage, setQrImage] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setSuccess(false)
    setQrImage(null)

    try {
      const response = await axios.post('/api/generate-qr', formData)
      setQrImage(`data:image/png;base64,${response.data.image_base64}`)
      setSuccess(true)
    } catch (err) {
      const errorDetail = err.response?.data?.detail
      if (errorDetail) {
        setError(errorDetail)
      } else if (err.code === 'ERR_NETWORK') {
        setError('서버에 연결할 수 없습니다. 백엔드 서버가 실행 중인지 확인해주세요.')
      } else {
        setError('QR 코드 생성 중 오류가 발생했습니다. 다시 시도해주세요.')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleDownload = () => {
    const link = document.createElement('a')
    link.href = qrImage
    link.download = `${formData.store_name}_wifi_qr.png`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return (
    <div className="app-container">
      <div className="header">
        <h1>Wi-Fi QR 생성기</h1>
        <p>매장의 Wi-Fi 접속용 QR 코드를 쉽게 생성하세요</p>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="store_name">매장명</label>
          <input
            type="text"
            id="store_name"
            name="store_name"
            value={formData.store_name}
            onChange={handleChange}
            required
            placeholder="예: 스타벅스 강남점"
          />
        </div>

        <div className="form-group">
          <label htmlFor="ssid">Wi-Fi 이름 (SSID)</label>
          <input
            type="text"
            id="ssid"
            name="ssid"
            value={formData.ssid}
            onChange={handleChange}
            required
            placeholder="예: StarbucksWiFi"
          />
        </div>

        <div className="form-group">
          <label htmlFor="security">보안 타입</label>
          <select
            id="security"
            name="security"
            value={formData.security}
            onChange={handleChange}
            required
          >
            <option value="WPA">WPA/WPA2</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="password">Wi-Fi 비밀번호</label>
          <input
            type="text"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            placeholder="비밀번호를 입력하세요"
          />
        </div>

        <button
          type="submit"
          className="btn-generate"
          disabled={loading}
        >
          {loading ? (
            <div className="loading">
              <div className="spinner"></div>
              생성 중...
            </div>
          ) : (
            'QR 코드 생성'
          )}
        </button>
      </form>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {qrImage && (
        <div className="result-container">
          {success && (
            <div className="success-message">
              ✅ QR 코드가 성공적으로 생성되었습니다!<br/>
              📁 Google Drive에 저장되었습니다.
            </div>
          )}

          <div className="qr-preview">
            <h3>QR 코드 미리보기</h3>
            <img src={qrImage} alt="Wi-Fi QR Code" />
          </div>

          <button
            type="button"
            className="btn-download"
            onClick={handleDownload}
          >
            다운로드
          </button>
        </div>
      )}
    </div>
  )
}

export default App


