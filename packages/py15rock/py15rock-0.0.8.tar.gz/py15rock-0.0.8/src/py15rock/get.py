import requests    
import pandas as pd

class config:
    api_key = None

#actual api calls
def requestCompanyReturning(ticker, endpoint):
    r = requests.get(f'https://api.15rock.com/company/{ticker}/{endpoint}', headers={'Authorization': f'{config.api_key}'})
    df = pd.read_json(r.content)
    return df

#api calls for endpoints that require years 
def requestCompanyReturningYears(ticker, years, endpoint, token):
    r = requests.get(f'https://api.15rock.com/company/{ticker}/{endpoint}/{years}', headers={'Authorization': f'{config.api_key}'})
    df = pd.read_json(r.content)
    return df


#company endpoints

def companyCarbon(ticker):
    df = requestCompanyReturning(ticker, "carbon-footprint")
    return df

def companyIndustryAverage(ticker):
    df = requestCompanyReturning(ticker, "industry-average")
    return df

def companyNetincomeCarbon(ticker):
    df = requestCompanyReturning(ticker, "netincome-carbon")
    return df

def company15rockScore(ticker):
    df = requestCompanyReturning(ticker, "15rock-globalscore")
    return df

def companyInfo(ticker):
    df = requestCompanyReturning(ticker, "")
    return df

def companyCalculator(ticker):
    df = requestCompanyReturning(ticker, "equivalencies_calculator")
    return df

def companyIndustrySum(ticker):
    df = requestCompanyReturning(ticker, "industry-sum")
    return df

def companyEmissionsEfficiency(ticker):
    df = requestCompanyReturning(ticker, "EmissionsEfficiency")
    return df

def companyHistoricalPrices(ticker):
    df = requestCompanyReturning(ticker, "historicalPrices")
    return df

def companyCOGS(ticker):
    df = requestCompanyReturning(ticker, "cogs")
    return df

def companySumHistoricCarbon(ticker, years):
    df = requestCompanyReturningYears(ticker, years, "sumhistoriccarbon")
    return df

def companyTempConversation(ticker, years):
    df = requestCompanyReturningYears(ticker, years, "temperatureconversion")
    return df

def companyCarbonAlpha(ticker, years):
    df = requestCompanyReturningYears(ticker, years, "carbonAlpha")
    return df

def companyCarbonTransitionRisk(ticker, years):
    df = requestCompanyReturningYears(ticker, years, "CarbonTransitonRisk")
    return df






def getCompany(ticker, endpoint, token):
    r = requests.get(f'https://api.15rock.com/company/{ticker}/{endpoint}', headers={'Authorization': f'{token}'})
    df = pd.read_json(r.content)
    return df