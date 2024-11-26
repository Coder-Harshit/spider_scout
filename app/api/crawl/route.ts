import { NextRequest, NextResponse } from 'next/server';
import { spawn } from 'child_process';

export const runtime = 'nodejs';

export async function POST(req: NextRequest) {
  const { url, depth, respectRobotsTxt } = await req.json();
  console.log('Request received:', { url, depth, respectRobotsTxt });
  if (!url || typeof depth !== 'number') {
    return NextResponse.json({ error: 'Invalid parameters' }, { status: 400 });
  }

  const pythonProcess = spawn('python', [
    '-u',
    'main.py',
    url,
    depth.toString(),
    respectRobotsTxt ? '1' : '0',
  ]);

  const encoder = new TextEncoder();
  const stream = new ReadableStream({
    start(controller) {
      let isControllerClosed = false;

      const closeController = () => {
        if (!isControllerClosed) {
          isControllerClosed = true;
          controller.close();
        }
      };

      // Handle stdout
      pythonProcess.stdout.on('data', (data) => {
        const decodedData = data.toString();
        if (!isControllerClosed) {
          try {
            const json = JSON.parse(decodedData.trim());

            // Handle specific types of responses
            if (json.type === 'completion') {
              console.log(json.message);
            } else if (json.type === 'error') {
              console.error(json.message);
            } else {
              controller.enqueue(encoder.encode(`${decodedData}\n`));
            }
          } catch (error) {
            // Handle non-JSON output
            controller.enqueue(encoder.encode(`Non-JSON Output: ${decodedData}\n`));
          }
        }
      });

      // Handle stderr
      pythonProcess.stderr.on('data', (data) => {
        const errorData = data.toString();
        console.error(`Python Error: ${errorData}`);
        if (!isControllerClosed) {
          controller.enqueue(
            encoder.encode(
              JSON.stringify({ type: 'error', message: errorData }) + '\n'
            )
          );
        }
      });

      // Handle process close
      pythonProcess.on('close', (code) => {
        console.log(`Python process exited with code ${code}`);
        closeController();
      });

      // Handle process errors
      pythonProcess.on('error', (err) => {
        console.error(`Python process error: ${err.message}`);
        if (!isControllerClosed) {
          controller.error(err);
        }
        closeController();
      });
    },
  });

  return new NextResponse(stream);
}
