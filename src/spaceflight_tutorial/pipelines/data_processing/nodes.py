"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.4
"""

import pandas as pd

# change the "t" and "f" into true false

def _is_true(x:pd.Series)->pd.Series:
    return x=="t"

#function example
#_is_true(shuttles.d_check_complete)

# parsing the money data by remove "$" and ","  ex: $1,325.0 -> 1325.o

def _parse_money(x:pd.Series)->pd.Series:
    x=x.str.replace("$","").str.replace(",","")
    x=x.astype(float)
    return x

#function example
#_parse_money(shuttles.price)

# parsing the percantege data by remove "%",  ex: 67% -> 0.67

def _parse_percentage(x:pd.Series)->pd.Series:
    x=x.str.replace("%","")
    x=x.astype(float)/100
    return x

#function example
#_parse_percentage(companies['company_rating'])

def preprocess_companies(companies:pd.DataFrame)->pd.DataFrame:
    """Preprocesses the data for companies.

    Args:
        companies: Raw data.
    Returns:
        Preprocessed data, with `company_rating` converted to a float and
        `iata_approved` converted to boolean.
    """
    companies['company_rating']=_parse_percentage(companies['company_rating'])
    companies['iata_approved']=_is_true(companies['iata_approved'])
    return companies
     
# function example
#preprocess_companies(companies)


def preprocess_shuttles(shuttles: pd.DataFrame) -> pd.DataFrame:
    """Preprocesses the data for shuttles.

    Args:
        shuttles: Raw data.
    Returns:
        Preprocessed data, with `price` converted to a float and `d_check_complete`,
        `moon_clearance_complete` converted to boolean.
    """
    shuttles['price']=_parse_money(shuttles['price'])
    shuttles['moon_clearance_complete']=_is_true(shuttles['moon_clearance_complete'])
    shuttles['d_check_complete']=_is_true(shuttles['d_check_complete'])
    return shuttles

# function example
#preprocess_shuttles(shuttles)

def create_model_input_table(
    shuttles: pd.DataFrame, companies: pd.DataFrame, reviews: pd.DataFrame
) -> pd.DataFrame:
    """Combines all data to create a model input table.

    Args:
        shuttles: Preprocessed data for shuttles.
        companies: Preprocessed data for companies.
        reviews: Raw data for reviews.
    Returns:
        model input table.

    """
    rated_shuttles = shuttles.merge(reviews, left_on="id", right_on="shuttle_id")
    model_input_table = rated_shuttles.merge(
        companies, left_on="company_id", right_on="id"
    )
    model_input_table = model_input_table.dropna()
    return model_input_table