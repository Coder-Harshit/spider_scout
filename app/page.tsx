'use client'
import { useState, useEffect, useRef } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Slider } from "@/components/ui/slider"
import { Switch } from "@/components/ui/switch"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { ScrollArea } from "@/components/ui/scroll-area"
import { AlertCircle, CheckCircle2, Moon, Sun, Loader2 } from 'lucide-react'
import { CrawlResults } from '@/components/crawl-results'
import { CrawlVisualizer } from '@/components/crawl-visualizer'

export default function WebCrawler() {
  const [darkMode, setDarkMode] = useState(false)
  const [url, setUrl] = useState('')
  const [depth, setDepth] = useState(1)
  const [respectRobotsTxt, setRespectRobotsTxt] = useState(true)
  const [crawling, setCrawling] = useState(false)
  const [progress, setProgress] = useState(0)
  const [results, setResults] = useState<string[]>([])
  const [graphData, setGraphData] = useState<{ url: string; links: string[] }[]>([])
  const [error, setError] = useState('')
  const [isError, setIsError] = useState(false)  // New state for error display

  const toggleDarkMode = () => {
    setDarkMode(!darkMode)
    document.documentElement.classList.toggle('dark')
  }

  const startCrawl = async () => {
    if (!url) {
      setError('Please enter a valid URL')
      setIsError(true)  // Display the error
      return
    }
    setError('')
    setIsError(false)
    setCrawling(true)
    setProgress(0)
    setResults([])

    try {
      const response = await fetch('/api/crawl', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url, depth, respectRobotsTxt }),
      })

      if (!response.ok) {
        throw new Error('Crawl request failed')
      }

      const reader = response.body?.getReader()
      if (!reader) {
        throw new Error('Unable to read response')
      }

      // while (true) {
      //   const { done, value } = await reader.read()
      //   if (done) break

      //   const chunk = new TextDecoder().decode(value)
      //   const lines = chunk.split('\n').filter(Boolean)

      //   lines.forEach(line => {
      //     const data = JSON.parse(line)
      //     if (data.type === 'progress') {
      //       setProgress(data.value)
      //     } else if (data.type === 'result') {
      //       setResults(prev => [...prev, data.url])
      //     }
      //   })
      let buffer = ''
      let completeGraphData = []

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = new TextDecoder().decode(value)
        buffer += chunk

        let lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.trim() === '') {
            // Skip empty lines
            continue
          }
          try {
            const data = JSON.parse(line)
            if (data.type === 'progress') {
              setProgress(data.value)
            } else if (data.type === 'result') {
              setResults(prev => [...prev, data.url])
            } else if (data.type === 'graph') {
              completeGraphData = data.data
            } else if (data.type === 'error') {
              setError(data.message)
            }
          } catch (e) {
            console.error('Error parsing line:', line)
          }
        }
      }
      setGraphData(completeGraphData)
      setCrawling(false)
    } catch (error) {
      setError('An error occurred during crawling')
      setIsError(true)  // Display the error
    } finally {
      setCrawling(false)
    }
  }

  useEffect(() => {
    if (isError) {
      // Simulate a timeout to clear the error after a few seconds
      const timeoutId = setTimeout(() => {
        setError('')
        setIsError(false)
      }, 5000);

      // Clear the timeout if the component unmounts
      return () => {
        clearTimeout(timeoutId);
      };
    }
  }, [isError]);
  
  return (
    <div className={`min-h-screen p-8 transition-colors duration-300 ${darkMode ? 'dark bg-gray-900 text-white' : 'bg-gray-100 text-gray-900'}`}>
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">Spider Scout Web Crawler</h1>
          <Button variant="ghost" size="icon" onClick={toggleDarkMode}>
            {darkMode ? <Sun className="h-6 w-6" /> : <Moon className="h-6 w-6" />}
            <span className="sr-only">Toggle dark mode</span>
          </Button>
        </div>

        <Card className="mb-8">
          <CardContent className="p-6">
            <div className="flex space-x-4 mb-4">
              <Input
                type="url"
                placeholder="Enter starting URL"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                className="flex-grow"
                aria-label="Starting URL"
              />
              <Button onClick={startCrawl} disabled={crawling}>
                {crawling ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Crawling...
                  </>
                ) : (
                  'Start Crawl'
                )}
              </Button>
            </div>

            <div className="flex items-center space-x-4 mb-4">
              <label className="flex items-center space-x-2">
                <span>Crawl Depth:</span>
                <Slider
                  min={1}
                  max={10}
                  step={1}
                  value={[depth]}
                  onValueChange={(value) => setDepth(value[0])}
                  className="w-32"
                  aria-label="Crawl depth"
                />
                <span>{depth}</span>
              </label>
              <label className="flex items-center space-x-2">
                <span>Respect robots.txt:</span>
                <Switch
                  checked={respectRobotsTxt}
                  onCheckedChange={setRespectRobotsTxt}
                  aria-label="Respect robots.txt"
                />
              </label>
            </div>

            {isError && (  // Display the error message
              <div className="flex items-center space-x-2 text-red-500 mb-4" role="alert">
                <AlertCircle className="h-4 w-4" />
                <span>{error}</span>
              </div>
            )}

            {crawling && (
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span>Crawl Progress:</span>
                  <span>{progress}%</span>
                </div>
                <Progress value={progress} className="w-full" aria-label="Crawl progress" />
              </div>
            )}
          </CardContent>
        </Card>

        <Tabs defaultValue="results" className="mb-8">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="results">Results</TabsTrigger>
            <TabsTrigger value="visualizer">Visualizer</TabsTrigger>
          </TabsList>
          <TabsContent value="results">
            <CrawlResults results={results} />
          </TabsContent>
          <TabsContent value="visualizer">
            <CrawlVisualizer results={results} />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}