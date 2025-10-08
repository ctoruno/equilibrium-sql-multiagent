# EPHC 2024
The Encuesta Permanente de Hogares Continua (EPHC) 2024, conducted by Paraguay's National Institute of Statistics (INE), is the country's primary ongoing household survey that has continuously measured employment, unemployment, income, and socioeconomic characteristics of the Paraguayan population. The survey covers the Eastern Region and Presidente Hayes department, targeting the population residing permanently in private dwellings. Operating under a quarterly data collection cycle with 50% inter-annual panel overlap, the EPHC 2024 employs a probabilistic two-stage stratified cluster design with an annual sample of 21,024 dwellings distributed across four quarters. The survey generates indicators on labor force participation, employment conditions, underemployment, income sources, and other demographic and economic characteristics at national, urban, and rural levels. Following the 2022 Census preliminary results, the EPHC has revised its weighting factors to align with updated population estimates, ensuring more accurate statistical validity for monitoring labor market dynamics and informing evidence-based policy decisions in Paraguay.

## Tables
The ephc-2024 database is composed by 3 different tables:
- REG01_EPHC_ANUAL_2024
- REG02_EPHC_ANUAL_2024
- INGREFAM_EPHC_ANUAL_2024

### REG01_EPHC_ANUAL_2024
**Module Name**: VIVIENDA

**Description:**
Comprehensive household characteristics module capturing dwelling quality, basic services infrastructure, household equipment ownership, and housing tenure arrangements. This module provides a complete picture of living conditions, material wellbeing, and access to essential utilities and amenities at the household level.

**Business Domain:** Housing, Utilities, Demographics & Assets

**Identifiers**: Each row represents a household. Records are uniquely identified at the household level by the combination of household identifiers (UPM, NVIVI, NHOGA).

**Expansion Factor**: FEX_2022 provides the statistical weight for population-level estimates and projections.

**Key Topics Covered:**
- **Household Composition**: Total members by gender (male, female counts), household type classification (unipersonal, nuclear complete/incomplete, extended, composite)
- **Dwelling Characteristics**: Housing type (house/ranch, apartment, tenement room, improvised dwelling), room count, bedroom count, construction materials for walls, floors, and roofs
- **Water Access**: Primary water source for general use and drinking water, water delivery method (piping within/outside dwelling, public tap, well, neighbor, water carrier), 24-hour availability indicator
- **Basic Utilities**: Electricity availability, fixed telephone line, mobile phone ownership
- **Sanitation**: Bathroom availability, wastewater disposal method (sewage network, septic tank, dry pit latrine, open surface, various latrine types)
- **Cooking Infrastructure**: Separate cooking room availability, primary cooking fuel (firewood, gas, charcoal, electricity, kerosene)
- **Waste Management**: Usual garbage disposal method (burning, public/private collection, dumping in various locations)
- **Housing Tenure**: Dwelling ownership status (owned, paying installments, condominium, rented, occupied de facto, ceded), land/lot tenure status, monthly rent paid, estimated rental value, estimated sale price
- **Household Assets & Equipment**: Ownership of technology devices (computer/notebook, tablet, internet access with connection types), home appliances (radio, TV, refrigerator, gas/electric stove, washing machine, video/DVD, water heater, air conditioner, microwave, electric oven), communication services (satellite dish, cable TV), vehicles (car/truck/pickup, motorcycle)
- **Housing Expenses**: 12-month recall question for housing-related expenditures (specific item details truncated in source)
- **Poverty Indicators**: Poverty status classification (extreme poor, non-extreme poor, non-poor), binary poverty condition flag

### REG02_EPHC_ANUAL_2024
**Module Name**: Registro de Población

**Description:**
Comprehensive individual-level module capturing demographic characteristics, labor market participation, educational attainment, health status, and income sources for all household members. This module provides complete person-level information on employment conditions, job characteristics, earnings, social protection coverage, educational trajectories, health care access, and socioeconomic status.

**Business Domain:** Demographics, Labor Market, Education, Health & Income

**Identifiers**: Each row represents an individual household member. Records are uniquely identified by the combination of household identifiers (UPM, NVIVI, NHOGA) and L02 (person line number).

**Expansion Factor**: FEX_2022 provides the statistical weight for population-level estimates and projections.

