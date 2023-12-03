addEventListener('fetch', (event) => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  // Your logic to handle the request goes here

  const url = new URL(request.url);
  const key = url.searchParams.get('key');
  const value = await whousesittable.get(key);

  // Set CORS headers
  const headers = {
    'Access-Control-Allow-Origin': 'https://enterprisetechstacks.pages.dev',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };

  return new Response(value, {
    status: 200,
    headers: { ...headers, 'Content-Type': 'text/plain' },
  });
}