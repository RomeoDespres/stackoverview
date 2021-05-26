import { useEffect, useState } from "react"

import Fade from "@material-ui/core/Fade"
import Typography from "@material-ui/core/Typography"
import { makeStyles } from "@material-ui/core/styles"

import Title from "../src/Title"

const useStyles = makeStyles((theme) => ({
  root: { margin: theme.spacing(4) },
}))

export default function Home() {
  const classes = useStyles()

  const title = "Stack\u200BOverview"
  const subtitle = "Real-time insights to beat the rep game on StackOverflow."

  return (
    <div className={classes.root}>
      <Title title={title} subtitle={subtitle} />
    </div>
  )
}