**Key Topics Covered:**
- **Demographics & Household Structure**: Line number, age, relationship to household head, household membership status, identity documentation (Paraguayan/foreign ID cards), civil registry enrollment, spouse/parent/mother line numbers, sex, date of birth (day/month/year), marital status, household type classification
- **Proxy Respondent Information**: Self-response indicator, proxy respondent line number
- **Employment Status & Job Search**: Work in last 7 days (any employment, minimum hours threshold), job attachment during absence, expected absence duration, number of jobs held, availability to start work, active job search (7-day and 30-day recall), job search methods, duration of job search (years/months/weeks), previous work experience
- **Main Occupation Characteristics**: Occupation code, economic sector, daily hours worked (Monday through Sunday), usual vs. actual hours comparison, reasons for deviation from usual hours, usual weekly hours, tenure in occupation (years/months/weeks), establishment size, employer tenure, pension contribution status and fund type, employment category, private insurance coverage and cost-sharing arrangements, paid vacation days, weekly rest days, union/association membership
- **Compensation - Main Job**: Net pay amount and payment period, additional salary components (overtime/commissions, annual bonus/aguinaldo), free meals/drinks and estimated value, employer-provided housing (occupancy or subsidized rent, market rent comparison), free uniform/clothing annual value, employment contract type (indefinite, temporary with/without invoicing, verbal)
- **Workplace Formality Indicators**: Manager line numbers, establishment RUC registration, legal business structure, invoice issuance practices
- **Secondary & Other Occupations**: Secondary job indicator, occupation/sector codes, hours worked (actual and usual), establishment size, pension contributions, employment category, manager line numbers, compensation amounts and payment periods, additional income components, contract type, formality indicators, count and characteristics of additional jobs
- **Underemployment & Job Mobility**: Availability for additional hours, desired hours increase, desire to improve/change/add jobs, active search for job changes, reasons for wanting to change employment
- **Income Sources**: Declared and imputed monthly income from: main/secondary/other occupations, rental income, interest/dividends/profits, domestic family assistance, divorce settlements/child support, pensions, government transfer programs (Tekoporá, Elderly Adult), special pensions (ex-combatants/widows), public food assistance, foreign remittances, agricultural income assigned to household head, school feeding program values (milk glass, lunch/dinner)
- **Socioeconomic Classification**: Per capita monthly income, poverty status (extreme poor/non-extreme poor/non-poor), binary poverty indicator, national and area-specific income quintiles and deciles, labor informality status (non-agricultural workers)
- **Derived Labor Market Variables**: Recoded employment category, establishment size, occupation classification, economic sector, total hours in main/secondary/all occupations, detailed and aggregated economic activity status (employed/unemployed/inactive, subemployment visibility), reason for economic inactivity
- **Educational Background**: Primary language spoken at home, literacy status, formal education attendance (ever and current), highest level and grade completed, title/diploma obtained, current enrollment by education level, school sector (public/private/subsidized), reasons for not attending school, receipt of school feeding programs (breakfast/snack, lunch/dinner - annual and monthly recall)
- **Derived Educational Variables**: Years of schooling, educational level of household head/spouse/father/mother
- **Health Status & Access**: Current health insurance coverage (IPS, private individual/employment/family, military/police sanitary services), IPS beneficiary type, illness or accident in last 90 days, specific illness types (up to 3), medical consultation for recent illness/accident, reason for not seeking care, type of health provider consulted, health facility type used, free medication receipt, hospitalization for recent illness/accident

# INGREFAM_EPHC_ANUAL_2024
**Module Name**: INGRESOS FAMILIARES

**Description:**
Household-level income aggregation and poverty measurement module consolidating all income sources (labor, capital, transfers, imputed values) to calculate comprehensive household income, per capita income, and poverty indicators. This module serves as the primary source for poverty analysis and socioeconomic stratification using official poverty lines and FGT (Foster-Greer-Thorbecke) poverty measures.

**Business Domain:** Income, Poverty & Demographics

**Identifiers**: Each row represents a household. Records are uniquely identified by the combination: UPM, NVIVI, NHOGA.

**Expansion Factor**: FEX_2022 provides the base statistical weight (househol-level). FACPOB (FEX_2022 × TOTPERS) provides the population expansion factor for person-level estimates.

**Key Topics Covered:**
- **Geographic & Survey Identifiers**: Primary sampling unit (UPM), dwelling identifier (NVIVI), household identifier (NHOGA), department of residence (Asunción and 15 departments), urban/rural area classification, survey year
- **Deflated Income Sources - Labor**: Main occupation income, secondary occupation income, other occupations income (all deflated to reference period prices)
- **Deflated Income Sources - Capital**: Net rental income, interest/dividends/profits (deflated)
- **Deflated Income Sources - Private Transfers**: Domestic family assistance, remittances from abroad, alimony/child support, other income (deflated)
- **Deflated Income Sources - Public Transfers**: Pension/retirement income, TekoporÃ£ program transfers, Adulto Mayor program transfers, in-kind public food assistance valued as income (deflated)
- **Deflated Income Sources - Agricultural**: Other agricultural income assigned to household head (deflated)
- **Deflated Income Sources - Imputed Values**: Owner-occupied housing imputed rent, school milk program imputed value, school lunch/dinner program imputed value (all deflated)
- **Deflated Deductions**: Annual tax expenditures (deflated, divided by 12 for monthly calculation)
- **Household Size**: Total household members excluding live-in domestic workers (TOTPERS)
- **Income Aggregates**: Monthly household income (INGREM = sum of all income sources minus monthly tax deduction), monthly per capita household income (IPCM = INGREM / TOTPERS), geographically deflated per capita income (IPCMDEFG)
- **Poverty Lines**: Total poverty line threshold (LINPOBTO), extreme poverty line threshold (LINPOBEX)
- **Poverty Classification**: Three-level poverty status (extreme poor, non-extreme poor, non-poor), binary poverty condition (poor/non-poor)
- **FGT Poverty Measures - Total Poverty**: Headcount ratio (P0POBTOT - incidence), poverty gap index (P1POBTOT - intensity/depth), squared poverty gap (P2POBTOT - severity/inequality among poor)
- **FGT Poverty Measures - Extreme Poverty**: Headcount ratio (P0POBEXT - incidence), poverty gap index (P1POBEXT - intensity/depth), squared poverty gap (P2POBEXT - severity/inequality among poor)
- **Income Distribution**: National income quintiles and deciles (QUINTILI, DECILI), area-specific income quintiles and deciles (QUINTIAI, DECILAI)