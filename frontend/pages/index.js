import { useEffect, useState } from "react"

import Fade from "@material-ui/core/Fade"
import Typography from "@material-ui/core/Typography"
import { makeStyles } from "@material-ui/core/styles"

const useStyles = makeStyles((theme) => ({
  root: { margin: theme.spacing(4) },
  title: {
    [theme.breakpoints.down("sm")]: {
      marginBottom: theme.spacing(2),
    },
  },
}))

export default function Home() {
  const classes = useStyles()
  const [showSubtitle, setShowSubtitle] = useState(false)

  const title = "Stack\u200BOverview"
  const subtitle =
    "Real-time insights to beat the rep game on StackOverflow. Coming soon."

  useEffect(() => {
    setTimeout(() => setShowSubtitle(true), 500)
  }, [])

  return (
    <div className={classes.root}>
      <Fade in={true} timeout={750}>
        <Typography variant="h1" className={classes.title}>
          {title}
        </Typography>
      </Fade>
      <Fade in={showSubtitle} timeout={750}>
        <Typography variant="subtitle1">{subtitle}</Typography>
      </Fade>
    </div>
  )
}
