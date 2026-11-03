install.packages("tidyverse")

library(tidyverse)
library(stringr)
library(dplyr)
library(tidyr)

# ============================================================================
# ORIGINAL FANTASY DATA CLEANING WORKFLOW
# ============================================================================

setwd("~/Library/CloudStorage/OneDrive-AuburnUniversity/Auburn/School/Grad_School/Current/Data Mining/Bass Project")

bass <- read_csv(
  "/Users/joshuaetherton/Library/CloudStorage/OneDrive-AuburnUniversity/Auburn/School/Grad_School/Current/Data Mining/Bass Project/bassmaster_fantasy_results.csv"
)

bass <- bass %>%
  mutate(
    place = as.numeric(place),
    fish = as.numeric(fish),
    weight_oz = as.numeric(weight_oz),
    fantasy_points = as.numeric(fantasy_points),
    year = as.numeric(year)
  )

bass <- bass %>%
  mutate(
    weight_lb = weight_oz / 16,
    weight_per_fish = weight_oz / fish
  )

bass <- bass %>%
  mutate(
    tournament_url =
      str_extract(
        tournament_url,
        "https://[^\\\">]+"
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

bass <- bass %>%
  filter(weight_oz >= 0)

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

bass <- bass %>%
  mutate(
    tech_era = case_when(
      year <= 2018 ~ "Pre-LiveScope",
      year <= 2020 ~ "Transition",
      TRUE ~ "LiveScope Era"
    )
  )

write_csv(bass, "bass_cleaned.csv")

# ============================================================================
# UPDATED PARTICIPANT RECORDS WORKFLOW
# ============================================================================

bass <- read_csv(
  "/Users/joshuaetherton/Library/CloudStorage/OneDrive-AuburnUniversity/Auburn/School/Grad_School/Current/Data Mining/Bass Project/bassmaster_output/bassmaster_complete_participant_records.csv"
)

bass <- bass %>%
  mutate(
    Avg_Fish_Weight = Weight_Lbs_Calculated / Fish_Caught
  )

bass <- bass %>%
  mutate(
    Month = str_extract(
      Tournament_Dates,
      "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec"
    )
  )

bass <- bass %>%
  mutate(
    Waterbody = case_when(
      
      str_detect(Location,
                 "Scottsboro|Guntersville|Lake Guntersville|Gadsden|Cullman") ~
        "Lake Guntersville",
      
      str_detect(Location,
                 "Waddington|Clayton|St\\. Lawrence River") ~
        "St. Lawrence River",
      
      str_detect(Location,
                 "Plattsburgh|Burlington") ~
        "Lake Champlain",
      
      str_detect(Location,
                 "Palatka|St\\. Johns River") ~
        "St. Johns River",
      
      str_detect(Location,
                 "Okeechobee|Lake Okeechobee") ~
        "Lake Okeechobee",
      
      str_detect(Location,
                 "Anderson|Lake Hartwell") ~
        "Lake Hartwell",
      
      str_detect(Location,
                 "Grand Lake") ~
        "Grand Lake",
      
      str_detect(Location,
                 "Many, LA") ~
        "Toledo Bend Reservoir",
      
      str_detect(Location,
                 "Orange, TX|Sabine River") ~
        "Sabine River",
      
      str_detect(Location,
                 "La Crosse|Mississippi River") ~
        "Mississippi River",
      
      str_detect(Location,
                 "Yantis|Quitman") ~
        "Lake Fork",
      
      str_detect(Location,
                 "Decatur, AL") ~
        "Wheeler Lake",
      
      str_detect(Location,
                 "Florence, AL|Counce, TN") ~
        "Pickwick Lake",
      
      str_detect(Location,
                 "Columbia, SC|Prosperity, SC") ~
        "Lake Murray",
      
      str_detect(Location,
                 "Clarendon County|Manning, SC") ~
        "Santee Cooper",
      
      str_detect(Location,
                 "Eufaula, AL") ~
        "Lake Eufaula",
      
      str_detect(Location,
                 "Union Springs|Oneida Lake") ~
        "Oneida Lake",
      
      str_detect(Location,
                 "Dayton, TN") ~
        "Lake Chickamauga",
      
      str_detect(Location,
                 "Jefferson City|Douglas Lake") ~
        "Douglas Lake",
      
      str_detect(Location,
                 "Alexander City") ~
        "Lake Martin",
      
      str_detect(Location,
                 "Charles County|Cecil County") ~
        "Potomac River",
      
      str_detect(Location,
                 "Macomb County|Detroit") ~
        "Lake St. Clair",
      
      str_detect(Location,
                 "Knoxville|Tennessee River") ~
        "Tennessee River (Knoxville)",
      
      Location == "Unknown Location" ~
        "Unknown",
      
      TRUE ~ Location
    )
  )

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
    "Bull Shoals, AR", "Detroit, MI", "Palatka, FL", "Dayton, TN",
    "Escanaba, MI", "Paris, TN", "Sturgeon Bay, WI", "Mille Lacs, MN",
    "Houston, TX", "Many, LA", "Lufkin, TX", "Macomb County, MI",
    "Paris, TN", "Jonestown, TX", "Union Springs, NY", "Cookson, OK",
    "Detroit, MI", "Quitman, TX", "Fort Worth, TX"
  ),
  Tournament_Dates = c(
    "April 19-22, 2013",
    "August 22-25, 2013",
    "March 20-23, 2014",
    "June 11-15, 2014",
    "September 18-21, 2014",
    "June 3-7, 2015",
    "September 17-20, 2015",
    "September 15-18, 2016",
    "March 24-26, 2017",
    "April 6-9, 2017",
    "May 17-21, 2017",
    "August 24-27, 2017",
    "May 4-7, 2018",
    "May 17-20, 2018",
    "August 22-25, 2019",
    "September 19-22, 2019",
    "September 28 - October 1, 2019",
    "November 5-8, 2020",
    "June 11-13, 2021"
  ),
  Forward_Facing_Sonar = c(
    "unavailable", "unavailable", "unavailable", "unavailable",
    "unavailable", "unavailable", "unavailable", "unavailable",
    "unavailable", "unavailable", "unavailable", "unavailable",
    "unavailable", "unavailable", "allowed", "allowed",
    "allowed", "allowed", "allowed"
  ),
  stringsAsFactors = FALSE
)

