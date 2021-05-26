import { createTheme, responsiveFontSizes } from "@material-ui/core/styles"

let theme = createTheme({
  typography: {
    fontFamily: "Open Sans",
  },
})

theme = responsiveFontSizes(theme)

export default theme
