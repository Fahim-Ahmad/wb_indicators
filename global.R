if(!require(tidyverse)) install.packages("tidyverse")
if(!require(rvest)) install.packages("rvest")
if(!require(shinydashboard)) install.packages("shinydashboard")
if(!require(shiny)) install.packages("shiny")

countries <- rvest::read_html('https://data.worldbank.org/country')
countries <- countries %>% 
  html_nodes("section.nav-item > ul > li") %>% 
  html_text() #%>% 
  # gsub(" ", "-", .)

fetch_data <- function(country) {
  
  data_df <- data.frame(
    type = character(),
    name = character(),
    href = character(),
    value = character(),
    year = character(),
    stringsAsFactors = FALSE
  )
  
  contents <- read_html(glue::glue('https://data.worldbank.org/country/{country}'))
  indicator_items <- contents %>% html_nodes('.indicator-item')
  
  for (i in indicator_items) {
    type <- i %>% html_nodes('h1') %>% html_text()
    
    i_inner <- i %>% html_nodes('.indicator-item__wrapper > .indicator-item__inner')
    
    for (ii in i_inner) {
      name <- ii %>% html_nodes('div.indicator-item__title') %>% html_text()
      
      value <- ii %>% html_nodes('div.indicator-item__data-info') %>% html_text()
      value <- ifelse(length(value) == 0, "No data available", value)
      
      year <- ii %>% html_nodes('p.indicator-item__data-info-year') %>% html_text()
      year <- ifelse(length(value) == 0, NA_character_, year)
      
      href <- ii %>% html_node('div.indicator-item__title > a') %>% html_attr('href')
      href <- glue::glue("https://data.worldbank.org{href}")
      
      new_row <- data.frame(
        type = type,
        name = name,
        href = href,
        value = value,
        year = year,
        stringsAsFactors = FALSE
      )
      
      data_df <- bind_rows(data_df, new_row)
    }
    
  }
  
  data_df <- data_df %>% mutate(country = country)
  return(data_df)
}

# df <- fetch_data('afghanistan')
# df = data.frame()
# for (cnt in c("Afghanistan", "Algeria", "Andorra", "American Samoa")) {
#   df = bind_rows(df, fetch_data(cnt))
# }

display_data <- function(data, category) {
  text <- ""
  for (cnt in unique(data$country)) {
    sub_df <- data %>% filter(type == category & country == cnt)
    
    if (length(unique(data$country)) > 1) {
      text <- glue::glue("{text}<div><h4 class='country-name'>{cnt}</h4>")
    } else {
      text <- glue::glue("{text}<div>")
    }
    # text <- glue::glue("{text}<div><h4 class='country-name'>{cnt}</h4>")
    
    text <- glue::glue("{text}<ul>")
    for (n in 1:nrow(sub_df)) {
      name <- glue::glue("<span class='indicator-name'>{sub_df[n, 'name']}</span>")
      year <- glue::glue("<span class='year'>{sub_df[n, 'year']}</span>")
      href <- sub_df[n, 'href']
      value <- sub_df[n, 'value']
      source <- ifelse(value != "No data available", glue::glue("[<span class='href'><a href='{href}'>source</a></span>]"), '')
      value <- ifelse(value != "No data available", glue::glue("<span class='value'>{sub_df[n, 'value']}</span>"), glue::glue("<span class='no-data'>{sub_df[n, 'value']}</span>"))
      text <- glue::glue("{text} <li>{name} {source}<br>{value} {ifelse(is.na(sub_df[n, 'year']), '', year)} </li>")
    }
    
    text <- glue::glue("{text}</ul></div>")
  }
  return(text)
}

# display_data(df, "Social")
# df %>% filter(country == "afghanistan") %>% display_data("Social")



