import { NextRequest, NextResponse } from 'next/server'
import { spawn } from 'child_process'

export async function POST(req: NextRequest) {
  const { url, depth, respectRobotsTxt } = await req.json()

  const pythonProcess = spawn('python', [
    '-u',
    'main.py',
    url,
    depth.toString(),
    respectRobotsTxt ? '1' : '0'
  ])

  const encoder = new TextEncoder()

  const stream = new ReadableStream({
    start(controller) {
      pythonProcess.stdout.on('data', (data) => {
        controller.enqueue(encoder.encode(`${data}\n`))
      })

      pythonProcess.stderr.on('data', (data) => {
        console.error(`Python Error: ${data}`)
        controller.enqueue(encoder.encode(JSON.stringify({ type: 'error', message: data.toString() }) + '\n'))
      })

      pythonProcess.on('close', (code) => {
        console.log(`Python process exited with code ${code}`)
        controller.close()
      })
    },
  })

  return new NextResponse(stream)
}

