import type { Config, Context } from '@netlify/functions'

export default async (req: Request, context: Context) => {
  const op = context.params.operation

  let data: { a?: unknown; b?: unknown }
  try {
    data = await req.json()
  } catch {
    return Response.json({ error: 'Request body must be valid JSON.' }, { status: 400 })
  }

  const missing = ['a', 'b'].filter((f) => !(f in data))
  if (missing.length) {
    return Response.json(
      { error: `Missing required field(s): ${missing.join(', ')}.` },
      { status: 400 },
    )
  }

  const { a, b } = data
  if (typeof a !== 'number' || typeof b !== 'number') {
    return Response.json({ error: "Fields 'a' and 'b' must be numbers." }, { status: 422 })
  }

  switch (op) {
    case 'add':
      return Response.json({ result: a + b })
    case 'subtract':
      return Response.json({ result: a - b })
    case 'multiply':
      return Response.json({ result: a * b })
    case 'divide':
      if (b === 0) {
        return Response.json({ error: 'Division by zero is not allowed.' }, { status: 400 })
      }
      return Response.json({ result: a / b })
    default:
      return Response.json({ error: `Unknown operation: ${op}` }, { status: 404 })
  }
}

export const config: Config = {
  path: '/api/:operation',
  method: 'POST',
}
