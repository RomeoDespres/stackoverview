import { createTheme, responsiveFontSizes } from "@material-ui/core/styles"

const theme = responsiveFontSizes(
  createTheme({
    typography: {
      fontFamily: "Open Sans",
    },
    palette: {
      background: {
        default: "#f8f8f8",
      },
    },
  })
)

export default theme
