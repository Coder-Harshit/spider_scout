import { Card, CardContent } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { CheckCircle2 } from 'lucide-react'

interface CrawlResultsProps {
  results: string[]
}

export function CrawlResults({ results }: CrawlResultsProps) {
  return (
    <Card>
      <CardContent className="p-6">
        <ScrollArea className="h-[400px] w-full rounded-lg border p-4">
          {results.length === 0 ? (
            <div className="flex items-center justify-center h-full text-muted-foreground">
              No results yet. Start a crawl to see URLs here.
            </div>
          ) : (
            results.map((result, index) => (
              <div
                key={index}
                className="flex items-center space-x-2 mb-2 p-2 rounded hover:bg-accent/5"
              >
                <CheckCircle2 className="h-4 w-4 text-green-500 flex-shrink-0" />
                <a
                  href={result}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="break-all hover:underline"
                >
                  {result}
                </a>
              </div>
            ))
          )}
        </ScrollArea>
      </CardContent>
    </Card>
  )
}
