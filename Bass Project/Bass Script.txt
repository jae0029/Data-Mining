install.packages("tidyverse")
library(tidyverse)

setwd("~/Library/CloudStorage/OneDrive-AuburnUniversity/Auburn/School/Grad_School/Current/Data Mining/Bass Project")

bass <- read_csv("/Users/joshuaetherton/Library/CloudStorage/OneDrive-AuburnUniversity/Auburn/School/Grad_School/Current/Data Mining/Bass Project/bassmaster_fantasy_results.csv")

glimpse(bass)

summary(bass)

head(bass)

bass <- bass %>%
  mutate(
    place = as.numeric(place),
    fish = as.numeric(fish),
    weight_oz = as.numeric(weight_oz),
    fantasy_points = as.numeric(fantasy_points),
    year = as.numeric(year)
  )

colSums(is.na(bass))

bass <- bass %>%
  mutate(
    weight_lb = weight_oz / 16
  )

bass <- bass %>%
  mutate(
    fishery = str_remove(
      tournament_name,
      "^\\d{4}\\sBassmaster Elite at\\s"
    )
  )

# bass <- bass %>%
#   mutate(
#     livescope_era = ifelse(year >= 2019,
#                            "Post",
#                            "Pre")
#   )
# 
# table(bass$livescope_era)

bass <- bass %>%
  mutate(
    weight_per_fish = weight_oz / fish
  )

tournament_summary <- bass %>%
  group_by(tournament_name, year) %>%
  summarise(
    avg_weight = mean(weight_lb, na.rm = TRUE),
    avg_fish = mean(fish, na.rm = TRUE),
    avg_points = mean(fantasy_points, na.rm = TRUE),
    winner_weight = max(weight_lb, na.rm = TRUE),
    anglers = n()
  )

fishery_trends <- bass %>%
  group_by(fishery, year) %>%
  summarise(
    mean_weight = mean(weight_lb, na.rm = TRUE),
    mean_fish = mean(fish, na.rm = TRUE)
  )

ggplot(fishery_trends,
       aes(year, mean_weight,
           color = fishery)) +
  geom_line() +
  theme_minimal()

bass %>%
  filter(weight_oz < 0)

library(stringr)

bass <- bass %>%
  mutate(
    tournament_url =
      str_extract(
        tournament_url,
        "https://[^\">]+"
      )
  )

bass <- bass %>%
  mutate(
    big_bag = replace_na(big_bag, 0),
    big_bass = replace_na(big_bass, 0),
    leader_bonus = replace_na(leader_bonus, 0)
  )

bass <- bass %>%
  mutate(
    fishery =
      str_remove(
        tournament_name,
        "^\\d{4}\\s"
      )
  )

bass <- bass %>%
  mutate(
    fishery =
      case_when(
        str_detect(tournament_name, "St\\. Lawrence") ~ "St. Lawrence River",
        str_detect(tournament_name, "Guntersville") ~ "Lake Guntersville",
        str_detect(tournament_name, "Champlain") ~ "Lake Champlain",
        str_detect(tournament_name, "Fork") ~ "Lake Fork",
        str_detect(tournament_name, "Hartwell") ~ "Lake Hartwell",
        TRUE ~ tournament_name
      )
  )

annual <- bass %>%
  group_by(year) %>%
  summarise(
    mean_weight =
      mean(weight_lb,
           na.rm = TRUE)
  )

ggplot(
  annual,
  aes(year,
      mean_weight)
) +
  geom_line() +
  geom_point() +
  theme_minimal() +
  labs(
    y = "Average Weight (lb)",
    x = "Year"
  )

winners <- bass %>%
  group_by(
    tournament_name,
    year
  ) %>%
  summarise(
    winning_weight =
      max(weight_lb)
  )

ggplot(
  winners,
  aes(year,
      winning_weight)
) +
  geom_point() +
  geom_smooth(se = FALSE)

sort(unique(bass$tournament_name))

library(tidyverse)

bass <- bass %>%
  mutate(
    fishery = case_when(
      
      str_detect(tournament_name, "St\\. Lawrence") ~ "St. Lawrence River",
      str_detect(tournament_name, "St\\. Clair") ~ "Lake St. Clair",
      str_detect(tournament_name, "Guntersville") ~ "Lake Guntersville",
      str_detect(tournament_name, "Champlain") ~ "Lake Champlain",
      str_detect(tournament_name, "Hartwell") ~ "Lake Hartwell",
      str_detect(tournament_name, "Fork") ~ "Lake Fork",
      str_detect(tournament_name, "Murray") ~ "Lake Murray",
      str_detect(tournament_name, "Seminole") ~ "Lake Seminole",
      str_detect(tournament_name, "Okeechobee") ~ "Lake Okeechobee",
      str_detect(tournament_name, "Oahe") ~ "Lake Oahe",
      str_detect(tournament_name, "Pickwick") ~ "Pickwick Lake",
      str_detect(tournament_name, "Martin") ~ "Lake Martin",
      str_detect(tournament_name, "Wheeler") ~ "Wheeler Lake",
      str_detect(tournament_name, "Toledo Bend") ~ "Toledo Bend",
      str_detect(tournament_name, "Champlain") ~ "Lake Champlain",
      str_detect(tournament_name, "Sabine") ~ "Sabine River",
      str_detect(tournament_name, "Mississippi River") ~ "Mississippi River",
      str_detect(tournament_name, "Potomac") ~ "Potomac River",
      str_detect(tournament_name, "Chesapeake") ~ "Chesapeake Bay",
      str_detect(tournament_name, "Winyah") ~ "Winyah Bay",
      str_detect(tournament_name, "Cayuga") ~ "Cayuga Lake",
      str_detect(tournament_name, "Lay Lake") ~ "Lay Lake",
      str_detect(tournament_name, "Smith Lake") ~ "Smith Lake",
      str_detect(tournament_name, "Harris Chain") ~ "Harris Chain",
      str_detect(tournament_name, "West Point") ~ "West Point Lake",
      
      TRUE ~ NA_character_
    )
  )

table(is.na(bass$fishery))

bass %>%
  filter(is.na(fishery)) %>%
  distinct(tournament_name) %>%
  arrange(tournament_name)


bass %>%
  group_by(year) %>%
  summarise(
    tournaments = n_distinct(tournament_name)
  )

bass <- bass %>%
  filter(weight_oz >= 0)

bass %>%
  filter(is.na(fishery)) %>%
  count(tournament_name, sort = TRUE)

bass %>%
  filter(tournament_name == "Douglas Lake Challenge") %>%
  select(year, tournament_name) %>%
  distinct()

bass %>%
  filter(is.na(fishery)) %>%
  count(tournament_name, sort = TRUE) %>%
  print(n = 60)

bass <- bass %>%
  mutate(
    fishery = case_when(
      is.na(fishery) & str_detect(tournament_name, "St\\. Johns|St\\. John’s") ~ "St. Johns River",
      is.na(fishery) & str_detect(tournament_name, "Lanier") ~ "Lake Lanier",
      is.na(fishery) & str_detect(tournament_name, "Tenkiller") ~ "Lake Tenkiller",
      is.na(fishery) & str_detect(tournament_name, "Cherokee") ~ "Lake Cherokee",
      is.na(fishery) & str_detect(tournament_name, "Dardanelle") ~ "Lake Dardanelle",
      is.na(fishery) & str_detect(tournament_name, "Ross Barnett") ~ "Ross Barnett Reservoir",
      is.na(fishery) & str_detect(tournament_name, "Santee Cooper") ~ "Santee Cooper",
      TRUE ~ fishery
    )
  )

table(is.na(bass$fishery))

bass <- bass %>%
  mutate(weight_lb = weight_oz / 16)

summary(bass$weight_lb)

bass <- bass %>%
  mutate(
    fishery = case_when(
      is.na(fishery) & str_detect(tournament_name, "Lake Havasu") ~ "Lake Havasu",
      is.na(fishery) & str_detect(tournament_name, "Sacramento River") ~ "Sacramento River",
      is.na(fishery) & str_detect(tournament_name, "Kentucky Lake") ~ "Kentucky Lake",
      is.na(fishery) & str_detect(tournament_name, "Table Rock") ~ "Table Rock Lake",
      is.na(fishery) & str_detect(tournament_name, "Bull Shoals") ~ "Bull Shoals/Norfork",
      is.na(fishery) & str_detect(tournament_name, "Grand Lake") ~ "Grand Lake",
      is.na(fishery) & str_detect(tournament_name, "Pasquotank") ~ "Pasquotank River",
      is.na(fishery) & str_detect(tournament_name, "Arkansas River") ~ "Arkansas River",
      is.na(fishery) & str_detect(tournament_name, "Tennessee River") ~ "Tennessee River",
      is.na(fishery) & str_detect(tournament_name, "Tennessee-Tombigbee") ~ "Tennessee-Tombigbee Waterway",
      is.na(fishery) & str_detect(tournament_name, "Neely Henry") ~ "Neely Henry Lake",
      is.na(fishery) & str_detect(tournament_name, "Chickamauga") ~ "Chickamauga Lake",
      is.na(fishery) & str_detect(tournament_name, "Eufaula") ~ "Lake Eufaula",
      
      TRUE ~ fishery
    )
  )

table(is.na(bass$fishery))

write_csv(
  bass,
  "bass_cleaned.csv"
)

bass %>%
  filter(!is.na(fishery)) %>%
  count(fishery, sort = TRUE)

bass %>%
  filter(!is.na(fishery)) %>%
  group_by(fishery) %>%
  summarise(
    years = n_distinct(year),
    tournaments = n_distinct(tournament_name)
  ) %>%
  arrange(desc(years))

fishery_year <- bass %>%
  filter(!is.na(fishery)) %>%
  group_by(fishery, year) %>%
  summarise(
    mean_weight_oz = mean(weight_oz, na.rm = TRUE),
    winner_weight_oz = max(weight_oz, na.rm = TRUE),
    mean_fish = mean(fish, na.rm = TRUE),
    n_anglers = n(),
    .groups = "drop"
  )

library(ggplot2)

fishery_year %>%
  filter(fishery %in% c(
    "St. Lawrence River",
    "Lake Champlain",
    "Lake Guntersville",
    "Lake Fork"
  )) %>%
  ggplot(
    aes(
      x = year,
      y = winner_weight_oz,
      color = fishery
    )
  ) +
  geom_line() +
  geom_point() +
  theme_minimal()

tournaments = unique(bass$tournament_name)
tournaments
str(bass)

bass <- bass %>%
  mutate(
    tech_era = case_when(
      year <= 2018 ~ "Pre-LiveScope",
      year <= 2020 ~ "Transition",
      TRUE ~ "LiveScope Era"
    )
  )

tournaments = unique(bass$tournament_name) 


