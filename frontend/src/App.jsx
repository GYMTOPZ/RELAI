import { useState } from 'react'
import { Upload, Sparkles, Video, Mic, Music, Download, Loader2 } from 'lucide-react'
import axios from 'axios'
import './App.css'

function App() {
  const [step, setStep] = useState(1)
  const [userImage, setUserImage] = useState(null)
  const [userImageId, setUserImageId] = useState(null)
  const [prompt, setPrompt] = useState('')
  const [voiceType, setVoiceType] = useState('ai')
  const [voiceFile, setVoiceFile] = useState(null)
  const [voiceFileId, setVoiceFileId] = useState(null)
  const [suggestions, setSuggestions] = useState([])
  const [isGenerating, setIsGenerating] = useState(false)
  const [videoId, setVideoId] = useState(null)
  const [videoStatus, setVideoStatus] = useState(null)
  const [isLoadingSuggestions, setIsLoadingSuggestions] = useState(false)

  // Upload user image
  const handleImageUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    setUserImage(URL.createObjectURL(file))

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await axios.post('/api/upload/image', formData)
      setUserImageId(response.data.file_id)
      setStep(2)
    } catch (error) {
      alert('Error uploading image: ' + error.message)
    }
  }

  // Upload voice sample
  const handleVoiceUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    setVoiceFile(file)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await axios.post('/api/upload/voice', formData)
      setVoiceFileId(response.data.file_id)
    } catch (error) {
      alert('Error uploading voice: ' + error.message)
    }
  }

  // Generate AI suggestions
  const generateSuggestions = async () => {
    setIsLoadingSuggestions(true)
    try {
      const response = await axios.post('/api/suggestions/generate', {
        context: prompt || 'fitness and lifestyle content creator',
        user_preferences: 'engaging social media videos'
      })
      setSuggestions(response.data.suggestions)
    } catch (error) {
      alert('Error generating suggestions: ' + error.message)
    } finally {
      setIsLoadingSuggestions(false)
    }
  }

  // Use a suggestion
  const useSuggestion = (suggestion) => {
    setPrompt(suggestion.description)
    setSuggestions([])
  }

  // Generate video
  const generateVideo = async () => {
    if (!prompt || !userImageId) {
      alert('Please provide a prompt and upload your image')
      return
    }

    setIsGenerating(true)
    setStep(3)

    try {
      const response = await axios.post('/api/video/generate', {
        user_image_id: userImageId,
        prompt: prompt,
        voice_type: voiceType,
        voice_file_id: voiceFileId,
        duration: 30
      })

      setVideoId(response.data.video_id)
      checkVideoStatus(response.data.video_id)
    } catch (error) {
      alert('Error generating video: ' + error.message)
      setIsGenerating(false)
    }
  }

  // Check video status
  const checkVideoStatus = async (id) => {
    const interval = setInterval(async () => {
      try {
        const response = await axios.get(`/api/video/status/${id}`)
        setVideoStatus(response.data)

        if (response.data.status === 'completed') {
          clearInterval(interval)
          setIsGenerating(false)
          setStep(4)
        } else if (response.data.status === 'failed') {
          clearInterval(interval)
          setIsGenerating(false)
          alert('Video generation failed: ' + (response.data.error || 'Unknown error'))
        }
      } catch (error) {
        clearInterval(interval)
        setIsGenerating(false)
        alert('Error checking status: ' + error.message)
      }
    }, 5000)
  }

  // Download video
  const downloadVideo = () => {
    window.open(`/api/video/download/${videoId}`, '_blank')
  }

  // Reset app
  const startOver = () => {
    setStep(1)
    setUserImage(null)
    setUserImageId(null)
    setPrompt('')
    setVoiceType('ai')
    setVoiceFile(null)
    setVoiceFileId(null)
    setSuggestions([])
    setVideoId(null)
    setVideoStatus(null)
  }

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-white mb-4">
            RELAI
          </h1>
          <p className="text-xl text-white/90">
            Relax & let AI create your social media videos
          </p>
        </div>

        {/* Main Card */}
        <div className="bg-white rounded-3xl shadow-2xl p-8">
          {/* Step 1: Upload Image */}
          {step === 1 && (
            <div className="text-center">
              <Upload className="w-16 h-16 mx-auto mb-6 text-primary-600" />
              <h2 className="text-3xl font-bold mb-4">Upload Your Photo</h2>
              <p className="text-gray-600 mb-8">
                This will be the base for all your AI-generated videos
              </p>

              <label className="cursor-pointer inline-block">
                <div className="bg-primary-500 hover:bg-primary-600 text-white font-semibold py-4 px-8 rounded-xl transition-colors">
                  Choose Photo
                </div>
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageUpload}
                  className="hidden"
                />
              </label>

              {userImage && (
                <div className="mt-8">
                  <img
                    src={userImage}
                    alt="Preview"
                    className="max-w-sm mx-auto rounded-xl shadow-lg"
                  />
                </div>
              )}
            </div>
          )}

          {/* Step 2: Create Prompt */}
          {step === 2 && (
            <div>
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-3xl font-bold">Describe Your Video</h2>
                <button
                  onClick={() => setStep(1)}
                  className="text-primary-600 hover:text-primary-700"
                >
                  Change Photo
                </button>
              </div>

              {userImage && (
                <img
                  src={userImage}
                  alt="Your photo"
                  className="w-32 h-32 object-cover rounded-xl mb-6"
                />
              )}

              <div className="mb-6">
                <label className="block text-sm font-semibold mb-2">
                  Video Idea
                </label>
                <textarea
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="Example: Show me doing a chest workout routine at a luxury gym in Miami, 5 exercises, all for chest, wearing athletic gear, with my puppy as my spotter..."
                  className="w-full h-32 px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-primary-500 focus:outline-none resize-none"
                />
              </div>

              <button
                onClick={generateSuggestions}
                disabled={isLoadingSuggestions}
                className="mb-6 flex items-center gap-2 text-primary-600 hover:text-primary-700 font-semibold"
              >
                {isLoadingSuggestions ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Generating ideas...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5" />
                    Get AI Suggestions
                  </>
                )}
              </button>

              {/* Suggestions */}
              {suggestions.length > 0 && (
                <div className="mb-6 space-y-3">
                  <h3 className="font-semibold text-lg">AI Suggestions:</h3>
                  {suggestions.map((suggestion, idx) => (
                    <div
                      key={idx}
                      onClick={() => useSuggestion(suggestion)}
                      className="p-4 border-2 border-gray-200 rounded-xl hover:border-primary-500 cursor-pointer transition-colors"
                    >
                      <h4 className="font-semibold mb-2">{suggestion.title}</h4>
                      <p className="text-sm text-gray-600">{suggestion.description}</p>
                      <div className="flex gap-2 mt-2">
                        {suggestion.hashtags?.slice(0, 3).map((tag, i) => (
                          <span key={i} className="text-xs bg-primary-100 text-primary-700 px-2 py-1 rounded">
                            {tag}
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Voice Options */}
              <div className="mb-6">
                <label className="block text-sm font-semibold mb-2">
                  <Mic className="w-4 h-4 inline mr-2" />
                  Voice Option
                </label>
                <div className="flex gap-4">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="radio"
                      value="ai"
                      checked={voiceType === 'ai'}
                      onChange={(e) => setVoiceType(e.target.value)}
                      className="w-4 h-4"
                    />
                    <span>AI Voice</span>
                  </label>
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="radio"
                      value="custom"
                      checked={voiceType === 'custom'}
                      onChange={(e) => setVoiceType(e.target.value)}
                      className="w-4 h-4"
                    />
                    <span>My Voice</span>
                  </label>
                </div>

                {voiceType === 'custom' && (
                  <div className="mt-4">
                    <label className="cursor-pointer inline-block">
                      <div className="bg-gray-200 hover:bg-gray-300 text-gray-700 font-semibold py-2 px-4 rounded-lg transition-colors">
                        {voiceFile ? voiceFile.name : 'Upload Voice Sample'}
                      </div>
                      <input
                        type="file"
                        accept="audio/*"
                        onChange={handleVoiceUpload}
                        className="hidden"
                      />
                    </label>
                  </div>
                )}
              </div>

              <button
                onClick={generateVideo}
                disabled={!prompt}
                className="w-full bg-gradient-to-r from-primary-500 to-purple-600 hover:from-primary-600 hover:to-purple-700 text-white font-bold py-4 px-8 rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                <Video className="w-5 h-5" />
                Generate Video
              </button>
            </div>
          )}

          {/* Step 3: Generating */}
          {step === 3 && isGenerating && (
            <div className="text-center py-12">
              <Loader2 className="w-16 h-16 mx-auto mb-6 text-primary-600 animate-spin" />
              <h2 className="text-3xl font-bold mb-4">Creating Your Video</h2>
              <p className="text-gray-600 mb-8">
                AI is generating your video with voice and music...
                <br />
                This may take 1-2 minutes
              </p>
              <div className="flex justify-center gap-8 text-sm">
                <div className="flex items-center gap-2">
                  <Video className="w-5 h-5 text-green-500" />
                  <span>Video Generation</span>
                </div>
                <div className="flex items-center gap-2">
                  <Mic className="w-5 h-5 text-green-500" />
                  <span>Voice Synthesis</span>
                </div>
                <div className="flex items-center gap-2">
                  <Music className="w-5 h-5 text-green-500" />
                  <span>Music Creation</span>
                </div>
              </div>
            </div>
          )}

          {/* Step 4: Download */}
          {step === 4 && videoId && (
            <div className="text-center">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <Video className="w-8 h-8 text-green-600" />
              </div>
              <h2 className="text-3xl font-bold mb-4">Your Video is Ready!</h2>
              <p className="text-gray-600 mb-8">
                Your AI-generated video is ready to download and share
              </p>

              <div className="space-y-4">
                <button
                  onClick={downloadVideo}
                  className="w-full bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white font-bold py-4 px-8 rounded-xl transition-all flex items-center justify-center gap-2"
                >
                  <Download className="w-5 h-5" />
                  Download Video
                </button>

                <button
                  onClick={startOver}
                  className="w-full bg-gray-200 hover:bg-gray-300 text-gray-700 font-semibold py-4 px-8 rounded-xl transition-colors"
                >
                  Create Another Video
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-white/80 text-sm">
          <p>Powered by Sora 2, ElevenLabs & Suno AI</p>
        </div>
      </div>
    </div>
  )
}

export default App
