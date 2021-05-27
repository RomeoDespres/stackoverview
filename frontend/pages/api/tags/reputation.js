import { fetchTagReputation } from "../../../src/api"

export default async function handler(req, res) {
  const tags = await fetchTagReputation()
  res.status(200).json({ tags })
}