tournaments = bass %>%
  distinct(tech_era, tournament_name) %>%
  arrange(tech_era, tournament_name) %>%
  print(n = 180)

write_csv(
  tournaments,
  "tournaments.csv"
)

# Updated ####
library(tidyverse)

setwd("~/Library/CloudStorage/OneDrive-AuburnUniversity/Auburn/School/Grad_School/Current/Data Mining/Bass Project")

bass <- read_csv("/Users/joshuaetherton/Library/CloudStorage/OneDrive-AuburnUniversity/Auburn/School/Grad_School/Current/Data Mining/Bass Project/bassmaster_output/bassmaster_complete_participant_records.csv")

bass %>%
  group_by(Season_Year) %>%
  summarise(
    tournaments = n_distinct(Event_Name)
  )

bass %>%
  group_by(Event_Name) %>%
  summarise(
    tournaments = n_distinct(Season_Year)
  ) %>%
  print(n = 180)

tournaments = unique(bass$Event_Name)

str(bass)

## 1. Distribution of Tournament Weights ####
# This tells you whether weights are roughly normal, skewed, bimodal, etc.
ggplot(bass, aes(x = Weight_Lbs_Calculated)) +
  geom_histogram(bins = 40, fill = "steelblue", color = "white") +
  labs(
    title = "Distribution of Catch Weights",
    x = "Weight (lb)",
    y = "Count"
  ) +
  theme_minimal()

## 2. Distribution of Fish Caught ####
ggplot(bass, aes(x = Fish_Caught)) +
  geom_histogram(binwidth = 1,
                 fill = "forestgreen",
                 color = "white") +
  labs(
    title = "Distribution of Fish Caught",
    x = "Fish Caught",
    y = "Count"
  ) +
  theme_minimal()

## 3. Weight vs Number of Fish ####
# Probably the single most informative exploratory plot.
ggplot(bass,
       aes(x = Fish_Caught,
           y = Weight_Lbs_Calculated)) +
  geom_point(alpha = 0.2) +
  geom_smooth(method = "loess",
              se = FALSE,
              color = "red") +
  labs(
    title = "Catch Weight vs Fish Caught",
    x = "Fish Caught",
    y = "Weight (lb)"
  ) +
  theme_minimal()

## 4. Weight by Place ####
ggplot(bass,
       aes(x = Place,
           y = Weight_Lbs_Calculated)) +
  geom_point(alpha = 0.1) +
  geom_smooth(se = FALSE,
              color = "blue") +
  labs(
    title = "Catch Weight by Tournament Finish",
    x = "Place",
    y = "Weight (lb)"
  ) +
  theme_minimal()

## 5. Winning Weights Over Time ####
# Just winners:
bass %>%
  filter(Place == 1) %>%
  ggplot(aes(x = Season_Year,
             y = Weight_Lbs_Calculated)) +
  geom_point() +
  geom_smooth(se = FALSE) +
  labs(
    title = "Winning Weights Through Time",
    x = "Year",
    y = "Winning Weight (lb)"
  ) +
  theme_minimal()

## 6. Variation Among Tournaments ####
# Tough fisheries, Productive fisheries, Tournaments with unusually high variation
bass %>%
  ggplot(aes(x = reorder(Event_Name,
                         Weight_Lbs_Calculated,
                         median),
             y = Weight_Lbs_Calculated)) +
  geom_boxplot() +
  coord_flip() +
  labs(
    title = "Catch Weight Distribution by Tournament",
    x = "",
    y = "Weight (lb)"
  ) +
  theme_minimal()

## 7. Average Fish Size ####
bass <- bass %>%
  mutate(
    Avg_Fish_Weight =
      Weight_Lbs_Calculated / Fish_Caught
  )

ggplot(bass,
       aes(x = Avg_Fish_Weight)) +
  geom_histogram(bins = 40,
                 fill = "orange",
                 color = "white") +
  labs(
    title = "Distribution of Average Fish Size",
    x = "Average Weight per Fish (lb)",
    y = "Count"
  ) +
  theme_minimal()

## Summary Table ####
bass %>%
  summarise(
    n = n(),
    min_weight = min(Weight_Lbs_Calculated, na.rm = TRUE),
    mean_weight = mean(Weight_Lbs_Calculated, na.rm = TRUE),
    median_weight = median(Weight_Lbs_Calculated, na.rm = TRUE),
    max_weight = max(Weight_Lbs_Calculated, na.rm = TRUE),
    min_fish = min(Fish_Caught, na.rm = TRUE),
    mean_fish = mean(Fish_Caught, na.rm = TRUE),
    median_fish = median(Fish_Caught, na.rm = TRUE),
    max_fish = max(Fish_Caught, na.rm = TRUE)
  )

## Average Fish Weight Over Time ####
library(dplyr)
library(ggplot2)

bass <- bass %>%
  mutate(
    Avg_Fish_Weight = Weight_Lbs_Calculated / Fish_Caught
  )

avg_fish_year <- bass %>%
  filter(Fish_Caught > 0) %>%
  group_by(Season_Year) %>%
  summarize(
    Avg_Fish_Weight = mean(Avg_Fish_Weight, na.rm = TRUE)
  )

ggplot(avg_fish_year,
       aes(x = Season_Year,
           y = Avg_Fish_Weight)) +
  geom_line(linewidth = 1) +
  geom_point(size = 2) +
  labs(
    title = "Average Fish Weight Over Time",
    x = "Year",
    y = "Average Fish Weight (lb/fish)"
  ) +
  theme_minimal()

ggplot(
  bass %>% filter(Fish_Caught > 0),
  aes(x = factor(Season_Year),
      y = Avg_Fish_Weight)
) +
  geom_boxplot() +
  labs(
    title = "Average Fish Weight by Year",
    x = "Year",
    y = "Average Fish Weight (lb/fish)"
  ) +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1)
  )

## Average Fish Weight of Top Ten Over Time ####
library(dplyr)
library(ggplot2)

top10 <- bass %>%
  filter(Place <= 10,
         Fish_Caught > 0) %>%
  mutate(
    Avg_Fish_Weight = Weight_Lbs_Calculated / Fish_Caught
  )

avg_fish_year_top10 <- top10 %>%
  group_by(Season_Year) %>%
  summarize(
    Avg_Fish_Weight = mean(Avg_Fish_Weight, na.rm = TRUE)
  )

ggplot(avg_fish_year_top10,
       aes(x = Season_Year,
           y = Avg_Fish_Weight)) +
  geom_line(linewidth = 1) +
  geom_point(size = 2) +
  labs(
    title = "Average Fish Weight Over Time (Top 10 Finishers)",
    x = "Year",
    y = "Average Fish Weight (lb/fish)"
  ) +
  theme_minimal()

avg_fish_year_top10 <- top10 %>%
  group_by(Season_Year) %>%
  summarize(
    mean_weight = mean(Avg_Fish_Weight, na.rm = TRUE),
    sd_weight = sd(Avg_Fish_Weight, na.rm = TRUE)
  )

ggplot(avg_fish_year_top10,
       aes(x = Season_Year, y = mean_weight)) +
  geom_ribbon(
    aes(ymin = mean_weight - sd_weight,
        ymax = mean_weight + sd_weight),
    alpha = 0.2
  ) +
  geom_line(linewidth = 1) +
  geom_point(size = 2) +
  labs(
    title = "Average Fish Weight by Year (Top 10 Finishers)",
    x = "Year",
    y = "Average Fish Weight (lb/fish)"
  ) +
  theme_minimal()