bass_updated <- bass %>%
  left_join(
    missing_tournaments_df,
    by = c("Season_Year", "Event_Name")
  ) %>%
  mutate(
    Tournament_Dates = ifelse(
      is.na(Tournament_Dates.x) | Tournament_Dates.x == "NA",
      Tournament_Dates.y,
      Tournament_Dates.x
    ),
    
    Location = ifelse(
      is.na(Location.x) | Location.x == "Unknown Location",
      Location.y,
      Location.x
    ),
    
    Allowed_FFS = ifelse(
      is.na(Allowed_FFS) | Allowed_FFS == "Unknown",
      Forward_Facing_Sonar,
      Allowed_FFS
    )
  ) %>%
  select(
    -Tournament_Dates.x,
    -Tournament_Dates.y,
    -Location.x,
    -Location.y,
    -Forward_Facing_Sonar
  )

bass <- bass_updated

if ("Tournament_Dates.x" %in% colnames(bass)) {
  bass <- bass %>%
    rename(Tournament_Dates = Tournament_Dates.x)
}

write_csv(
  bass,
  "bass_final_cleaned.csv"
)


# tournament_dates <- unique(bass$Tournament_Dates)
# tournament_dates
# sum(is.na(bass$Tournament_Dates))
# sum(bass$`Location` == "Unknown Location", na.rm = TRUE)
# 
# unique_events <- unique(bass[, c("Season_Year", "Event_Name")])
# unique_events
# str(unique_events)
# 
# missing_dates <- bass %>%
#   filter(is.na(Tournament_Dates)) %>%
#   distinct(Season_Year, Event_Name)
# 
# # To see the results:
# print(missing_dates)

unique_events <- unique(bass[, c("Season_Year", "Event_Name", "Waterbody", "Location")])
print(unique_events, n = 150)

bass_stand_loc <- read_csv(
  "/Users/joshuaetherton/Library/CloudStorage/OneDrive-AuburnUniversity/Auburn/School/Grad_School/Current/Data Mining/Bass Project/clean_bassmaster_events.csv"
)

library(dplyr)
library(stringr)

# Automatically standardize Event_Name without losing original row context
bass_clean <- bass %>%
  mutate(
    Event_Name = case_when(
      str_detect(Event_Name, "(?i)Classic") ~ "Bassmaster Classic",
      str_detect(Event_Name, "(?i)AOY|Angler of the Year") ~ "Angler of the Year Championship",
      str_detect(Event_Name, "(?i)Elite|Showdown|Slam|Quest|Challenge|Battle|Rumble|Championship|Chase|Charge|BASSfest|Texas Fest|Festival") ~ "Elite Series",
      TRUE ~ "Elite Series" # Fallback category for regular season events
    )
  )

