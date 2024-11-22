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
        <ScrollArea className="h-[400px] w-full rounded-md border p-4">
          {results.map((result, index) => (
            <div key={index} className="flex items-center space-x-2 mb-2">
              <CheckCircle2 className="h-4 w-4 text-green-500 flex-shrink-0" />
              <span className="break-all">{result}</span>
            </div>
          ))}
        </ScrollArea>
      </CardContent>
    </Card>
  )
}

