import { Typography } from "@material-ui/core"
import Card from "@material-ui/core/Card"
import CardContent from "@material-ui/core/CardContent"
import CardHeader from "@material-ui/core/CardHeader"
import Fade from "@material-ui/core/Fade"
import Grid from "@material-ui/core/Grid"
import { makeStyles, useTheme } from "@material-ui/core/styles"

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Rectangle,
  ReferenceLine,
  ResponsiveContainer,
} from "recharts"

const useStyles = makeStyles((theme) => ({
  root: { marginTop: theme.spacing(6), fontFamily: "Roboto" },
  chart: {
    "&& svg": { overflow: "visible", fontSize: 16 },
  },
}))

export default function TagReputationChart({ avgReputation, tags, show }) {
  const classes = useStyles()
  const theme = useTheme()

  return (
    <Fade in={show} timeout={1000}>
      <Grid xs={12} className={classes.root}>
        <Card style={{ borderRadius: "16px" }}>
          <CardHeader
            title={
              <Typography fontWeight="bold">
                Answer reputation by tag
              </Typography>
            }
          />
          <CardContent>
            <ResponsiveContainer height={700} className={classes.chart}>
              <BarChart layout="vertical" data={tags}>
                <XAxis hide type="number" />
                <YAxis hide dataKey="tag" type="category" />
                <Bar
                  dataKey="reputation"
                  fill="#f48024"
                  radius={[5, 15, 15, 5]}
                  isAnimationActive={false}
                  label={<Label tags={tags} />}
                  barSize={100}
                />
                <ReferenceLine
                  x={avgReputation}
                  stroke={theme.palette.background.paper}
                  strokeDasharray={[6, 3]}
                  label={<ReferenceLabel />}
                />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </Grid>
    </Fade>
  )
}

function Label({ x, y, tags, index, width, offset, value, ...other }) {
  const theme = useTheme()
  const fill = theme.palette.background.paper
  y += 20
  return (
    <>
      <text x={x + 8} y={y} fill={fill}>
        {tags[index].tag}
      </text>
      <text x={x + width - 40} y={y} fill={fill}>
        {value.toFixed(1)}
      </text>
    </>
  )
}

function ReferenceLabel(props) {
  const { x, offset } = props
  return (
    <text x={props.viewBox.x} y={-5} textAnchor="middle">
      Average
    </text>
  )
}