bass_stand_loc_clean <- bass_stand_loc %>%
  mutate(
    Event_Name = case_when(
      str_detect(Event_Name, "(?i)Classic") ~ "Bassmaster Classic",
      str_detect(Event_Name, "(?i)AOY|Angler of the Year") ~ "Angler of the Year Championship",
      str_detect(Event_Name, "(?i)Elite|Showdown|Slam|Quest|Challenge|Battle|Rumble|Championship|Chase|Charge|BASSfest|Texas Fest|Festival") ~ "Elite Series",
      TRUE ~ "Elite Series" # Fallback category for regular season events
    )
  )

library(dplyr)

final_merged_bass <- bass_clean %>%
  left_join(
    bass_stand_loc_clean %>% 
      distinct(Season_Year, Waterbody, Location, .keep_all = TRUE), 
    by = c("Season_Year", "Waterbody", "Location")
  )

# Note: If your lookup table has different column names, map them explicitly:
# by = c("Season_Year" = "Season_Year", "Waterbody" = "Clean_Waterbody")


final_merged_bass <- bass_clean %>%
  left_join(
    bass_stand_loc_clean %>% 
      distinct(Season_Year, Event_Name, Waterbody, Location, .keep_all = TRUE), 
    by = c("Season_Year", "Event_Name", "Waterbody", "Location")
  )


library(dplyr)

