#%% fix
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None #for settingwithcopywarning
#%%
def bbanalyze():
    """
    :return: constructs and returns a dictionary with the following cells:
             -record.count
             -complete.cases
             -years
             -player.count
             -team.count
             -league.count
             -bb
             -nl
             -al
             -records
    :rtype: dictionary
    """

    #read csv file into python using pandas
    df = pd.read_csv("baseball.csv")

    #finding count of number of records in dataset
    record_count = len(df) # number of records in dataset = number of rows in the dataset

    #finding complete cases (no NANs)
    complete_cases = len(df.dropna()) #drops all rows with nan values, takes length of that

    #tuple of year (min, max)
    min_year = df["year"].min() #finding min value
    max_year = df["year"].max() #finding max value

    years = (min_year, max_year) #year in tuple form

    #count of number of players
    player_count = df["id"].nunique() #counts number of unique id values

    #count of number of teams
    team_count = df["team"].nunique() #counts number of unique team values

    #league_count
    league_count = df["lg"].nunique() #counts number of unique league values

    #revised baseball data set
    bb_comp = df.dropna()  #complete cases

    obp_num = bb_comp["h"] + bb_comp["bb"] + bb_comp["hbp"]
    obp_denom = bb_comp["ab"] + bb_comp["bb"] + bb_comp["hbp"]

    obp = obp_num / obp_denom #creating obp column
    obp.name = "obp"

    pab_num = bb_comp["h"] + bb_comp["bb"] + bb_comp["hbp"] + bb_comp["sf"] + bb_comp["sh"]
    pab_denom = bb_comp["ab"] + bb_comp["bb"] + bb_comp["hbp"] + bb_comp["sf"] + bb_comp["sh"]

    pab = pab_num / pab_denom #creating pab column
    pab.name = "pab"

    bb = pd.concat([bb_comp, obp, pab],axis=1) #revised baseball data set

    #dict with national league data
    dat_nl = bb[bb["lg"] == "NL"] #subset bb df to only include national league data

    nl = {"dat": dat_nl, #creating the nl dict
          "players": dat_nl["id"].nunique(), #count number of players in dat_nl df
          "teams": dat_nl["team"].nunique()} #count number of teams in dat_nl df

    #dict with american league data
    dat_al = bb[bb["lg"] == "AL"]  # subset bb df to only include american league data

    al = {"dat": dat_al, #creating the al dict
          "players": dat_al["id"].nunique(), #count number of players in dat_al df
          "teams": dat_al["team"].nunique()} #count number of teams in dat_al df

    #creating the records dictionary:
    bbrec = bb[(bb["stint"] == 1) & (bb["ab"] >= 50)] #players with 50 or more at bats in a stint

    def rec_ind(column_name):  # function- returns highest id
        rec_in = bbrec.groupby("id")[column_name].max().sort_values(ascending=False).index[0]

        return rec_in

    def rec_val(column_name):  # function- returns highest value
        rec_val = bbrec.groupby("id")[column_name].max().sort_values(ascending=False).iloc[0]

        return rec_val

    def new_col_a(column_name):  # creates new column for percentage of plate appearances
        bbrec.loc[:, f"{column_name}a"] = bbrec[column_name] / (
                    bbrec["ab"] + bbrec["bb"] + bbrec["hbp"] + bbrec["sf"] + bbrec["sh"])

        return bbrec
    def perab_ind_a(column_name):  # function- returns index of percentage of at plate appearances
        new_col_a(column_name)

        perab_ind = bbrec.groupby("id")[column_name].max().sort_values(ascending=False).index[0]
        return perab_ind

    def perab_val_a(column_name):  # function- returns val of percentage of at plate appearances
        new_col_a(column_name)

        perab_val = bbrec.groupby("id")[column_name].max().sort_values(ascending=False).iloc[0]
        return (f"{round(perab_val, 2)}%")

    def new_col_p(column_name):  # creates new column for percentage of abs
        bbrec.loc[:, f"{column_name}p"] = bbrec[column_name] / bbrec["ab"]

        return bbrec

    def perab_ind_p(column_name):  # function- returns index of percentage of at bats values
        new_col_p(column_name)

        perab_ind = bbrec.groupby("id")[column_name].max().sort_values(ascending=False).index[0]
        return perab_ind

    def perab_val_p(column_name):  # function- returns val of percentage of at bats values
        new_col_p(column_name)

        perab_val = bbrec.groupby("id")[column_name].max().sort_values(ascending=False).iloc[0]
        return (f"{round(perab_val, 2)}%")

    def records():  # function- returns records dictionary of 14 career records
        obp_record = {"id": rec_ind("obp"),
                      "value": rec_val("obp")
                      }

        pab_record = {"id": rec_ind("pab"),
                      "value": rec_val("pab")
                      }

        hr_record = {"id": rec_ind("hr"),
                     "value": rec_val("hr")
                     }

        hrp_record = {"id": perab_ind_p("hr"),
                      "value": perab_val_p("hr")
                      }

        h_record = {"id": rec_ind("h"),
                    "value": rec_val("h")
                    }

        hp_record = {"id": perab_ind_p("h"),
                     "value": perab_val_p("h")
                     }

        sb_record = {"id": rec_ind("sb"),
                     "value": rec_val("sb")
                     }

        sbp_record = {"id": perab_ind_p("sb"),
                      "value": perab_val_p("sb")
                      }

        so_record = {"id": rec_ind("so"),
                     "value": rec_val("so")
                     }

        sop_record = {"id": perab_ind_p("so"),
                      "value": perab_val_p("so")
                      }

        sopa_record = {"id": perab_ind_a("sop"),
                       "value": perab_val_a("sop")
                       }

        bb_record = {"id": rec_ind("bb"),
                     "value": rec_val("bb")
                     }

        bbp_record = {"id": perab_ind_p("bb"),
                      "value": perab_val_p("bb")
                      }

        g_record = {"id": rec_ind("g"),
                    "value": rec_val("g")
                    }

        records = {"obp": obp_record,
                   "pab": pab_record,
                   "hr": hr_record,
                   "hrp": hrp_record,
                   "h": h_record,
                   "hp": hp_record,
                   "sb": sb_record,
                   "sbp": sbp_record,
                   "so": so_record,
                   "sop": sop_record,
                   "sopa": sopa_record,
                   "bb": bb_record,
                   "bbp": bbp_record,
                   "g": g_record
                   }
        return(records)

    #constructing the dict that is returned by bbanalyze
    main_dict = {"record.count": record_count,
                 "complete.cases": complete_cases,
                 "years": years,
                 "player.count": player_count,
                 "team.count": team_count,
                 "league.count": league_count,
                 "bb": bb,
                 "nl": nl,
                 "al": al,
                 "records": records()
               }
    return main_dict
#%%
bbanalyze()