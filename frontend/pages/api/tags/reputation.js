import { fetchTagReputation } from "../../../src/api"

export default async function handler(req, res) {
  res.status(200).json(await fetchTagReputation())
}
