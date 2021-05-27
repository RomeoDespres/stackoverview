import { fetchTagReputation } from "../src/api"
import Home from "../src/Home"

export default function Page(props) {
  return <Home {...props} />
}

export async function getServerSideProps(context) {
  return {
    props: { tags: await fetchTagReputation() },
  }
}
