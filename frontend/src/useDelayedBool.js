import { useEffect, useState } from "react"

export default function useDelayedBool(timeout) {
  const [bool, setBool] = useState(false)
  useEffect(() => setTimeout(() => setBool(true), timeout), [])
  return bool
}
