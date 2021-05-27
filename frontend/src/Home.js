import { makeStyles } from "@material-ui/core/styles"

import TagReputationChart from "./TagReputationChart"
import Title from "./Title"
import useDelayedBool from "./useDelayedBool"

const useStyles = makeStyles((theme) => ({
  root: { margin: theme.spacing(4) },
}))

export default function Home({ tags }) {
  const showTitle = useDelayedBool(0)
  const showSubtitle = useDelayedBool(250)
  const showCharts = useDelayedBool(1000)

  const classes = useStyles()

  const title = "Stack\u200BOverview"
  const subtitle = "Real-time insights to beat the rep game on StackOverflow."

  return (
    <div className={classes.root}>
      <Title
        title={title}
        subtitle={subtitle}
        showTitle={showTitle}
        showSubtitle={showSubtitle}
      />
      <TagReputationChart tags={tags} show={showCharts} />
    </div>
  )
}