top10 %>%
  group_by(Season_Year, Tournament_ID, Event_Name) %>%
  summarize(
    Avg_Fish_Weight = mean(Avg_Fish_Weight, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  ggplot(aes(x = Season_Year, y = Avg_Fish_Weight)) +
  geom_jitter(width = 0.2, alpha = 0.5) +
  geom_smooth(se = FALSE, color = "red") +
  labs(
    title = "Tournament-Level Average Fish Weight (Top 10 Finishers)",
    x = "Year",
    y = "Average Fish Weight (lb/fish)"
  ) +
  theme_minimal()

# Analysis ####
## 1. Average Fish Weight Over Time, Colored by FFS Status ####
bass %>%
  filter(
    Place <= 10,
    Fish_Caught > 0
  ) %>%
  mutate(
    Avg_Fish_Weight = Weight_Lbs_Calculated / Fish_Caught
  ) %>%
  group_by(Season_Year, Allowed_FFS) %>%
  summarize(
    Avg_Fish_Weight = mean(Avg_Fish_Weight, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  ggplot(aes(
    x = Season_Year,
    y = Avg_Fish_Weight,
    color = Allowed_FFS
  )) +
  geom_line(linewidth = 1) +
  geom_point() +
  labs(
    title = "Average Fish Weight Over Time by FFS Status",
    x = "Year",
    y = "Average Fish Weight (lb/fish)",
    color = "FFS Status"
  ) +
  theme_minimal()

## 2. Distribution of Average Fish Weight by FFS Category ####
bass %>%
  filter(
    Place <= 10,
    Fish_Caught > 0
  ) %>%
  mutate(
    Avg_Fish_Weight = Weight_Lbs_Calculated / Fish_Caught
  ) %>%
  ggplot(aes(
    x = Allowed_FFS,
    y = Avg_Fish_Weight
  )) +
  geom_boxplot() +
  labs(
    title = "Average Fish Weight by FFS Status",
    x = "FFS Status",
    y = "Average Fish Weight (lb/fish)"
  ) +
  theme_minimal() +
  coord_flip()

## 3. Top-10 Tournament Average Fish Weight by Year ####
# Sometimes yearly averages hide a lot of variation.
bass %>%
  filter(
    Place <= 10,
    Fish_Caught > 0
  ) %>%
  mutate(
    Avg_Fish_Weight = Weight_Lbs_Calculated / Fish_Caught
  ) %>%
  group_by(
    Season_Year,
    Tournament_ID,
    Allowed_FFS
  ) %>%
  summarize(
    Avg_Fish_Weight = mean(Avg_Fish_Weight),
    .groups = "drop"
  ) %>%
  ggplot(aes(
    x = Season_Year,
    y = Avg_Fish_Weight,
    color = Allowed_FFS
  )) +
  geom_jitter(width = 0.25, alpha = 0.6) +
  geom_smooth(se = FALSE) +
  labs(
    title = "Tournament-Level Average Fish Weight",
    x = "Year",
    y = "Average Fish Weight (lb/fish)"
  ) +
  theme_minimal()

## 4. Total Catch Weight of Top 10 by Year ####
bass %>%
  filter(Place <= 10) %>%
  group_by(
    Season_Year,
    Allowed_FFS
  ) %>%
  summarize(
    Avg_Weight = mean(Weight_Lbs_Calculated),
    .groups = "drop"
  ) %>%
  ggplot(aes(
    x = Season_Year,
    y = Avg_Weight,
    color = Allowed_FFS
  )) +
  geom_line(linewidth = 1) +
  geom_point() +
  labs(
    title = "Average Top-10 Catch Weight Over Time",
    x = "Year",
    y = "Average Catch Weight (lb)"
  ) +
  theme_minimal()

## 5. Fish Caught by FFS Status ####
# # 
# # This helps distinguish whether anglers are catching:
# # more fish
# # bigger fish
# # or both
# bass %>%
#   filter(Place <= 10) %>%
#   ggplot(aes(
#     x = Allowed_FFS,
#     y = Fish_Caught
#   )) +
#   geom_boxplot() +
#   labs(
#     title = "Fish Caught by Top-10 Anglers",
#     x = "FFS Status",
#     y = "Number of Fish"
#   ) +
#   theme_minimal() +
#   coord_flip()

## 6. Average Fish Weight Over Time By FFS Allowance ####
bass %>%
  filter(
    Place <= 10,
    Fish_Caught > 0
  ) %>%
  mutate(
    Avg_Fish_Weight = Weight_Lbs_Calculated /
      Fish_Caught
  ) %>%
  ggplot(aes(
    x = Season_Year,
    y = Avg_Fish_Weight,
    color = Allowed_FFS
  )) +
  geom_jitter(
    width = 0.2,
    alpha = 0.3
  ) +
  geom_smooth(
    se = TRUE,
    linewidth = 1.2
  ) +
  labs(
    title = "Top-10 Average Fish Weight Through Time",
    x = "Year",
    y = "Average Fish Weight (lb/fish)"
  ) +
  theme_minimal()

## Identify Waters With Both Eras
Common_Waters <- bass %>%
  distinct(Location, Allowed_FFS) %>%
  count(Location) %>%
  arrange(desc(n))

Common_Waters %>% print(n = 76)

# common_waters <- bass %>%
#   group_by(Location) %>%
#   summarise(
#     n_ffs_states = n_distinct(Allowed_FFS)
#   ) %>%
#   filter(n_ffs_states > 1) %>%
#   pull(Location)

## 7. Compare Top-10 Average Fish Weight ####
bass %>%
  filter(
    Location %in% common_waters,
    # Place <= 10,
    Fish_Caught > 0
  ) %>%
  mutate(
    Avg_Fish_Weight = Weight_Lbs_Calculated / Fish_Caught
  ) %>%
  ggplot(
    aes(
      x = Allowed_FFS,
      y = Avg_Fish_Weight
    )
  ) +
  geom_boxplot() +
  facet_wrap(~ Location, scales = "free_y") +
  labs(
    title = "Top-10 Average Fish Weight by Water Body",
    x = "FFS Status",
    y = "Average Fish Weight (lb/fish)"
  ) +
  theme_minimal()


location_summary <- bass %>%
  filter(
    # Place <= 10,
    Fish_Caught > 0
  ) %>%
  mutate(
    Avg_Fish_Weight = Weight_Lbs_Calculated / Fish_Caught
  ) %>%
  group_by(Location, Allowed_FFS) %>%
  summarise(
    Mean_Fish_Weight = mean(Avg_Fish_Weight),
    .groups = "drop"
  )

ggplot(
  location_summary,
  aes(
    x = Allowed_FFS,
    y = Mean_Fish_Weight,
    group = Location
  )
) +
  geom_line(alpha = 0.5) +
  geom_point(size = 2) +
  labs(
    title = "Change in Average Fish Weight Within Water Bodies",
    x = "FFS Status",
    y = "Average Fish Weight (lb/fish)"
  ) +
  theme_minimal()

# Add Season ####
library(stringr)

bass <- bass %>%
  mutate(
    Month = str_extract(Tournament_Dates,
                        "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec")
  )

tourn_summary <- bass %>%
  filter(
    # Place <= 10,
    Fish_Caught > 0
  ) %>%
  mutate(
    Avg_Fish_Weight = Weight_Lbs_Calculated / Fish_Caught
  ) %>%
  group_by(
    Tournament_ID,
    Event_Name,
    Location,
    Month,
    Allowed_FFS,
    Season_Year
  ) %>%
  summarize(
    Mean_Fish_Weight = mean(Avg_Fish_Weight),
    Mean_Catch_Weight = mean(Weight_Lbs_Calculated),
    Mean_Fish_Caught = mean(Fish_Caught),
    .groups = "drop"
  )

comparison_lakes <- tourn_summary %>%
  group_by(Location) %>%
  summarize(
    n_eras = n_distinct(Allowed_FFS)
  ) %>%
  filter(n_eras > 1) %>%
  pull(Location)

tourn_summary2 <- tourn_summary %>%
  filter(Location %in% comparison_lakes)

ggplot(
  tourn_summary2,
  aes(
    x = Allowed_FFS,
    y = Mean_Fish_Weight
  )
) +
  geom_boxplot() +
  facet_wrap(~ Location) +
  theme_minimal()

ggplot(
  tourn_summary2,
  aes(
    x = Allowed_FFS,
    y = Mean_Fish_Weight
  )
) +
  geom_boxplot() +
  facet_grid(
    Month ~ Location,
    scales = "free_y"
  ) +
  theme_minimal()

paired <- tourn_summary %>%
  group_by(
    Location,
    Month,
    Allowed_FFS
  ) %>%
  summarize(
    Mean_Fish_Weight = mean(Mean_Fish_Weight),
    .groups = "drop"
  )

ggplot(
  paired,
  aes(
    x = Allowed_FFS,
    y = Mean_Fish_Weight,
    group = interaction(Location, Month)
  )
) +
  geom_line(alpha = 0.4) +
  geom_point(size = 2) +
  theme_minimal() +
  labs(
    title = "Average Fish Weight Within Location-Month Pairs",
    x = "FFS Status",
    y = "Average Fish Weight (lb/fish)"
  )

paired2 <- paired %>%
  filter(Allowed_FFS != "Unknown") %>%
  mutate(
    FFS_Group = case_when(
      Allowed_FFS == "No FFS Existed" ~ "Pre-FFS",
      Allowed_FFS == "No" ~ "FFS Not Allowed",
      Allowed_FFS %in% c("Yes (Restricted)",
                         "Yes (Unrestricted)") ~ "FFS Allowed"
    )
  )

paired_wide <- paired2 %>%
  group_by(Location, Month, FFS_Group) %>%
  summarize(
    Mean_Fish_Weight = mean(Mean_Fish_Weight),
    .groups = "drop"
  ) %>%
  tidyr::pivot_wider(
    names_from = FFS_Group,
    values_from = Mean_Fish_Weight
  )

paired_wide <- paired_wide %>%
  mutate(
    Difference = `FFS Allowed` - `Pre-FFS`
  )

ggplot(paired_wide,
       aes(x = Difference)) +
  geom_histogram(
    bins = 15,
    fill = "steelblue",
    color = "white"
  ) +
  geom_vline(
    xintercept = 0,
    linetype = "dashed",
    color = "red"
  ) +
  theme_minimal() +
  labs(
    title = "Change in Average Fish Weight After FFS",
    x = "Difference (lb/fish)",
    y = "Count"
  )

paired2 %>%
  count(Location, Month, FFS_Group) %>%
  tidyr::pivot_wider(
    names_from = FFS_Group,
    values_from = n,
    values_fill = 0
  ) %>% print(n = 120)

bass %>%
  count(Location, sort = TRUE) %>% print(n = 120)

library(dplyr)
library(stringr)

bass <- bass %>%
  mutate(
    Waterbody = case_when(
      
      # Guntersville
      str_detect(Location,
                 "Scottsboro|Guntersville|Lake Guntersville|Gadsden|Cullman") ~
        "Lake Guntersville",
      
      # St. Lawrence River
      str_detect(Location,
                 "Waddington|Clayton|St\\. Lawrence River") ~
        "St. Lawrence River",
      
      # Champlain
      str_detect(Location,
                 "Plattsburgh|Burlington") ~
        "Lake Champlain",
      
      # St. Johns
      str_detect(Location,
                 "Palatka|St\\. Johns River") ~
        "St. Johns River",
      
      # Okeechobee
      str_detect(Location,
                 "Okeechobee|Lake Okeechobee") ~
        "Lake Okeechobee",
      
      # Hartwell
      str_detect(Location,
                 "Anderson|Lake Hartwell") ~
        "Lake Hartwell",
      
      # Grand Lake
      str_detect(Location,
                 "Grand Lake") ~
        "Grand Lake",
      
      # Toledo Bend
      str_detect(Location,
                 "Many, LA") ~
        "Toledo Bend Reservoir",
      
      # Sabine
      str_detect(Location,
                 "Orange, TX|Sabine River") ~
        "Sabine River",
      
      # Mississippi River
      str_detect(Location,
                 "La Crosse|Mississippi River") ~
        "Mississippi River",
      
      # Lake Fork
      str_detect(Location,
                 "Yantis|Quitman") ~
        "Lake Fork",
      
      # Wheeler Lake
      str_detect(Location,
                 "Decatur, AL") ~
        "Wheeler Lake",
      
      # Pickwick
      str_detect(Location,
                 "Florence, AL|Counce, TN") ~
        "Pickwick Lake",
      
      # Lake Murray
      str_detect(Location,
                 "Columbia, SC|Prosperity, SC") ~
        "Lake Murray",
      
      # Santee Cooper
      str_detect(Location,
                 "Clarendon County|Manning, SC") ~
        "Santee Cooper",
      
      # Lake Eufaula
      str_detect(Location,
                 "Eufaula, AL") ~
        "Lake Eufaula",
      
      # Oneida
      str_detect(Location,
                 "Union Springs|Oneida Lake") ~
        "Oneida Lake",
      
      # Chickamauga
      str_detect(Location,
                 "Dayton, TN") ~
        "Lake Chickamauga",
      
      # Douglas
      str_detect(Location,
                 "Jefferson City|Douglas Lake") ~
        "Douglas Lake",
      
      # Cherokee
      str_detect(Location,
                 "Alexander City") ~
        "Lake Martin",
      
      # Potomac
      str_detect(Location,
                 "Charles County|Cecil County") ~
        "Potomac River",
      
      # St Clair
      str_detect(Location,
                 "Macomb County|Detroit") ~
        "Lake St. Clair",
      
      # Tennessee River Knoxville events
      str_detect(Location,
                 "Knoxville|Tennessee River") ~
        "Tennessee River (Knoxville)",
      
      # Generic unknown
      Location == "Unknown Location" ~
        "Unknown",
      
      TRUE ~ Location
    )
  )

bass %>%
  count(Waterbody, sort = TRUE) %>%
  print(n = Inf)

bass %>%
  filter(Allowed_FFS != "Unknown") %>%
  distinct(Waterbody, Allowed_FFS) %>%
  count(Waterbody) %>%
  arrange(desc(n))

bass %>%
  filter(Allowed_FFS != "Unknown") %>%
  group_by(Waterbody) %>%
  summarize(
    FFS_Categories = paste(sort(unique(Allowed_FFS)),
                           collapse = ", "),
    n_tournaments = n_distinct(Tournament_ID)
  ) %>%
  arrange(desc(n_tournaments)) %>%
  print(n = Inf)

tourn <- bass %>%
  filter(
    # Place <= 10,
    Fish_Caught > 0,
    Allowed_FFS != "Unknown"
  ) %>%
  mutate(
    Avg_Fish_Weight = Weight_Lbs_Calculated / Fish_Caught
  ) %>%
  group_by(
    Tournament_ID,
    Season_Year,
    Waterbody,
    Allowed_FFS
  ) %>%
  summarize(
    Mean_Fish_Weight = mean(Avg_Fish_Weight),
    Mean_Catch_Weight = mean(Weight_Lbs_Calculated),
    Mean_Fish_Caught = mean(Fish_Caught),
    .groups = "drop"
  )

### Plot 1: Average fish weight by fishery and FFS status ####
ggplot(
  tourn,
  aes(
    x = Allowed_FFS,
    y = Mean_Fish_Weight
  )
) +
  geom_point(size = 3) +
  facet_wrap(~ Waterbody, scales = "free_y") +
  theme_minimal() +
  labs(
    title = "Average Fish Weight by Fishery",
    y = "Average Fish Weight (lb/fish)"
  )

### Plot 2: Paired change within waterbody ####
ffs_compare <- tourn %>%
  mutate(
    Era = case_when(
      Allowed_FFS == "No FFS Existed" ~ "Pre-FFS",
      Allowed_FFS == "No" ~ "FFS Banned",
      TRUE ~ "FFS Allowed"
    )
  ) %>%
  group_by(Waterbody, Era) %>%
  summarize(
    Mean_Fish_Weight = mean(Mean_Fish_Weight),
    .groups = "drop"
  )

ggplot(
  ffs_compare,
  aes(
    x = Era,
    y = Mean_Fish_Weight,
    group = Waterbody
  )
) +
  geom_line(alpha = 0.7) +
  geom_point(size = 3) +
  theme_minimal() +
  labs(
    title = "Change in Average Fish Weight Within Fisheries",
    y = "Average Fish Weight (lb/fish)"
  )

### Plot 3: Top-10 catch weight before and after FFS ####
ggplot(
  tourn,
  aes(
    x = Allowed_FFS,
    y = Mean_Catch_Weight
  )
) +
  geom_boxplot() +
  facet_wrap(~ Waterbody, scales = "free_y") +
  theme_minimal() +
  labs(
    title = "Top-10 Average Catch Weight",
    y = "Weight (lb)"
  )

diffs <- ffs_compare %>%
  filter(Era %in% c("Pre-FFS", "FFS Allowed")) %>%
  tidyr::pivot_wider(
    names_from = Era,
    values_from = Mean_Fish_Weight
  ) %>%
  mutate(
    Difference = `FFS Allowed` - `Pre-FFS`
  ) %>%
  arrange(desc(Difference))

print(diffs) %>%
  print(n = Inf)

library(ggplot2)

diffs %>%
  filter(!is.na(Difference)) %>%
  ggplot(aes(
    x = reorder(Waterbody, Difference),
    y = Difference,
    fill = Difference > 0
  )) +
  geom_col() +
  coord_flip() +
  geom_hline(
    yintercept = 0,
    linetype = "dashed",
    color = "red"
  ) +
  labs(
    title = "Change in Average Fish Weight\n(FFS Era - Pre-FFS Era)",
    x = "",
    y = "Difference (lb/fish)"
  ) +
  theme_minimal() +
  theme(
    legend.position = "none"
  )

tourn %>%
  filter(
    Waterbody %in% c(
      "Lake Guntersville",
      "St. Lawrence River",
      "Lake Okeechobee",
      "Toledo Bend Reservoir"
    )
  ) %>%
  arrange(Waterbody, Season_Year)

tourn %>%
  filter(
    Waterbody %in% (
      diffs |>
        dplyr::filter(!is.na(Difference)) |>
        dplyr::pull(Waterbody)
    )
  ) %>%
  ggplot(
    aes(
      x = Season_Year,
      y = Mean_Fish_Weight,
      color = Allowed_FFS
    )
  ) +
  geom_point(size = 3) +
  geom_line(aes(group = 1)) +
  facet_wrap(~ Waterbody, scales = "free_y") +
  theme_minimal()

matched_waterbodies <- diffs %>%
  filter(!is.na(Difference)) %>%
  pull(Waterbody)

matched_waterbodies
install.packages("tidyverse")
library(tidyverse)

setwd("~/Library/CloudStorage/OneDrive-AuburnUniversity/Auburn/School/Grad_School/Current/Data Mining/Bass Project")

bass <- read_csv("/Users/joshuaetherton/Library/CloudStorage/OneDrive-AuburnUniversity/Auburn/School/Grad_School/Current/Data Mining/Bass Project/bassmaster_fantasy_results.csv")

glimpse(bass)

summary(bass)

head(bass)

bass <- bass %>%
  mutate(
    place = as.numeric(place),
    fish = as.numeric(fish),
    weight_oz = as.numeric(weight_oz),
    fantasy_points = as.numeric(fantasy_points),
    year = as.numeric(year)
  )

colSums(is.na(bass))

bass <- bass %>%
  mutate(
    weight_lb = weight_oz / 16
  )

bass <- bass %>%
  mutate(
    fishery = str_remove(
      tournament_name,
      "^\\d{4}\\sBassmaster Elite at\\s"
    )
  )

# bass <- bass %>%
#   mutate(
#     livescope_era = ifelse(year >= 2019,
#                            "Post",
#                            "Pre")
#   )
# 
# table(bass$livescope_era)

bass <- bass %>%
  mutate(
    weight_per_fish = weight_oz / fish
  )

tournament_summary <- bass %>%
  group_by(tournament_name, year) %>%
  summarise(
    avg_weight = mean(weight_lb, na.rm = TRUE),
    avg_fish = mean(fish, na.rm = TRUE),
    avg_points = mean(fantasy_points, na.rm = TRUE),
    winner_weight = max(weight_lb, na.rm = TRUE),
    anglers = n()
  )

fishery_trends <- bass %>%
  group_by(fishery, year) %>%
  summarise(
    mean_weight = mean(weight_lb, na.rm = TRUE),
    mean_fish = mean(fish, na.rm = TRUE)
  )

ggplot(fishery_trends,
       aes(year, mean_weight,
           color = fishery)) +
  geom_line() +
  theme_minimal()

bass %>%
  filter(weight_oz < 0)

library(stringr)

bass <- bass %>%
  mutate(
    tournament_url =
      str_extract(
        tournament_url,
        "https://[^\">]+"
      )
  )

bass <- bass %>%
  mutate(
    big_bag = replace_na(big_bag, 0),
    big_bass = replace_na(big_bass, 0),
    leader_bonus = replace_na(leader_bonus, 0)
  )

bass <- bass %>%
  mutate(
    fishery =
      str_remove(
        tournament_name,
        "^\\d{4}\\s"
      )
  )

bass <- bass %>%
  mutate(
    fishery =
      case_when(
        str_detect(tournament_name, "St\\. Lawrence") ~ "St. Lawrence River",
        str_detect(tournament_name, "Guntersville") ~ "Lake Guntersville",
        str_detect(tournament_name, "Champlain") ~ "Lake Champlain",
        str_detect(tournament_name, "Fork") ~ "Lake Fork",
        str_detect(tournament_name, "Hartwell") ~ "Lake Hartwell",
        TRUE ~ tournament_name
      )
  )

annual <- bass %>%
  group_by(year) %>%
  summarise(
    mean_weight =
      mean(weight_lb,
           na.rm = TRUE)
  )

ggplot(
  annual,
  aes(year,
      mean_weight)
) +
  geom_line() +
  geom_point() +
  theme_minimal() +
  labs(
    y = "Average Weight (lb)",
    x = "Year"
  )

winners <- bass %>%
  group_by(
    tournament_name,
    year
  ) %>%
  summarise(
    winning_weight =
      max(weight_lb)
  )

ggplot(
  winners,
  aes(year,
      winning_weight)
) +
  geom_point() +
  geom_smooth(se = FALSE)

sort(unique(bass$tournament_name))

library(tidyverse)

bass <- bass %>%
  mutate(
    fishery = case_when(
      
      str_detect(tournament_name, "St\\. Lawrence") ~ "St. Lawrence River",
      str_detect(tournament_name, "St\\. Clair") ~ "Lake St. Clair",
      str_detect(tournament_name, "Guntersville") ~ "Lake Guntersville",
      str_detect(tournament_name, "Champlain") ~ "Lake Champlain",
      str_detect(tournament_name, "Hartwell") ~ "Lake Hartwell",
      str_detect(tournament_name, "Fork") ~ "Lake Fork",
      str_detect(tournament_name, "Murray") ~ "Lake Murray",
      str_detect(tournament_name, "Seminole") ~ "Lake Seminole",
      str_detect(tournament_name, "Okeechobee") ~ "Lake Okeechobee",
      str_detect(tournament_name, "Oahe") ~ "Lake Oahe",
      str_detect(tournament_name, "Pickwick") ~ "Pickwick Lake",
      str_detect(tournament_name, "Martin") ~ "Lake Martin",
      str_detect(tournament_name, "Wheeler") ~ "Wheeler Lake",
      str_detect(tournament_name, "Toledo Bend") ~ "Toledo Bend",
      str_detect(tournament_name, "Champlain") ~ "Lake Champlain",
      str_detect(tournament_name, "Sabine") ~ "Sabine River",
      str_detect(tournament_name, "Mississippi River") ~ "Mississippi River",
      str_detect(tournament_name, "Potomac") ~ "Potomac River",
      str_detect(tournament_name, "Chesapeake") ~ "Chesapeake Bay",
      str_detect(tournament_name, "Winyah") ~ "Winyah Bay",
      str_detect(tournament_name, "Cayuga") ~ "Cayuga Lake",
      str_detect(tournament_name, "Lay Lake") ~ "Lay Lake",
      str_detect(tournament_name, "Smith Lake") ~ "Smith Lake",
      str_detect(tournament_name, "Harris Chain") ~ "Harris Chain",
      str_detect(tournament_name, "West Point") ~ "West Point Lake",
      
      TRUE ~ NA_character_
    )
  )

table(is.na(bass$fishery))

bass %>%
  filter(is.na(fishery)) %>%
  distinct(tournament_name) %>%
  arrange(tournament_name)


bass %>%
  group_by(year) %>%
  summarise(
    tournaments = n_distinct(tournament_name)
  )

bass <- bass %>%
  filter(weight_oz >= 0)

bass %>%
  filter(is.na(fishery)) %>%
  count(tournament_name, sort = TRUE)

bass %>%
  filter(tournament_name == "Douglas Lake Challenge") %>%
  select(year, tournament_name) %>%
  distinct()

bass %>%
  filter(is.na(fishery)) %>%
  count(tournament_name, sort = TRUE) %>%
  print(n = 60)

bass <- bass %>%
  mutate(
    fishery = case_when(
      is.na(fishery) & str_detect(tournament_name, "St\\. Johns|St\\. John’s") ~ "St. Johns River",
      is.na(fishery) & str_detect(tournament_name, "Lanier") ~ "Lake Lanier",
      is.na(fishery) & str_detect(tournament_name, "Tenkiller") ~ "Lake Tenkiller",
      is.na(fishery) & str_detect(tournament_name, "Cherokee") ~ "Lake Cherokee",
      is.na(fishery) & str_detect(tournament_name, "Dardanelle") ~ "Lake Dardanelle",
      is.na(fishery) & str_detect(tournament_name, "Ross Barnett") ~ "Ross Barnett Reservoir",
      is.na(fishery) & str_detect(tournament_name, "Santee Cooper") ~ "Santee Cooper",
      TRUE ~ fishery
    )
  )

table(is.na(bass$fishery))

bass <- bass %>%
  mutate(weight_lb = weight_oz / 16)

summary(bass$weight_lb)

bass <- bass %>%
  mutate(
    fishery = case_when(
      is.na(fishery) & str_detect(tournament_name, "Lake Havasu") ~ "Lake Havasu",
      is.na(fishery) & str_detect(tournament_name, "Sacramento River") ~ "Sacramento River",
      is.na(fishery) & str_detect(tournament_name, "Kentucky Lake") ~ "Kentucky Lake",
      is.na(fishery) & str_detect(tournament_name, "Table Rock") ~ "Table Rock Lake",
      is.na(fishery) & str_detect(tournament_name, "Bull Shoals") ~ "Bull Shoals/Norfork",
      is.na(fishery) & str_detect(tournament_name, "Grand Lake") ~ "Grand Lake",
      is.na(fishery) & str_detect(tournament_name, "Pasquotank") ~ "Pasquotank River",
      is.na(fishery) & str_detect(tournament_name, "Arkansas River") ~ "Arkansas River",
      is.na(fishery) & str_detect(tournament_name, "Tennessee River") ~ "Tennessee River",
      is.na(fishery) & str_detect(tournament_name, "Tennessee-Tombigbee") ~ "Tennessee-Tombigbee Waterway",
      is.na(fishery) & str_detect(tournament_name, "Neely Henry") ~ "Neely Henry Lake",
      is.na(fishery) & str_detect(tournament_name, "Chickamauga") ~ "Chickamauga Lake",
      is.na(fishery) & str_detect(tournament_name, "Eufaula") ~ "Lake Eufaula",
      
      TRUE ~ fishery
    )
  )

table(is.na(bass$fishery))

write_csv(
  bass,
  "bass_cleaned.csv"
)

bass %>%
  filter(!is.na(fishery)) %>%
  count(fishery, sort = TRUE)

bass %>%
  filter(!is.na(fishery)) %>%
  group_by(fishery) %>%
  summarise(
    years = n_distinct(year),
    tournaments = n_distinct(tournament_name)
  ) %>%
  arrange(desc(years))

fishery_year <- bass %>%
  filter(!is.na(fishery)) %>%
  group_by(fishery, year) %>%
  summarise(
    mean_weight_oz = mean(weight_oz, na.rm = TRUE),
    winner_weight_oz = max(weight_oz, na.rm = TRUE),
    mean_fish = mean(fish, na.rm = TRUE),
    n_anglers = n(),
    .groups = "drop"
  )

library(ggplot2)

fishery_year %>%
  filter(fishery %in% c(
    "St. Lawrence River",
    "Lake Champlain",
    "Lake Guntersville",
    "Lake Fork"
  )) %>%
  ggplot(
    aes(
      x = year,
      y = winner_weight_oz,
      color = fishery
    )
  ) +
  geom_line() +
  geom_point() +
  theme_minimal()

tournaments = unique(bass$tournament_name)
tournaments
str(bass)

bass <- bass %>%
  mutate(
    tech_era = case_when(
      year <= 2018 ~ "Pre-LiveScope",
      year <= 2020 ~ "Transition",
      TRUE ~ "LiveScope Era"
    )
  )

tournaments = unique(bass$tournament_name) 


tournaments = bass %>%
  distinct(tech_era, tournament_name) %>%
  arrange(tech_era, tournament_name) %>%
  print(n = 180)

write_csv(
  tournaments,
  "tournaments.csv"
)

# Updated ####
library(tidyverse)

setwd("~/Library/CloudStorage/OneDrive-AuburnUniversity/Auburn/School/Grad_School/Current/Data Mining/Bass Project")

bass <- read_csv("/Users/joshuaetherton/Library/CloudStorage/OneDrive-AuburnUniversity/Auburn/School/Grad_School/Current/Data Mining/Bass Project/bassmaster_output/bassmaster_complete_participant_records.csv")

bass %>%
  group_by(Season_Year) %>%
  summarise(
    tournaments = n_distinct(Event_Name)
  )

bass %>%
  group_by(Event_Name) %>%
  summarise(
    tournaments = n_distinct(Season_Year)
  ) %>%
  print(n = 180)

tournaments = unique(bass$Event_Name)

str(bass)

## 1. Distribution of Tournament Weights ####
# This tells you whether weights are roughly normal, skewed, bimodal, etc.
ggplot(bass, aes(x = Weight_Lbs_Calculated)) +
  geom_histogram(bins = 40, fill = "steelblue", color = "white") +
  labs(
    title = "Distribution of Catch Weights",
    x = "Weight (lb)",
    y = "Count"
  ) +
  theme_minimal()

## 2. Distribution of Fish Caught ####
ggplot(bass, aes(x = Fish_Caught)) +
  geom_histogram(binwidth = 1,
                 fill = "forestgreen",
                 color = "white") +
  labs(
    title = "Distribution of Fish Caught",
    x = "Fish Caught",
    y = "Count"
  ) +
  theme_minimal()

## 3. Weight vs Number of Fish ####
# Probably the single most informative exploratory plot.
ggplot(bass,
       aes(x = Fish_Caught,
           y = Weight_Lbs_Calculated)) +
  geom_point(alpha = 0.2) +
  geom_smooth(method = "loess",
              se = FALSE,
              color = "red") +
  labs(
    title = "Catch Weight vs Fish Caught",
    x = "Fish Caught",
    y = "Weight (lb)"
  ) +
  theme_minimal()

## 4. Weight by Place ####
ggplot(bass,
       aes(x = Place,
           y = Weight_Lbs_Calculated)) +
  geom_point(alpha = 0.1) +
  geom_smooth(se = FALSE,
              color = "blue") +
  labs(
    title = "Catch Weight by Tournament Finish",
    x = "Place",
    y = "Weight (lb)"
  ) +
  theme_minimal()

## 5. Winning Weights Over Time ####
# Just winners:
bass %>%
  filter(Place == 1) %>%
  ggplot(aes(x = Season_Year,
             y = Weight_Lbs_Calculated)) +
  geom_point() +
  geom_smooth(se = FALSE) +
  labs(
    title = "Winning Weights Through Time",
    x = "Year",
    y = "Winning Weight (lb)"
  ) +
  theme_minimal()

## 6. Variation Among Tournaments ####
# Tough fisheries, Productive fisheries, Tournaments with unusually high variation
bass %>%
  ggplot(aes(x = reorder(Event_Name,
                         Weight_Lbs_Calculated,
                         median),
             y = Weight_Lbs_Calculated)) +
  geom_boxplot() +
  coord_flip() +
  labs(
    title = "Catch Weight Distribution by Tournament",
    x = "",
    y = "Weight (lb)"
  ) +
  theme_minimal()

## 7. Average Fish Size ####
bass <- bass %>%
  mutate(
    Avg_Fish_Weight =
      Weight_Lbs_Calculated / Fish_Caught
  )

ggplot(bass,
       aes(x = Avg_Fish_Weight)) +
  geom_histogram(bins = 40,
                 fill = "orange",
                 color = "white") +
  labs(
    title = "Distribution of Average Fish Size",
    x = "Average Weight per Fish (lb)",
    y = "Count"
  ) +
  theme_minimal()

## Summary Table ####
bass %>%
  summarise(
    n = n(),
    min_weight = min(Weight_Lbs_Calculated, na.rm = TRUE),
    mean_weight = mean(Weight_Lbs_Calculated, na.rm = TRUE),
    median_weight = median(Weight_Lbs_Calculated, na.rm = TRUE),
    max_weight = max(Weight_Lbs_Calculated, na.rm = TRUE),
    min_fish = min(Fish_Caught, na.rm = TRUE),
    mean_fish = mean(Fish_Caught, na.rm = TRUE),
    median_fish = median(Fish_Caught, na.rm = TRUE),
    max_fish = max(Fish_Caught, na.rm = TRUE)
  )

## Average Fish Weight Over Time ####
library(dplyr)
library(ggplot2)

bass <- bass %>%
  mutate(
    Avg_Fish_Weight = Weight_Lbs_Calculated / Fish_Caught
  )

avg_fish_year <- bass %>%
  filter(Fish_Caught > 0) %>%
  group_by(Season_Year) %>%
  summarize(
    Avg_Fish_Weight = mean(Avg_Fish_Weight, na.rm = TRUE)
  )

ggplot(avg_fish_year,
       aes(x = Season_Year,
           y = Avg_Fish_Weight)) +
  geom_line(linewidth = 1) +
  geom_point(size = 2) +
  labs(
    title = "Average Fish Weight Over Time",
    x = "Year",
    y = "Average Fish Weight (lb/fish)"
  ) +
  theme_minimal()

ggplot(
  bass %>% filter(Fish_Caught > 0),
  aes(x = factor(Season_Year),
      y = Avg_Fish_Weight)
) +
  geom_boxplot() +
  labs(
    title = "Average Fish Weight by Year",
    x = "Year",
    y = "Average Fish Weight (lb/fish)"
  ) +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1)
  )

## Average Fish Weight of Top Ten Over Time ####
library(dplyr)
library(ggplot2)

top10 <- bass %>%
  filter(Place <= 10,
         Fish_Caught > 0) %>%
  mutate(
    Avg_Fish_Weight = Weight_Lbs_Calculated / Fish_Caught
  )

avg_fish_year_top10 <- top10 %>%
  group_by(Season_Year) %>%
  summarize(
    Avg_Fish_Weight = mean(Avg_Fish_Weight, na.rm = TRUE)
  )

ggplot(avg_fish_year_top10,
       aes(x = Season_Year,
           y = Avg_Fish_Weight)) +
  geom_line(linewidth = 1) +
  geom_point(size = 2) +
  labs(
    title = "Average Fish Weight Over Time (Top 10 Finishers)",
    x = "Year",
    y = "Average Fish Weight (lb/fish)"
  ) +
  theme_minimal()

avg_fish_year_top10 <- top10 %>%
  group_by(Season_Year) %>%
  summarize(
    mean_weight = mean(Avg_Fish_Weight, na.rm = TRUE),
    sd_weight = sd(Avg_Fish_Weight, na.rm = TRUE)
  )

ggplot(avg_fish_year_top10,
       aes(x = Season_Year, y = mean_weight)) +
  geom_ribbon(
    aes(ymin = mean_weight - sd_weight,
        ymax = mean_weight + sd_weight),
    alpha = 0.2
  ) +
  geom_line(linewidth = 1) +
  geom_point(size = 2) +
  labs(
    title = "Average Fish Weight by Year (Top 10 Finishers)",
    x = "Year",
    y = "Average Fish Weight (lb/fish)"
  ) +
  theme_minimal()

top10 %>%
  group_by(Season_Year, Tournament_ID, Event_Name) %>%
  summarize(
    Avg_Fish_Weight = mean(Avg_Fish_Weight, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  ggplot(aes(x = Season_Year, y = Avg_Fish_Weight)) +
  geom_jitter(width = 0.2, alpha = 0.5) +
  geom_smooth(se = FALSE, color = "red") +
  labs(
    title = "Tournament-Level Average Fish Weight (Top 10 Finishers)",
    x = "Year",
    y = "Average Fish Weight (lb/fish)"
  ) +
  theme_minimal()

# Analysis ####
## 1. Average Fish Weight Over Time, Colored by FFS Status ####
bass %>%
  filter(
    Place <= 10,
    Fish_Caught > 0
  ) %>%
  mutate(
    Avg_Fish_Weight = Weight_Lbs_Calculated / Fish_Caught
  ) %>%
  group_by(Season_Year, Allowed_FFS) %>%
  summarize(
    Avg_Fish_Weight = mean(Avg_Fish_Weight, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  ggplot(aes(
    x = Season_Year,
    y = Avg_Fish_Weight,
    color = Allowed_FFS
  )) +
  geom_line(linewidth = 1) +
  geom_point() +
  labs(
    title = "Average Fish Weight Over Time by FFS Status",
    x = "Year",
    y = "Average Fish Weight (lb/fish)",
    color = "FFS Status"
  ) +
  theme_minimal()

## 2. Distribution of Average Fish Weight by FFS Category ####
bass %>%
  filter(
    Place <= 10,
    Fish_Caught > 0
  ) %>%
  mutate(
    Avg_Fish_Weight = Weight_Lbs_Calculated / Fish_Caught
  ) %>%
  ggplot(aes(
    x = Allowed_FFS,
    y = Avg_Fish_Weight
  )) +
  geom_boxplot() +
  labs(
    title = "Average Fish Weight by FFS Status",
    x = "FFS Status",
    y = "Average Fish Weight (lb/fish)"
  ) +
  theme_minimal() +
  coord_flip()

## 3. Top-10 Tournament Average Fish Weight by Year ####
# Sometimes yearly averages hide a lot of variation.
bass %>%
  filter(
    Place <= 10,
    Fish_Caught > 0
  ) %>%
  mutate(
    Avg_Fish_Weight = Weight_Lbs_Calculated / Fish_Caught
  ) %>%
  group_by(
    Season_Year,
    Tournament_ID,
    Allowed_FFS
  ) %>%
  summarize(
    Avg_Fish_Weight = mean(Avg_Fish_Weight),
    .groups = "drop"
  ) %>%
  ggplot(aes(
    x = Season_Year,
    y = Avg_Fish_Weight,
    color = Allowed_FFS
  )) +
  geom_jitter(width = 0.25, alpha = 0.6) +
  geom_smooth(se = FALSE) +
  labs(
    title = "Tournament-Level Average Fish Weight",
    x = "Year",
    y = "Average Fish Weight (lb/fish)"
  ) +
  theme_minimal()

## 4. Total Catch Weight of Top 10 by Year ####
bass %>%
  filter(Place <= 10) %>%
  group_by(
    Season_Year,
    Allowed_FFS
  ) %>%
  summarize(
    Avg_Weight = mean(Weight_Lbs_Calculated),
    .groups = "drop"
  ) %>%
  ggplot(aes(
    x = Season_Year,
    y = Avg_Weight,
    color = Allowed_FFS
  )) +
  geom_line(linewidth = 1) +
  geom_point() +
  labs(
    title = "Average Top-10 Catch Weight Over Time",
    x = "Year",
    y = "Average Catch Weight (lb)"
  ) +
  theme_minimal()

## 5. Fish Caught by FFS Status ####
# # 
# # This helps distinguish whether anglers are catching:
# # more fish
# # bigger fish
# # or both
# bass %>%
#   filter(Place <= 10) %>%
#   ggplot(aes(
#     x = Allowed_FFS,
#     y = Fish_Caught
#   )) +
#   geom_boxplot() +
#   labs(
#     title = "Fish Caught by Top-10 Anglers",
#     x = "FFS Status",
#     y = "Number of Fish"
#   ) +
#   theme_minimal() +
#   coord_flip()

## 6. Average Fish Weight Over Time By FFS Allowance ####
bass %>%
  filter(
    Place <= 10,
    Fish_Caught > 0
  ) %>%
  mutate(
    Avg_Fish_Weight = Weight_Lbs_Calculated /
      Fish_Caught
  ) %>%
  ggplot(aes(
    x = Season_Year,
    y = Avg_Fish_Weight,
    color = Allowed_FFS
  )) +
  geom_jitter(
    width = 0.2,
    alpha = 0.3
  ) +
  geom_smooth(
    se = TRUE,
    linewidth = 1.2
  ) +
  labs(
    title = "Top-10 Average Fish Weight Through Time",
    x = "Year",
    y = "Average Fish Weight (lb/fish)"
  ) +
  theme_minimal()

## Identify Waters With Both Eras
Common_Waters <- bass %>%
  distinct(Location, Allowed_FFS) %>%
  count(Location) %>%
  arrange(desc(n))

Common_Waters %>% print(n = 76)

# common_waters <- bass %>%
#   group_by(Location) %>%
#   summarise(
#     n_ffs_states = n_distinct(Allowed_FFS)
#   ) %>%
#   filter(n_ffs_states > 1) %>%
#   pull(Location)

## 7. Compare Top-10 Average Fish Weight ####
bass %>%
  filter(
    Location %in% common_waters,
    # Place <= 10,
    Fish_Caught > 0
  ) %>%
  mutate(
    Avg_Fish_Weight = Weight_Lbs_Calculated / Fish_Caught
  ) %>%
  ggplot(
    aes(
      x = Allowed_FFS,
      y = Avg_Fish_Weight
    )
  ) +
  geom_boxplot() +
  facet_wrap(~ Location, scales = "free_y") +
  labs(
    title = "Top-10 Average Fish Weight by Water Body",
    x = "FFS Status",
    y = "Average Fish Weight (lb/fish)"
  ) +
  theme_minimal()


location_summary <- bass %>%
  filter(
    # Place <= 10,
    Fish_Caught > 0
  ) %>%
  mutate(
    Avg_Fish_Weight = Weight_Lbs_Calculated / Fish_Caught
  ) %>%
  group_by(Location, Allowed_FFS) %>%
  summarise(
    Mean_Fish_Weight = mean(Avg_Fish_Weight),
    .groups = "drop"
  )

ggplot(
  location_summary,
  aes(
    x = Allowed_FFS,
    y = Mean_Fish_Weight,
    group = Location
  )
) +
  geom_line(alpha = 0.5) +
  geom_point(size = 2) +
  labs(
    title = "Change in Average Fish Weight Within Water Bodies",
    x = "FFS Status",
    y = "Average Fish Weight (lb/fish)"
  ) +
  theme_minimal()

# Add Season ####
library(stringr)

bass <- bass %>%
  mutate(
    Month = str_extract(Tournament_Dates,
                        "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec")
  )

tourn_summary <- bass %>%
  filter(
    # Place <= 10,
    Fish_Caught > 0
  ) %>%
  mutate(
    Avg_Fish_Weight = Weight_Lbs_Calculated / Fish_Caught
  ) %>%
  group_by(
    Tournament_ID,
    Event_Name,
    Location,
    Month,
    Allowed_FFS,
    Season_Year
  ) %>%
  summarize(
    Mean_Fish_Weight = mean(Avg_Fish_Weight),
    Mean_Catch_Weight = mean(Weight_Lbs_Calculated),
    Mean_Fish_Caught = mean(Fish_Caught),
    .groups = "drop"
  )

comparison_lakes <- tourn_summary %>%
  group_by(Location) %>%
  summarize(
    n_eras = n_distinct(Allowed_FFS)
  ) %>%
  filter(n_eras > 1) %>%
  pull(Location)

tourn_summary2 <- tourn_summary %>%
  filter(Location %in% comparison_lakes)

ggplot(
  tourn_summary2,
  aes(
    x = Allowed_FFS,
    y = Mean_Fish_Weight
  )
) +
  geom_boxplot() +
  facet_wrap(~ Location) +
  theme_minimal()

ggplot(
  tourn_summary2,
  aes(
    x = Allowed_FFS,
    y = Mean_Fish_Weight
  )
) +
  geom_boxplot() +
  facet_grid(
    Month ~ Location,
    scales = "free_y"
  ) +
  theme_minimal()

paired <- tourn_summary %>%
  group_by(
    Location,
    Month,
    Allowed_FFS
  ) %>%
  summarize(
    Mean_Fish_Weight = mean(Mean_Fish_Weight),
    .groups = "drop"
  )

ggplot(
  paired,
  aes(
    x = Allowed_FFS,
    y = Mean_Fish_Weight,
    group = interaction(Location, Month)
  )
) +
  geom_line(alpha = 0.4) +
  geom_point(size = 2) +
  theme_minimal() +
  labs(
    title = "Average Fish Weight Within Location-Month Pairs",
    x = "FFS Status",
    y = "Average Fish Weight (lb/fish)"
  )

paired2 <- paired %>%
  filter(Allowed_FFS != "Unknown") %>%
  mutate(
    FFS_Group = case_when(
      Allowed_FFS == "No FFS Existed" ~ "Pre-FFS",
      Allowed_FFS == "No" ~ "FFS Not Allowed",
      Allowed_FFS %in% c("Yes (Restricted)",
                         "Yes (Unrestricted)") ~ "FFS Allowed"
    )
  )

paired_wide <- paired2 %>%
  group_by(Location, Month, FFS_Group) %>%
  summarize(
    Mean_Fish_Weight = mean(Mean_Fish_Weight),
    .groups = "drop"
  ) %>%
  tidyr::pivot_wider(
    names_from = FFS_Group,
    values_from = Mean_Fish_Weight
  )

paired_wide <- paired_wide %>%
  mutate(
    Difference = `FFS Allowed` - `Pre-FFS`
  )

ggplot(paired_wide,
       aes(x = Difference)) +
  geom_histogram(
    bins = 15,
    fill = "steelblue",
    color = "white"
  ) +
  geom_vline(
    xintercept = 0,
    linetype = "dashed",
    color = "red"
  ) +
  theme_minimal() +
  labs(
    title = "Change in Average Fish Weight After FFS",
    x = "Difference (lb/fish)",
    y = "Count"
  )

paired2 %>%
  count(Location, Month, FFS_Group) %>%
  tidyr::pivot_wider(
    names_from = FFS_Group,
    values_from = n,
    values_fill = 0
  ) %>% print(n = 120)

bass %>%
  count(Location, sort = TRUE) %>% print(n = 120)

library(dplyr)
library(stringr)

bass <- bass %>%
  mutate(
    Waterbody = case_when(
      
      # Guntersville
      str_detect(Location,
                 "Scottsboro|Guntersville|Lake Guntersville|Gadsden|Cullman") ~
        "Lake Guntersville",
      
      # St. Lawrence River
      str_detect(Location,
                 "Waddington|Clayton|St\\. Lawrence River") ~
        "St. Lawrence River",
      
      # Champlain
      str_detect(Location,
                 "Plattsburgh|Burlington") ~
        "Lake Champlain",
      
      # St. Johns
      str_detect(Location,
                 "Palatka|St\\. Johns River") ~
        "St. Johns River",
      
      # Okeechobee
      str_detect(Location,
                 "Okeechobee|Lake Okeechobee") ~
        "Lake Okeechobee",
      
      # Hartwell
      str_detect(Location,
                 "Anderson|Lake Hartwell") ~
        "Lake Hartwell",
      
      # Grand Lake
      str_detect(Location,
                 "Grand Lake") ~
        "Grand Lake",
      
      # Toledo Bend
      str_detect(Location,
                 "Many, LA") ~
        "Toledo Bend Reservoir",
      
      # Sabine
      str_detect(Location,
                 "Orange, TX|Sabine River") ~
        "Sabine River",
      
      # Mississippi River
      str_detect(Location,
                 "La Crosse|Mississippi River") ~
        "Mississippi River",
      
      # Lake Fork
      str_detect(Location,
                 "Yantis|Quitman") ~
        "Lake Fork",
      
      # Wheeler Lake
      str_detect(Location,
                 "Decatur, AL") ~
        "Wheeler Lake",
      
      # Pickwick
      str_detect(Location,
                 "Florence, AL|Counce, TN") ~
        "Pickwick Lake",
      
      # Lake Murray
      str_detect(Location,
                 "Columbia, SC|Prosperity, SC") ~
        "Lake Murray",
      
      # Santee Cooper
      str_detect(Location,
                 "Clarendon County|Manning, SC") ~
        "Santee Cooper",
      
      # Lake Eufaula
      str_detect(Location,
                 "Eufaula, AL") ~
        "Lake Eufaula",
      
      # Oneida
      str_detect(Location,
                 "Union Springs|Oneida Lake") ~
        "Oneida Lake",
      
      # Chickamauga
      str_detect(Location,
                 "Dayton, TN") ~
        "Lake Chickamauga",
      
      # Douglas
      str_detect(Location,
                 "Jefferson City|Douglas Lake") ~
        "Douglas Lake",
      
      # Cherokee
      str_detect(Location,
                 "Alexander City") ~
        "Lake Martin",
      
      # Potomac
      str_detect(Location,
                 "Charles County|Cecil County") ~
        "Potomac River",
      
      # St Clair
      str_detect(Location,
                 "Macomb County|Detroit") ~
        "Lake St. Clair",
      
      # Tennessee River Knoxville events
      str_detect(Location,
                 "Knoxville|Tennessee River") ~
        "Tennessee River (Knoxville)",
      
      # Generic unknown
      Location == "Unknown Location" ~
        "Unknown",
      
      TRUE ~ Location
    )
  )

bass %>%
  count(Waterbody, sort = TRUE) %>%
  print(n = Inf)

bass %>%
  filter(Allowed_FFS != "Unknown") %>%
  distinct(Waterbody, Allowed_FFS) %>%
  count(Waterbody) %>%
  arrange(desc(n))

bass %>%
  filter(Allowed_FFS != "Unknown") %>%
  group_by(Waterbody) %>%
  summarize(
    FFS_Categories = paste(sort(unique(Allowed_FFS)),
                           collapse = ", "),
    n_tournaments = n_distinct(Tournament_ID)
  ) %>%
  arrange(desc(n_tournaments)) %>%
  print(n = Inf)

tourn <- bass %>%
  filter(
    # Place <= 10,
    Fish_Caught > 0,
    Allowed_FFS != "Unknown"
  ) %>%
  mutate(
    Avg_Fish_Weight = Weight_Lbs_Calculated / Fish_Caught
  ) %>%
  group_by(
    Tournament_ID,
    Season_Year,
    Waterbody,
    Allowed_FFS
  ) %>%
  summarize(
    Mean_Fish_Weight = mean(Avg_Fish_Weight),
    Mean_Catch_Weight = mean(Weight_Lbs_Calculated),
    Mean_Fish_Caught = mean(Fish_Caught),
    .groups = "drop"
  )

### Plot 1: Average fish weight by fishery and FFS status ####
ggplot(
  tourn,
  aes(
    x = Allowed_FFS,
    y = Mean_Fish_Weight
  )
) +
  geom_point(size = 3) +
  facet_wrap(~ Waterbody, scales = "free_y") +
  theme_minimal() +
  labs(
    title = "Average Fish Weight by Fishery",
    y = "Average Fish Weight (lb/fish)"
  )

### Plot 2: Paired change within waterbody ####
ffs_compare <- tourn %>%
  mutate(
    Era = case_when(
      Allowed_FFS == "No FFS Existed" ~ "Pre-FFS",
      Allowed_FFS == "No" ~ "FFS Banned",
      TRUE ~ "FFS Allowed"
    )
  ) %>%
  group_by(Waterbody, Era) %>%
  summarize(
    Mean_Fish_Weight = mean(Mean_Fish_Weight),
    .groups = "drop"
  )

ggplot(
  ffs_compare,
  aes(
    x = Era,
    y = Mean_Fish_Weight,
    group = Waterbody
  )
) +
  geom_line(alpha = 0.7) +
  geom_point(size = 3) +
  theme_minimal() +
  labs(
    title = "Change in Average Fish Weight Within Fisheries",
    y = "Average Fish Weight (lb/fish)"
  )

### Plot 3: Top-10 catch weight before and after FFS ####
ggplot(
  tourn,
  aes(
    x = Allowed_FFS,
    y = Mean_Catch_Weight
  )
) +
  geom_boxplot() +
  facet_wrap(~ Waterbody, scales = "free_y") +
  theme_minimal() +
  labs(
    title = "Top-10 Average Catch Weight",
    y = "Weight (lb)"
  )

diffs <- ffs_compare %>%
  filter(Era %in% c("Pre-FFS", "FFS Allowed")) %>%
  tidyr::pivot_wider(
    names_from = Era,
    values_from = Mean_Fish_Weight
  ) %>%
  mutate(
    Difference = `FFS Allowed` - `Pre-FFS`
  ) %>%
  arrange(desc(Difference))

print(diffs) %>%
  print(n = Inf)

library(ggplot2)

diffs %>%
  filter(!is.na(Difference)) %>%
  ggplot(aes(
    x = reorder(Waterbody, Difference),
    y = Difference,
    fill = Difference > 0
  )) +
  geom_col() +
  coord_flip() +
  geom_hline(
    yintercept = 0,
    linetype = "dashed",
    color = "red"
  ) +
  labs(
    title = "Change in Average Fish Weight\n(FFS Era - Pre-FFS Era)",
    x = "",
    y = "Difference (lb/fish)"
  ) +
  theme_minimal() +
  theme(
    legend.position = "none"
  )

tourn %>%
  filter(
    Waterbody %in% c(
      "Lake Guntersville",
      "St. Lawrence River",
      "Lake Okeechobee",
      "Toledo Bend Reservoir"
    )
  ) %>%
  arrange(Waterbody, Season_Year)

tourn %>%
  filter(
    Waterbody %in% (
      diffs |>
        dplyr::filter(!is.na(Difference)) |>
        dplyr::pull(Waterbody)
    )
  ) %>%
  ggplot(
    aes(
      x = Season_Year,
      y = Mean_Fish_Weight,
      color = Allowed_FFS
    )
  ) +
  geom_point(size = 3) +
  geom_line(aes(group = 1)) +
  facet_wrap(~ Waterbody, scales = "free_y") +
  theme_minimal()

matched_waterbodies <- diffs %>%
  filter(!is.na(Difference)) %>%
  pull(Waterbody)

matched_waterbodies

ggplot(
  tourn %>% filter(Waterbody %in% matched_waterbodies),
  aes(
    Season_Year,
    Mean_Fish_Weight
  )
) +
  geom_line(color = "grey60") +
  geom_point(
    aes(color = Allowed_FFS),
    size = 3
  ) +
  facet_wrap(~ Waterbody, scales = "free_y") +
  theme_minimal() +
  labs(
    title = "Tournament-Level Average Fish Weight Through Time",
    x = "Year",
    y = "Average Fish Weight (lb/fish)"
  )

matched_waterbodies <- diffs %>%
  filter(
    !is.na(`Pre-FFS`),
    !is.na(`FFS Allowed`)
  ) %>%
  pull(Waterbody)

diffs %>%
  filter(
    !is.na(`Pre-FFS`),
    !is.na(`FFS Allowed`)
  ) %>%
  ggplot(
    aes(
      x = reorder(Waterbody, Difference),
      y = Difference,
      fill = Difference > 0
    )
  ) +
  geom_col() +
  coord_flip() +
  geom_hline(
    yintercept = 0,
    linetype = "dashed"
  ) +
  labs(
    title = "Change in Average Fish Weight After FFS",
    x = "",
    y = "FFS - Pre-FFS (lb/fish)"
  ) +
  theme_minimal() +
  theme(
    legend.position = "none"
  )

ggplot(
  tourn,
  aes(
    Season_Year,
    Mean_Fish_Weight,
    color = Allowed_FFS
  )
) +
  geom_point() +
  geom_smooth(se = FALSE) +
  facet_wrap(~ Waterbody)

tourn <- tourn %>%
  group_by(Waterbody) %>%
  mutate(
    Relative_Fish_Weight =
      Mean_Fish_Weight -
      mean(Mean_Fish_Weight, na.rm = TRUE)
  ) %>%
  ungroup()

ggplot(
  tourn,
  aes(
    Allowed_FFS,
    Relative_Fish_Weight
  )
) +
  geom_boxplot()

lm(
  Mean_Fish_Weight ~
    Allowed_FFS +
    Waterbody +
    Month,
  data = tourn
)


library(tidyr)
library(dplyr)

fisheries <- c(
  "Lake Guntersville",
  "Lake Okeechobee",
  "St. Johns River",
  "St. Lawrence River",
  "Lake Fork",
  "Toledo Bend Reservoir",
  "Mississippi River",
  "Oneida Lake",
  "Grand Lake",
  "Sabine River"
)

cpue_template <- expand_grid(
  Waterbody = fisheries,
  Year = 2026:2012
) %>%
  arrange(Waterbody, desc(Year)) %>%
  mutate(
    Spring_Total_CPUE = NA_real_,
    Spring_Total_CPUE_RSE = NA_real_,
    Spring_Stock_CPUE = NA_real_,
    Spring_Stock_CPUE_RSE = NA_real_,
    Fall_Total_CPUE = NA_real_,
    Fall_Total_CPUE_RSE = NA_real_,
    Fall_Stock_CPUE = NA_real_,
    Fall_Stock_CPUE_RSE = NA_real_,
    Source = "",
    Notes = ""
  )

write.csv(
  cpue_template,
  "fishery_cpue_template.csv",
  row.names = FALSE
)

head(cpue_template)


# 1. Basic summaries ####
library(dplyr)

bass %>%
  summarize(
    n_obs = n(),
    n_tournaments = n_distinct(Tournament_ID),
    n_years = n_distinct(Season_Year),
    n_anglers = n_distinct(Player_ID),
    n_waterbodies = n_distinct(Waterbody),
    
    mean_weight = mean(Weight_Lbs_Calculated, na.rm = TRUE),
    median_weight = median(Weight_Lbs_Calculated, na.rm = TRUE),
    
    mean_fish = mean(Fish_Caught, na.rm = TRUE),
    median_fish = median(Fish_Caught, na.rm = TRUE)
  )

# 2. Weight distribution ####
ggplot(bass, aes(Weight_Lbs_Calculated)) +
  geom_histogram(bins = 40) +
  theme_minimal() +
  labs(
    title = "Distribution of Tournament Weights",
    x = "Weight (lb)"
  )

# 3. Fish caught distribution ####
ggplot(bass, aes(Fish_Caught)) +
  geom_histogram(binwidth = 1) +
  theme_minimal()

# 4. Average fish weight ####
bass <- bass %>%
  mutate(
    Avg_Fish_Weight =
      Weight_Lbs_Calculated / Fish_Caught
  )

ggplot(
  bass %>% filter(Fish_Caught > 0),
  aes(Avg_Fish_Weight)
) +
  geom_histogram(bins = 30) +
  theme_minimal()

# 5. Weight vs fish caught ####
ggplot(
  bass %>% filter(Fish_Caught > 0),
  aes(
    Fish_Caught,
    Weight_Lbs_Calculated
  )
) +
  geom_point(alpha = 0.2) +
  geom_smooth() +
  theme_minimal()

# 6. Top-10 trends through time ####
bass %>%
  filter(
    Place <= 10,
    Fish_Caught > 0
  ) %>%
  group_by(Season_Year) %>%
  summarize(
    Mean_Fish_Weight =
      mean(Avg_Fish_Weight)
  ) %>%
  ggplot(
    aes(
      Season_Year,
      Mean_Fish_Weight
    )
  ) +
  geom_line() +
  geom_point() +
  theme_minimal()

# 7. Weight trends by FFS category ####
bass %>%
  filter(
    Place <= 10,
    Fish_Caught > 0
  ) %>%
  ggplot(
    aes(
      Season_Year,
      Avg_Fish_Weight,
      color = Allowed_FFS
    )
  ) +
  geom_jitter(alpha = 0.2) +
  geom_smooth(se = FALSE)

# 8. Which fisheries produce the biggest fish? ####
bass %>%
  filter(
    Place <= 10,
    Fish_Caught > 0
  ) %>%
  group_by(Waterbody) %>%
  summarize(
    Avg_Fish_Weight =
      mean(Avg_Fish_Weight),
    n = n()
  ) %>%
  filter(n > 50) %>%
  arrange(desc(Avg_Fish_Weight))

# 9. Which fisheries have changed most? ####
bass %>%
  filter(
    Place <= 10,
    Fish_Caught > 0
  ) %>%
  group_by(Waterbody, Season_Year) %>%
  summarize(
    Avg_Fish_Weight =
      mean(Avg_Fish_Weight),
    .groups = "drop"
  ) %>%
  ggplot(
    aes(
      Season_Year,
      Avg_Fish_Weight
    )
  ) +
  geom_line() +
  facet_wrap(
    ~ Waterbody,
    scales = "free_y"
  )

# 10. Correlation matrix ####
install.packages("GGally")
library(GGally)

bass %>%
  select(
    Weight_Lbs_Calculated,
    Fish_Caught,
    Place,
    Fantasy_Points
  ) %>%
  ggpairs()

bass %>%
  filter(
    Place <= 10,
    Fish_Caught > 0
  ) %>%
  ggplot(
    aes(
      x = Season_Year,
      y = Avg_Fish_Weight
    )
  ) +
  geom_boxplot(
    aes(group = Season_Year)
  )

tournament_summary <- bass %>%
  filter(
    Place <= 10,
    Fish_Caught > 0
  ) %>%
  group_by(
    Season_Year,
    Tournament_ID,
    Waterbody,
    Allowed_FFS
  ) %>%
  summarize(
    Mean_Fish_Weight =
      mean(Avg_Fish_Weight),
    Mean_Catch_Weight =
      mean(Weight_Lbs_Calculated),
    Mean_Fish_Caught =
      mean(Fish_Caught),
    .groups = "drop"
  )

str(tournament_summary)


tournament_dates <- unique(bass$Tournament_Dates)
tournament_dates
sum(is.na(bass$Tournament_Dates))
sum(bass$`Location` == "Unknown Location", na.rm = TRUE)

unique_events <- unique(bass[, c("Season_Year", "Event_Name")])
unique_events
str(unique_events)

missing_dates <- bass %>%
  filter(is.na(Tournament_Dates)) %>%
  distinct(Season_Year, Event_Name)

# To see the results:
print(missing_dates)

# Create the data frame with the missing tournament information
missing_tournaments_df <- data.frame(
  Season_Year = c(
    2013, 2013, 2014, 2014, 2014, 2015, 2015, 2016, 2017, 2017, 
    2017, 2017, 2018, 2018, 2019, 2019, 2019, 2020, 2021
  ),
  Event_Name = c(
    "Ramada Quest",
    "Plano Championship Chase",
    "Bassmaster Elite Series at St. Johns River",
    "Bassmaster BASSFest at Chickamauga Lake",
    "Bassmaster Elite Series AOY Championship",
    "Elite Series Tournament: Bassmaster BASSfest at Kentucky Lake",
    "Elite Series Tournament: Toyota Bassmaster AOY Championship",
    "2016 Toyota Bassmaster Angler of the Year Championship",
    "2017 GEICO Bassmaster Classic",
    "Bassmaster Elite at Toledo Bend",
    "Toyota Bassmaster Texas Fest",
    "Bassmaster Elite at St. Clair",
    "Berkley Bassmaster Elite at Kentucky Lake presented by Abu Garcia",
    "Toyota Bassmaster Texas Fest benefiting the Texas Parks and Wildlife Department",
    "2019 Bassmaster Elite at Cayuga Lake",
    "2019 Bassmaster Elite at Lake Tenkiller",
    "Toyota Bassmaster Angler of the Year Championship",
    "2020 Toyota Bassmaster Texas Fest",
    "2021 Academy Sports + Outdoors Bassmaster Classic presented by Huk"
  ),
  Location = c(
    "Bull Shoals, AR", "Detroit, MI", "Palatka, FL", "Dayton, TN", "Escanaba, MI",
    "Paris, TN", "Sturgeon Bay, WI", "Mille Lacs, MN", "Houston, TX", "Many, LA",
    "Lufkin, TX", "Macomb County, MI", "Paris, TN", "Jonestown, TX", "Union Springs, NY",
    "Cookson, OK", "Detroit, MI", "Quitman, TX", "Fort Worth, TX"
  ),
  Tournament_Dates = c(
    "April 19-22, 2013", "August 22-25, 2013", "March 20-23, 2014", "June 11-15, 2014", "September 18-21, 2014",
    "June 3-7, 2015", "September 17-20, 2015", "September 15-18, 2016", "March 24-26, 2017", "April 6-9, 2017",
    "May 17-21, 2017", "August 24-27, 2017", "May 4-7, 2018", "May 17-20, 2018", "August 22-25, 2019",
    "September 19-22, 2019", "September 28 - October 1, 2019", "November 5-8, 2020", "June 11-13, 2021"
  ),
  Forward_Facing_Sonar = c(
    "unavailable", "unavailable", "unavailable", "unavailable", "unavailable",
    "unavailable", "unavailable", "unavailable", "unavailable", "unavailable",
    "unavailable", "unavailable", "unavailable", "unavailable", "allowed",
    "allowed", "allowed", "allowed", "allowed"
  ),
  stringsAsFactors = FALSE
)

# View the newly created data frame structure
str(missing_tournaments_df)



# 1. Update the dataset using the proper joined suffixes (.x and .y)
bass_updated <- bass %>%
  left_join(missing_tournaments_df, by = c("Season_Year", "Event_Name")) %>%
  mutate(
    # Combine the original (.x) and new (.y) date columns
    Tournament_Dates = ifelse(is.na(Tournament_Dates.x) | Tournament_Dates.x == "NA", 
                              Tournament_Dates.y, 
                              Tournament_Dates.x),
    
    # Do the same for Location to fill in the missing cities/states
    Location = ifelse(is.na(Location.x) | Location.x == "Unknown Location", 
                      Location.y, 
                      Location.x),
    
    # Consolidate your FFS tracking into your existing column
    Allowed_FFS = ifelse(is.na(Allowed_FFS) | Allowed_FFS == "Unknown", 
                         Forward_Facing_Sonar, 
                         Allowed_FFS)
  ) %>%
  # 2. Clean up all the temporary leftover tracking columns
  select(-Tournament_Dates.x, -Tournament_Dates.y, -Location.x, -Location.y, -Forward_Facing_Sonar)

# 3. Overwrite the old object
bass <- bass_updated

# Rename the column back to Tournament_Dates
if("Tournament_Dates.x" %in% colnames(bass)) {
  bass <- bass %>% rename(Tournament_Dates = Tournament_Dates.x)
}

