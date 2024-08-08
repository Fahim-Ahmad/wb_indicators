source("global.R")

ui <- dashboardPage(
  dashboardHeader(disable = T),
  dashboardSidebar(disable = T),
  dashboardBody(
    tags$head(tags$style(HTML("
      .disabled {
        pointer-events: none;
        opacity: 0.5;
      }
      
      .box {
        max-height: 50vh;
        overflow-y: auto;
      }
      
      .box .box-title {
        font-size: 18px;
        color: gray
      }
      
      .value {
        font-size: 20px;
        # font-weight: bold;
      }
      
      .no-data {
        color: maroon;
      }
      
    "))),
    fluidRow(
      column(4, offset = 3,
             selectInput("countries", label = NULL, choices = countries, selected = NULL, width = "100%", multiple = TRUE)
             ),
      column(2, uiOutput("search_button_ui"))
    ),
    fluidRow(
      br(),
      uiOutput("result")
    ),
  )
)

server <- function(input, output, session){
  
  observe({
    if (is.null(input$countries) || length(input$countries) == 0) {
      output$search_button_ui <- renderUI({
        actionButton("fetch", "Search", class = "disabled")
      })
    } else {
      output$search_button_ui <- renderUI({
        actionButton("fetch", "Search")
      })
    }
  })
  
  
  output$result <- renderUI({
    column(10, offset = 1,
           markdown("Hello, my name is Fahim.\n
            I have developed this app for learning purposes only.
            It takes a country name (or two or more than two countries for comparison purposes) as input and returns the most recent values of social, economic, and environmental indicators from the World Bank (https://data.worldbank.org/country).
            The source code is publicly available on my [GitHub](https://github.com/Fahim-Ahmad/wb_indicators/tree/r-shiny) account for anyone who is interested.")
           )
  })
  
  observeEvent(input$fetch, {
    selected_countries <- input$countries %>% gsub(" ", "-", .)
    
    df = data.frame()
    for (cnt in selected_countries) {
      df = bind_rows(df, fetch_data(cnt))
    }
    
    output$result <- renderUI({
      list(
        column(6, 
               box(title = "Social", width = NULL, status = "primary", solidHeader = FALSE,
                   HTML(display_data(df, "Social"))
               )
        ),
        column(6, 
               box(title = "Economic", width = NULL, status = "primary", solidHeader = FALSE,
                   HTML(display_data(df, "Economic"))
               )
        ),
        column(6, 
               box(title = "Environment", width = NULL, status = "primary", solidHeader = FALSE,
                   HTML(display_data(df, "Environment"))
               )
        ),
        column(6, 
               box(title = "Institutions", width = NULL, status = "primary", solidHeader = FALSE,
                   HTML(display_data(df, "Institutions"))
               )
        )
      )
    })
  
  })
  
}

shinyApp(ui = ui, server = server)