# 1. Create the explicit 149-row clean dataset to match unique_events row-for-row
clean_149 <- tibble(
  clean_Event_Name = c(
    "Bassmaster Classic", "Elite Series", "Elite Series", "Elite Series", "Elite Series", 
    "Elite Series", "Elite Series", "Elite Series", "Elite Series", "Bassmaster Classic", 
    "Elite Series", "Elite Series", "Elite Series", "Elite Series", "Elite Series", 
    "Elite Series", "Elite Series", "Elite Series", "Bassmaster Classic", "Elite Series", 
    "Elite Series", "Elite Series", "Elite Series", "Elite Series", "Elite Series", 
    "Elite Series", "Angler of the Year Championship", "Bassmaster Classic", "Elite Series", "Elite Series", 
    "Elite Series", "Elite Series", "Elite Series", "Elite Series", "Elite Series", 
    "Elite Series", "Angler of the Year Championship", "Bassmaster Classic", "Elite Series", "Elite Series", 
    "Elite Series", "Elite Series", "Elite Series", "Elite Series", "Elite Series", 
    "Elite Series", "Elite Series", "Angler of the Year Championship", "Elite Series", "Bassmaster Classic", 
    "Elite Series", "Elite Series", "Elite Series", "Elite Series", "Elite Series", 
    "Elite Series", "Elite Series", "Angler of the Year Championship", "Elite Series", "Bassmaster Classic", 
    "Elite Series", "Elite Series", "Elite Series", "Elite Series", "Elite Series", 
    "Elite Series", "Elite Series", "Angler of the Year Championship", "Elite Series", "Elite Series", 
    "Elite Series", "Elite Series", "Elite Series", "Elite Series", "Elite Series", 
    "Elite Series", "Elite Series", "Elite Series", "Angler of the Year Championship", "Elite Series", 
    "Elite Series", "Elite Series", "Elite Series", "Elite Series", "Elite Series", 
    "Elite Series", "Elite Series", "Elite Series", "Elite Series", "Elite Series", 
    "Elite Series", "Elite Series", "Elite Series", "Elite Series", "Elite Series", 
    "Elite Series", "Bassmaster Classic", "Elite Series", "Elite Series", "Elite Series", 
    "Elite Series", "Bassmaster Classic", "Elite Series", "Elite Series", "Elite Series", 
    "Elite Series", "Elite Series", "Elite Series", "Elite Series", "Elite Series", 
    "Elite Series", "Bassmaster Classic", "Elite Series", "Elite Series", "Elite Series", 
    "Elite Series", "Elite Series", "Elite Series", "Elite Series", "Elite Series", 
    "Elite Series", "Bassmaster Classic", "Elite Series", "Elite Series", "Elite Series", 
    "Elite Series", "Elite Series", "Elite Series", "Elite Series", "Elite Series", 
    "Elite Series", "Bass Pro Shops Bassmaster Classic", "Elite Series", "Elite Series", "Elite Series", 
    "Elite Series", "Elite Series", "Elite Series", "Elite Series", "Elite Series", 
    "Elite Series", "Bass Pro Shops Bassmaster Classic", "Elite Series", "Elite Series", "Elite Series", 
    "Elite Series", "Elite Series", "Elite Series", "Elite Series"
  ),
  clean_Waterbody = c(
    "Red River", "St. Johns River", "Lake Okeechobee", "Bull Shoals Lake", "Douglas Lake", 
    "Toledo Bend Reservoir", "Mississippi River", "Green Bay", "Oneida Lake", "Grand Lake", 
    "Sabine River", "Falcon Lake", "Bull Shoals Lake", "West Point Lake", "Alabama River", 
    "Mississippi River", "St. Lawrence River", "Lake St. Clair / Detroit River", "Lake Guntersville", "Lake Seminole", 
    "St. Johns River", "Table Rock Lake", "Toledo Bend Reservoir", "Lake Dardanelle", "Chickamauga Lake", 
    "Cayuga Lake", "Little Bay de Noc", "Lake Hartwell", "Sabine River", "Lake Guntersville", 
    "Sacramento River", "Lake Havasu", "Kentucky Lake", "St. Lawrence River", "Chesapeake Bay / Potomac River", 
    "Lake St. Clair", "Green Bay", "Grand Lake", "St. Johns River", "Winyah Bay", 
    "Bull Shoals Lake / Norfork Lake", "Wheeler Lake", "Toledo Bend Reservoir", "Lake Texoma", "Cayuga Lake", 
    "Potomac River", "Mississippi River", "Mille Lacs Lake", "Cherokee Lake", "Lake Conroe", 
    "Toledo Bend Reservoir", "Ross Barnett Reservoir", "Sam Rayburn Reservoir", "Lake Dardanelle", "St. Lawrence River", 
    "Lake Champlain", "Lake St. Clair", "Mille Lacs Lake", "Lake Martin", "Lake Hartwell", 
    "Grand Lake", "Kentucky Lake", "Lake Travis", "Sabine River", "Mississippi River", 
    "Lake Oahe", "St. Lawrence River", "Lake Chatuge", "St. Johns River", "Lake Lanier", 
    "Lake Hartwell", "Lake Hartwell", "Winyah Bay", "Lake Guntersville", "Lake Guntersville", 
    "St. Lawrence River", "Cayuga Lake", "Lake Tenkiller", "Lake St. Clair", "Lake Eufaula", 
    "Mississippi River", "Lake Eufaula", "Lake Champlain", "Lake Champlain", "Lake St. Clair", 
    "Lake Guntersville", "Santee Cooper Lakes", "Chickamauga Lake", "Lake Fork", "St. Johns River", 
    "Tennessee River", "Pickwick Lake", "Sabine River", "Lake Fork", "Neely Henry Lake", 
    "Lake Guntersville", "Lake Ray Roberts", "Lake Champlain", "St. Lawrence River", "St. Johns River", 
    "Harris Chain of Lakes", "Lake Hartwell", "Santee Cooper Lakes", "Chickamauga Lake", "Lake Fork", 
    "Pickwick Lake", "St. Lawrence River", "Lake Oahe", "Mississippi River", "Lake Okeechobee", 
    "Lake Seminole", "Tennessee River", "Lake Murray", "Santee Cooper Lakes", "Lay Lake", 
    "Sabine River", "Lake St. Clair", "Lake Champlain", "St. Lawrence River", "Toledo Bend Reservoir", 
    "Lake Fork", "Grand Lake", "Harris Chain of Lakes", "St. Johns River", "Lake Murray", 
    "Wheeler Lake", "Smith Lake", "Lake Champlain", "St. Lawrence River", "St. Johns River", 
    "Lake Okeechobee", "Lake Ray Roberts", "Pasquotank River", "Lake Hartwell", "Lake Fork", 
    "Sabine River", "Lake Tenkiller", "Lake St. Clair", "Mississippi River", "Lake Guntersville", 
    "Lake Martin", "Tennessee River", "Tennessee-Tombigbee Waterway", "Arkansas River", "Lake Murray", 
    "Santee Cooper Lakes", "Pasquotank River / Albemarle Sound", "Lake Champlain", "St. Lawrence River"
  ),
  clean_Location = c(
    "Shreveport, LA", "Palatka, FL", "Okeechobee, FL", "Bull Shoals, AR", "Dandridge, TN", 
    "Many, LA", "La Crosse, WI", "Green Bay, WI", "Oneida Lake, NY", "Grove, OK", 
    "Orange, TX", "Zapata, TX", "Bull Shoals, AR", "LaGrange, GA", "Montgomery, AL", 
    "La Crosse, WI", "Ogdensburg, NY", "Detroit, MI", "Birmingham, AL", "Bainbridge, GA", 
    "Palatka, FL", "Branson, MO", "Many, LA", "Russellville, AR", "Dayton, TN", 
    "Union Springs, NY", "Escanaba, MI", "Greenville, SC", "Orange, TX", "Guntersville, AL", 
    "Sacramento, CA", "Lake Havasu City, AZ", "Paris, TN", "Waddington, NY", "Cecil County, MD", 
    "Detroit, MI", "Sturgeon Bay, WI", "Grove, OK", "Palatka, FL", "Georgetown, SC", 
    "Mountain Home, AR", "Decatur, AL", "Many, LA", "Durant, OK", "Union Springs, NY", 
    "Charles County, MD", "La Crosse, WI", "Mille Lacs, MN", "Jefferson City, TN", "Houston, TX", 
    "Many, LA", "Ridgeland, MS", "Lufkin, TX", "Russellville, AR", "Waddington, NY", 
    "Plattsburgh, NY", "Macomb County, MI", "Mille Lacs Lake, MN", "Alexander City, AL", "Greenville, SC", 
    "Grove, OK", "Paris, TN", "Jonestown, TX", "Orange, TX", "La Crosse, WI", 
    "Pierre, SD", "Waddington, NY", "Lake Chatuge, GA", "Palatka, FL", "Gwinnett, GA", 
    "Anderson, SC", "Anderson, SC", "Georgetown, SC", "Scottsboro, AL", "Scottsboro, AL", 
    "Waddington, NY", "Union Springs, NY", "Cookson, OK", "Detroit, MI", "Eufaula, AL", 
    "La Crosse, WI", "Eufaula, AL", "Plattsburgh, NY", "Plattsburgh, NY", "Macomb County, MI", 
    "Scottsboro, AL", "Manning, SC", "Dayton, TN", "Quitman, TX", "Palatka, FL", 
    "Knoxville, TN", "Florence, AL", "Orange, TX", "Quitman, TX", "Gadsden, AL", 
    "Scottsboro, AL", "Fort Worth, TX", "Burlington, VT", "Waddington, NY", "Palatka, FL", 
    "Leesburg, FL", "Greenville, SC", "Clarendon County, SC", "Dayton, TN", "Quitman, TX", 
    "Counce, TN", "Clayton, NY", "Mobridge, SD", "La Crosse, WI", "Okeechobee, FL", 
    "Bainbridge, GA", "Knoxville, TN", "Columbia, SC", "Clarendon County, SC", "Shelby County, AL", 
    "Orange, TX", "Macomb County, MI", "Plattsburgh, NY", "Clayton, NY", "Many, LA", 
    "Yantis, TX", "Grove, OK", "Leesburg, FL", "Palatka, FL", "Prosperity, SC", 
    "Decatur, AL", "Cullman, AL", "Plattsburgh, NY", "Waddington, NY", "Palatka, FL", 
    "Okeechobee, FL", "Fort Worth, TX", "Elizabeth City, NC", "Anderson, SC", "Yantis, TX", 
    "Orange, TX", "Cookson, OK", "Macomb County, MI", "La Crosse, WI", "Scottsboro, AL", 
    "Alexander City, AL", "Knoxville, TN", "Columbus, MS", "Muskogee, OK", "Columbia, SC", 
    "Clarendon County, SC", "Elizabeth City, NC", "Plattsburgh, NY", "Clayton, NY"
  )
)

# 2. Build the lookup map directly alongside the messy entries
lookup_table <- unique_events %>%
  distinct(Season_Year, Event_Name, Waterbody, Location) %>%
  rename(
    old_Event_Name = Event_Name,
    old_Waterbody = Waterbody,
    old_Location = Location
  ) %>%
  bind_cols(clean_149)

# 3. Merge the clean fields into your deep dataset using original keys
final_merged_bass <- bass_clean %>%
  left_join(
    lookup_table, 
    by = c(
      "Season_Year" = "Season_Year", 
      "Event_Name" = "old_Event_Name", 
      "Waterbody" = "old_Waterbody", 
      "Location" = "old_Location"
    )
  ) %>%
  # 4. Overwrite original columns with the clean mapped values
  mutate(
    Event_Name = clean_Event_Name,
    Waterbody = clean_Waterbody,
    Location = clean_Location
  ) %>%
  # 5. Clean up temporary reference helper columns
  select(-clean_Event_Name, -clean_Waterbody, -clean_Location)
























