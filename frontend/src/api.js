function getApiUrl(path) {
  const root = "https://1be4sw89wi.execute-api.eu-west-3.amazonaws.com/"
  return root + path
}

export async function fetchTagReputation() {
  const response = await fetch(getApiUrl("tags/reputation"))
  const body = await response.json()
  return body
}
