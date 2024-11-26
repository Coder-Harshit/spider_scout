import { useEffect, useRef, useMemo } from 'react'
import { Card, CardContent } from "@/components/ui/card"
import ForceGraph2D from 'react-force-graph-2d'
import { useTheme } from 'next-themes'

interface CrawlVisualizerProps {
  results: string[]
}

export function CrawlVisualizer({ results }: CrawlVisualizerProps) {
  const graphRef = useRef<any>(null);
  const { theme } = useTheme();  // Get the current theme (light or dark)

  useEffect(() => {
    if (graphRef.current) {
      graphRef.current.d3Force('charge').strength(-100)
      graphRef.current.d3Force('link').distance(50)
      graphRef.current.d3Force('center').strength(0.5)
    }
  }, [])

  const graphData = useMemo(() => {
    const nodes = results.map(url => ({ id: url }))
    const links = results.slice(1).map(url => ({
      source: results[0],
      target: url,
    }))
    return { nodes, links }
  }, [results])

  return (
    <Card>
      <CardContent className="p-6">
        <div className="h-[400px] w-full rounded-lg border">
          <ForceGraph2D
            ref={graphRef}
            graphData={graphData}
            nodeAutoColorBy="id"
            linkDirectionalArrowLength={6}
            linkDirectionalArrowRelPos={1}
            nodeLabel="id"
            nodeRelSize={6}
            linkDirectionalParticles={2}
            linkDirectionalParticleSpeed={0.005}
            backgroundColor={theme === 'light' ? '#ffffff' : '#333333'}  // Set background based on theme
            linkColor={() => "#999"}
            onNodeHover={(node) => {
              if (node) console.log('Hovered node:', node);
            }}
            onNodeClick={(node) => {
              if (node) console.log('Clicked node:', node);
            }}
          />
        </div>
      </CardContent>
    </Card>
  )
}