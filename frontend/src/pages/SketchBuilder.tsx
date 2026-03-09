import { useState, useRef, useEffect } from 'react'
import { fabric } from 'fabric'
import { Save, Upload, Trash2, RotateCw, ZoomIn, ZoomOut, Grid, Layers } from 'lucide-react'
import toast from 'react-hot-toast'

export default function SketchBuilder() {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [canvas, setCanvas] = useState<fabric.Canvas | null>(null)
  const [selectedTool, setSelectedTool] = useState('select')
  const [showGrid, setShowGrid] = useState(true)

  useEffect(() => {
    if (canvasRef.current && !canvas) {
      const fabricCanvas = new fabric.Canvas(canvasRef.current, {
        width: 800,
        height: 1000,
        backgroundColor: '#ffffff',
      })

      setCanvas(fabricCanvas)

      return () => {
        fabricCanvas.dispose()
      }
    }
  }, [])

  const handleSaveSketch = () => {
    if (!canvas) return

    const json = canvas.toJSON()
    const dataUrl = canvas.toDataURL({
      format: 'png',
      quality: 1
    })

    toast.success('Sketch saved!')
    console.log('Canvas data:', json)
  }

  const handleClearCanvas = () => {
    if (!canvas) return
    if (window.confirm('Clear entire canvas?')) {
      canvas.clear()
      canvas.backgroundColor = '#ffffff'
      canvas.renderAll()
      toast.success('Canvas cleared')
    }
  }

  const handleZoomIn = () => {
    if (!canvas) return
    const zoom = canvas.getZoom()
    canvas.setZoom(zoom * 1.1)
  }

  const handleZoomOut = () => {
    if (!canvas) return
    const zoom = canvas.getZoom()
    canvas.setZoom(zoom / 1.1)
  }

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 p-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Sketch Builder</h1>
            <p className="text-sm text-gray-600 mt-1">Create composite face sketches</p>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={handleSaveSketch}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            >
              <Save className="w-4 h-4" />
              Save Sketch
            </button>
          </div>
        </div>
      </div>

      <div className="flex flex-1 overflow-hidden">
        {/* Toolbar */}
        <div className="w-20 bg-white border-r border-gray-200 p-4 flex flex-col gap-4">
          <button
            onClick={handleZoomIn}
            className="p-3 hover:bg-gray-100 rounded-lg transition"
            title="Zoom In"
          >
            <ZoomIn className="w-5 h-5" />
          </button>
          <button
            onClick={handleZoomOut}
            className="p-3 hover:bg-gray-100 rounded-lg transition"
            title="Zoom Out"
          >
            <ZoomOut className="w-5 h-5" />
          </button>
          <button
            onClick={() => setShowGrid(!showGrid)}
            className={`p-3 rounded-lg transition ${showGrid ? 'bg-blue-100' : 'hover:bg-gray-100'}`}
            title="Toggle Grid"
          >
            <Grid className="w-5 h-5" />
          </button>
          <button
            className="p-3 hover:bg-gray-100 rounded-lg transition"
            title="Layers"
          >
            <Layers className="w-5 h-5" />
          </button>
          <div className="flex-1" />
          <button
            onClick={handleClearCanvas}
            className="p-3 hover:bg-red-100 text-red-600 rounded-lg transition"
            title="Clear Canvas"
          >
            <Trash2 className="w-5 h-5" />
          </button>
        </div>

        {/* Canvas Area */}
        <div className="flex-1 overflow-auto p-8">
          <div className="inline-block bg-white shadow-lg">
            <canvas ref={canvasRef} className="border-2 border-gray-300" />
          </div>
        </div>

        {/* Elements Panel */}
        <div className="w-80 bg-white border-l border-gray-200 p-4 overflow-y-auto">
          <h3 className="font-semibold text-gray-900 mb-4">Facial Elements</h3>
          
          <div className="space-y-4">
            {['Eyes', 'Nose', 'Mouth', 'Eyebrows', 'Hair', 'Face Shape', 'Accessories'].map((category) => (
              <div key={category} className="border border-gray-200 rounded-lg p-3">
                <h4 className="font-medium text-gray-900 mb-2">{category}</h4>
                <div className="grid grid-cols-3 gap-2">
                  {[1, 2, 3, 4, 5, 6].map((item) => (
                    <div
                      key={item}
                      className="aspect-square bg-gray-100 rounded border border-gray-200 hover:border-blue-500 cursor-pointer transition"
                    />
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
