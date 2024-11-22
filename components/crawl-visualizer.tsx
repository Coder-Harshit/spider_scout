import { useEffect, useRef } from 'react'
import { Card, CardContent } from "@/components/ui/card"
import ForceGraph2D from 'react-force-graph-2d'

interface CrawlVisualizerProps {
  results: string[]
}

export function CrawlVisualizer({ results }: CrawlVisualizerProps) {
  const graphRef = useRef<any>(null)

  useEffect(() => {
    if (graphRef.current) {
      graphRef.current.d3Force('charge').strength(-100)
      graphRef.current.d3Force('link').distance(50)
    }
  }, [])

  const graphData = {
    nodes: results.map((url, index) => ({ id: url, group: index % 5 })),
    links: results.slice(1).map((url, index) => ({
      source: results[0],
      target: url,
    })),
  }

  return (
    <Card>
      <CardContent className="p-6">
        <div className="h-[400px] w-full">
          <ForceGraph2D
            ref={graphRef}
            graphData={graphData}
            nodeAutoColorBy="group"
            nodeLabel="id"
            linkDirectionalParticles={2}
          />
        </div>
      </CardContent>
    </Card>
  )
}

