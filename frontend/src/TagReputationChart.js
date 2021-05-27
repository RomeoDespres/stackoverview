import Card from "@material-ui/core/Card"
import CardContent from "@material-ui/core/CardContent"
import CardHeader from "@material-ui/core/CardHeader"
import Fade from "@material-ui/core/Fade"
import Grid from "@material-ui/core/Grid"
import { makeStyles } from "@material-ui/core/styles"

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts"

const useStyles = makeStyles((theme) => ({
  root: { marginTop: theme.spacing(6) },
}))

export default function TagReputationChart({ tags, show }) {
  const classes = useStyles()

  return (
    <Fade in={show} timeout={1000}>
      <Grid xs={12} className={classes.root}>
        <Card>
          <CardHeader title="Answer reputation by tag" />
          <CardContent>
            <ResponsiveContainer height={700}>
              <BarChart layout="vertical" data={tags}>
                <XAxis hide type="number" />
                <YAxis hide dataKey="tag" type="category" />
                <Bar
                  dataKey="reputation"
                  fill="#f48024"
                  radius={[0, 15, 15, 0]}
                  isAnimationActive={false}
                  label={<Label tags={tags} />}
                  barSize={100}
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
  console.log(other)
  y += 20
  const fontSize = 14
  return (
    <>
      <text x={x + 4} y={y} fontSize={fontSize}>
        {tags[index].tag}
      </text>
      <text x={x + width - 40} y={y} fontSize={fontSize}>
        {value.toFixed(1)}
      </text>
    </>
  )
}
