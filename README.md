# Economic Scenario Generator REST Service

## Overview

### 1. What is Economic Scenario Generator?
Economic Scenario Generator is a software tool that many financial institutions
utilize to generate stochastic interest rates, equities, credits, FX,
and/or other asset classes to fulfill their various needs. For example, an 
investment banker may utilize Risk-Neutral ESG (no additional expected return from
investing risky asset) to price exotic derivatives or review hedging
strategies. Or, an insurer may utilize a Real-World ESG (realistic ESG with risk premium)
to find the reserve requirements to meet regulatory demands. 

### 2. Features to be developed
* Pull necessary market data from the Internet
* Implement American Academy of Actuaries ESG in Python
* Add Risk-Neutral ESG
* Fast generations of scenarios by using numpy optimization
* Push the scenarios as JSON form to www.financescript.com by using REST API

## Purpose of this tool
This tool would be used for computing the discount rates in the
equity researches in FinancialScript.com

In traditional equity research, an analyst would calculate the expected cash flow
and then discount them by the risk-adjusted rates, which are mostly deterministic and
highly subjective. Using the monte carlo simulations could reduce the valuation errors,
and also allow us to get a range of values within some confidence levels. 

## Installation
This tool should work in any version of Python 3.5+

All the necessary libraries are/will be included in requirements.txt
```
pip install requirements.txt
```

## Source
<a href="https://www.actuary.org/">American Academy of Actuaries</a> published Excel workbook
which contains Excel code that generates a lot of interest rate and equity.
Our ESG tool will mostly implement this tool, and build additional features listed above.
