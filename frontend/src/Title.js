import { useEffect, useState } from "react"

import Fade from "@material-ui/core/Fade"
import { makeStyles } from "@material-ui/core/styles"
import Typography from "@material-ui/core/Typography"

const useStyles = makeStyles((theme) => ({
  title: {
    [theme.breakpoints.down("sm")]: {
      marginBottom: theme.spacing(2),
    },
  },
  subtitle: { marginLeft: "0.25rem" },
}))

export default function Title({ title, subtitle }) {
  const [showSubtitle, setShowSubtitle] = useState(false)

  const classes = useStyles()

  useEffect(() => {
    setTimeout(() => setShowSubtitle(true), 500)
  }, [])

  return (
    <>
      <Fade in={true} timeout={750}>
        <Typography variant="h1" className={classes.title}>
          {title}
        </Typography>
      </Fade>
      <Fade in={showSubtitle} timeout={750}>
        <Typography variant="subtitle1" className={classes.subtitle}>
          {subtitle}
        </Typography>
      </Fade>
    </>
  )
}
