# ENAHO 2024
The 2024 National Household Survey (ENAHO), conducted by the National Institute of Statistics and Informatics (INEI), is an ongoing survey that has measured the living conditions, poverty, and well-being of Peruvian households since 1995. Its coverage is national, encompassing urban and rural areas of the 24 departments and the Constitutional Province of Callao, through mixed interviews (in-person and by telephone). The 2024 sample comprises 36,594 households and allows for the generation of indicators on poverty, employment, health, education, spending, social programs, governance, and other social and economic aspects, with inference levels from the national to the departmental level.

## Tables
The enaho-2024 database is composed by 12 different tables:
- ENAHO01-2024-100
- ENAHO01-2024-200
- ENAHO01-2024-601
- ENAHO01-2024-603
- ENAHO01-2024-604
- ENAHO01-2024-605
- ENAHO01-2024-609
- ENAHO01-2024-612
- ENAHO01A-2024-300
- ENAHO01A-2024-400
- ENAHO01A-2024-500
- SUMARIA-2024-12G

### ENAHO01-2024-100
**Module Name**: Características de la Vivienda y del Hogar (Módulo 100)

**Description:**
Core housing and household characteristics module capturing detailed information about dwelling conditions, infrastructure access, utilities, and basic household demographics.

**Business Domain:** Housing & Infrastructure Analytics

**Identifiers**: Each row represents a household (hogar), noting that a single dwelling (vivienda) can contain multiple households. Records are uniquely identified by the combination: ANO, MES, CONGLOME, VIVIENDA, HOGAR.

**Expansion Factor**: FACTOR07 provides the statistical weight for population-level estimates and projections.

**Key Topics Covered:**
- Housing Quality & Construction: Dwelling type, construction materials, building permits, technical assistance
- Property Ownership & Finance: Ownership status, property titles, mortgage/credit information, rental costs, property valuations
- Basic Infrastructure Access: Water supply sources, sanitation systems, electricity connections
- Utilities & Services: Telecommunications (phone, internet, cable TV), cooking fuel types, lighting sources
- Household Expenses: Monthly expenditures on utilities, fuel, and communication services by source

### ENAHO01-2024-200
**Module Name**: Características de los Miembros del Hogar (Módulo 200)

**Description:**
Individual demographics and basic labor activity module capturing personal characteristics, household relationships, and preliminary work engagement for all household members.

**Business Domain:** Demographics & Labor Force Analytics

**Identifiers**: Each row represents an individual person within households. Records are uniquely identified by the combination: ANO, MES, CONGLOME, VIVIENDA, HOGAR, CODPERSO.

**Expansion Factor**: FACPOB07 provides the statistical weight for population-level estimates and projections.

**Key Topics Covered:**
- Individual Demographics: Age, sex, marital status, household membership status, presence/absence patterns
- Household Relationships: Relationship to household head, family nucleus composition and roles
- Basic Labor Activity: Previous week work engagement, type of tasks performed, hours worked
- Child Labor Assessment: Hazardous task classification based on activity type and time commitment
- Module Assignments: Eligibility indicators for education, health, and employment survey modules

### ENAHO01-2024-601
**Module Name**: Gastos del Hogar

**Description:**
Household expenditure module capturing detailed food and non-food consumption patterns, acquisition methods, quantities, and spending by households over a 15-day reference period.

**Business Domain:** Consumer Expenditure & Food Security Analytics

**Identifiers**: Each row represents a specific product obtained by a household. Records are uniquely identified by the combination: ANO, MES, CONGLOME, VIVIENDA, HOGAR, P601A (product code).

**Expansion Factor**: FACTOR07 provides the statistical weight for population-level estimates and projections.

**Key Topics Covered:**
- Product Acquisition Methods: Purchase, self-production, gifts, in-kind payments, social program benefits, other sources
- Purchase Behavior: Frequency of purchase, quantities bought, units of measurement, purchase locations, total expenditure
- Consumption Patterns: Frequency of consumption, quantities consumed, consumption periodicity
- Expenditure Analysis: Both raw and processed monetary values
- Product Classification: Standardized product codes and free/subsidized good indicators

**Important Note**: This tables registers specific expenditure on certain products or services. For aggregated household income and expenditure data, please refer to the SUMARIA-2024-12G table. Additionally, for ratios and percentages involving expenditure data covered in this  module, it is best to use the SUMARIA-2024-12G table as the denominator to ensure consistency.

### ENAHO01-2024-603
**Module Name**: Mantenimiento de la Vivienda

**Description:**
Household maintenance and cleaning products expenditure module capturing acquisition methods, costs, and valuations for cleaning supplies, maintenance services, and household care items over a monthly reference period.

**Business Domain:** Household Maintenance Expenditure Analytics

**Identifiers**: Each row represents a specific maintenance product or service obtained by a household. Records are uniquely identified by the combination: ANO, MES, CONGLOME, VIVIENDA, HOGAR, P603N.

**Expansion Factor**: FACTOR07 provides the statistical weight for population-level estimates and projections.

**Key Topics Covered:**
- Product Acquisition Methods: Purchase, self-production, in-kind payments, gifts from other households, institutional donations, other sources
- Purchase Details: Purchase locations, total expenditure amounts for bought items
- Service Valuations: Estimated market values for non-purchased items across all acquisition methods
- Product Categories: Cleaning supplies, maintenance tools, household services, personal care items
- Cost Analysis: Both raw and processed monetary estimates

**Important Note**: This tables registers specific expenditure on certain products or services. For aggregated household income and expenditure data, please refer to the SUMARIA-2024-12G table. Additionally, for ratios and percentages involving expenditure data covered in this  module, it is best to use the SUMARIA-2024-12G table as the denominator to ensure consistency.

### ENAHO01-2024-604
**Module Name**: Transportes y Comunicaciones

**Description:**
Transportation and communications expenditure module capturing household spending on vehicle fuels, transportation services, travel expenses, and communication services over a monthly reference period.

**Business Domain:** Transportation & Communications Expenditure Analytics

**Identifiers**: Each row represents a specific transportation or communication product/service used by a household. Records are uniquely identified by the combination: ANO, MES, CONGLOME, VIVIENDA, HOGAR, P604N.

**Expansion Factor**: FACTOR07 provides the statistical weight for population-level estimates and projections.

**Key Topics Covered:**
- Vehicle Operations: Gasoline, diesel fuel, vehicle maintenance and repair services
- Transportation Services: Public transport, specialized transport for minors, mototaxi services
- Travel Expenses: Work/study trips, tourism travel, family-related travel
- Communication Services: Public telephone usage for minors, postal services, fax services, mobile phone accessories and equipment
- Acquisition Methods: Purchase, self-production, in-kind payments, gifts, institutional donations, other sources
- Cost Analysis: Purchase locations, total expenditure, and estimated market values for non-purchased services

**Important Note**: This tables registers specific expenditure on certain products or services. For aggregated household income and expenditure data, please refer to the SUMARIA-2024-12G table. Additionally, for ratios and percentages involving expenditure data covered in this  module, it is best to use the SUMARIA-2024-12G table as the denominator to ensure consistency.

### ENAHO01-2024-605
**Module Name**: Servicios a la Vivienda

**Description:**
Housing services expenditure module capturing household spending on property-related services including security, maintenance, domestic help, and waste management over a monthly reference period.

**Business Domain:** Housing Services & Property Management Analytics

**Identifiers**: Each row represents a specific housing service used by a household. Records are uniquely identified by the combination: ANO, MES, CONGLOME, VIVIENDA, HOGAR, P605N.

**Expansion Factor**: FACTOR07 provides the statistical weight for population-level estimates and projections.

**Key Topics Covered:**
- Security Services: Garage/parking services, security guard services, neighborhood watch programs (serenazgo)
- Property Maintenance: Building maintenance services, community services, private waste collection
- Domestic Services: Household domestic help and cleaning services
- Payment Methods: Direct household payments, gifts from other households, rent-inclusive services, other arrangements
- Cost Analysis: Monthly service costs and estimated market values for non-paid services

**Important Note**: This tables registers specific expenditure on certain products or services. For aggregated household income and expenditure data, please refer to the SUMARIA-2024-12G table. Additionally, for ratios and percentages involving expenditure data covered in this  module, it is best to use the SUMARIA-2024-12G table as the denominator to ensure consistency.

### ENAHO01-2024-609
**Module Name**: Gastos de Transferencias

**Description:**
Transfer payments and financial obligations module capturing household expenditures on legal, social, and family transfer payments including alimony, taxes, insurance premiums, and remittances over a quarterly reference period.

**Business Domain:** Financial Transfers & Obligations Analytics

**Identifiers**: Each row represents a specific transfer payment or financial obligation made by a household. Records are uniquely identified by the combination: ANO, MES, CONGLOME, VIVIENDA, HOGAR, P609N.

**Expansion Factor**: FACTOR07 provides the statistical weight for population-level estimates and projections.

**Key Topics Covered:**
- Legal Obligations: Alimony and child support payments
- Social Transfers: Tips to household members under 14, tips to non-household members, charitable donations to religious and social institutions
- Family Support: Remittances and gifts to household members living elsewhere, periodic transfers to non-resident family members
- Government Obligations: Direct taxes, mandatory insurance payments
- Cost Analysis: Total expenditure amounts with processed monetary estimates

**Important Note**: This tables registers specific expenditure on certain products or services. For aggregated household income and expenditure data, please refer to the SUMARIA-2024-12G table. Additionally, for ratios and percentages involving expenditure data covered in this  module, it is best to use the SUMARIA-2024-12G table as the denominator to ensure consistency.

### ENAHO01-2024-612
**Module Name**: Equipamiento del Hogar

**Description:**
Household durable goods inventory module capturing ownership, quantities, usage patterns, acquisition details, and valuations of household appliances, electronics, vehicles, and equipment.

**Business Domain:** Household Assets & Durable Goods Analytics

**Identifiers**: Each row represents a specific durable good owned by a household. Records are uniquely identified by the combination: ANO, MES, CONGLOME, VIVIENDA, HOGAR, P612N.

**Expansion Factor**: FACTOR07 provides the statistical weight for population-level estimates and projections.

**Key Topics Covered:**
- Electronics & Appliances: Audio/visual equipment, kitchen appliances, household appliances
- Technology Assets: Computers, laptops, tablets and computing equipment
- Transportation Vehicles: Cars, motorcycles, bicycles, commercial vehicles
- Asset Details: Quantity owned, primary usage, acquisition timing
- Economic Valuation: Original purchase costs, current market value estimates, and processed monetary values

**Important Note**: This tables registers specific expenditure on certain products or services. For aggregated household income and expenditure data, please refer to the SUMARIA-2024-12G table. Additionally, for ratios and percentages involving expenditure data covered in this  module, it is best to use the SUMARIA-2024-12G table as the denominator to ensure consistency.

### ENAHO01A-2024-300
**Module Name**: Educación

**Description:**
Individual education module capturing educational attainment, school enrollment, educational expenses, technology usage, and digital literacy skills for household members aged 3 and older.

**Business Domain:** Individual Education & Digital Literacy Analytics

**Identifiers**: Each row represents an individual household member aged 3+. Records are uniquely identified by the combination: ANO, MES, CONGLOME, VIVIENDA, HOGAR, CODPERSO.

**Expansion Factor**: FACTOR07 provides the statistical weight for population-level estimates and projections.

**Key Topics Covered:**
- Educational Background: Native language, educational attainment levels, career field studies, institutional details
- Current Education Status: School enrollment, attendance patterns, academic performance, reasons for non-attendance, educational institution quality assessments
- Educational Expenses: School supplies, uniforms, tuition, transportation, technology equipment, acquisition methods and costs
- Technology Access & Skills: Internet usage patterns, locations of access, devices used, digital activities performed, computer literacy skills assessment
- Vocational Training: Technical education programs, duration, certification details

### ENAHO01A-2024-400
**Module Name**: Salud

**Description:**
Comprehensive health and demographic module capturing health status, disability conditions, civil identity documentation, residential mobility, and basic demographic characteristics for all household members.

**Business Domain:** Individual Health & Demographic Analytics

**Identifiers**: Each row represents an individual household member. Records are uniquely identified by the combination: AÑO, MES, CONGLOME, VIVIENDA, HOGAR, CODPERSO.

**Expansion Factor**: FACTOR07 provides the statistical weight for population-level estimates and projections.

**Key Topics Covered:**
- Basic Demographics: Birth date, age, sex, marital status, household relationship, and membership status
- Civil Identity Documentation: National ID (DNI) possession status and detailed barriers to obtaining DNI or birth certificates
- Residential Mobility: Five-year migration patterns, current district residence history, and mother's residence location at respondent's birth
- Disability & Functional Limitations: Permanent limitations across six domains (mobility, vision, communication, hearing, cognitive function, social/mental health interactions)
- Health Status & Recent Conditions: Chronic disease presence and recent 4-week health episodes including symptoms, illnesses, chronic disease relapses, accidents, and COVID-19 symptoms
- Educational Background: Highest level of educational attainment achieved

### ENAHO01A-2024-500
**Module Name**: Empleo e Ingreso

**Description:**
Comprehensive employment and labor market module capturing work status, job characteristics, income sources, and employment conditions for all household members aged 14 years and older.

**Business Domain:** Labor Market & Employment Analytics

**Identifiers**: Each row represents an individual household member aged 14+. Records are uniquely identified by the combination: AÑO, MES, CONGLOME, VIVIENDA, HOGAR, CODPERSO.

**Expansion Factor**: FAC500A provides the statistical weight for population-level estimates and projections.

**Key Topics Covered:**
- Employment Status: Current work status, job attachment during temporary absence, business ownership, and detailed income-generating activities
- Job Characteristics: Primary occupation, main tasks performed, industry classification, employment status
- Workplace Structure: Employer type, business formality, accounting practices, firm size categories and exact worker counts
Employment Conditions: Contract types, supervision responsibilities
Compensation Structure: Multiple payment types including salary, wages, commission, piece rates, subsidies, professional fees, business profits, agricultural income, tips, in-kind payments, and unpaid work arrangements

### SUMARIA-2024-12G
**Module Name**: Sumaria por 12 Grupos de Gastos

**Description**:
Household-level summary dataset aggregating income and expenditure data across 12 consumption groups. This is the primary analytical file for poverty measurement, socioeconomic classification, and household welfare analysis in the ENAHO survey. All monetary values are annualized and standardized to a common reference period.

**Business Domain**: Household Income, Expenditure & Poverty Analytics

**Identifiers**: Each record represents a household uniquely identified by: ANO, MES, CONGLOME, VIVIENDA, HOGAR.

**Expansion Factor**: FACTOR07 provides statistical weights for generating population-level estimates based on 2007 census projections.

**Key Topics Covered**:
- Labor Income: Gross and net income from primary and secondary employment (dependent and independent work), including monetary payments, in-kind compensation, self-consumption, and extraordinary work income
- Non-Labor Income: Property rents, domestic and foreign transfers (private and public), social program benefits (Juntos, Pensión 65, Beca 18, various bonuses), imputed housing rent
- Social Program Transfers: Detailed breakdown of 14+ public assistance programs including conditional cash transfers, subsidies (gas, electricity), scholarships, and emergency bonuses
- Expenditure by 12 COICOP Groups:
    - Group 1: Food at home
    - Group 2: Alcoholic beverages and tobacco
    - Group 3: Clothing and footwear
    - Group 4: Housing, utilities, and fuels
    - Group 5: Furniture and home maintenance
    - Group 6: Health
    - Group 7: Transport
    - Group 8: Communications
    - Group 9: Recreation, culture, and pet care
    - Group 10: Education
    - Group 11: Restaurants and hotels (food away from home)
    - Group 12: Personal care and miscellaneous services
- Expenditure by Acquisition Type: Each group disaggregated by purchase, self-consumption/self-supply, in-kind payment, public donation, private donation, and other sources
- Housing Finance: Credits for home purchase, land acquisition, construction, and improvements
- Aggregate Income Measures:
    - INGMO1HD/INGMO2HD: Gross/net monetary income
    - INGHOG1D/INGHOG2D: Total gross/net income (including non-monetary)
    - GASHOG1D/GASHOG2D: Monetary and total expenditure
- Welfare Classification:
    - ESTRSOCIAL: Socioeconomic stratum (A through E, plus Rural)
    - POBREZA: Poverty status (extreme poor, non-extreme poor, non-poor)
    - POBREZAV: Poverty and vulnerability classification
    - LINEA/LINPE: Total and food poverty lines
- Household Demographics: Total members (MIEPERHO), total persons (TOTMIEHO), income earners (PERCEPHO)
- Geographic Classification: DOMINIO (8 geographic domains), ESTRATO (8 population-based strata), UBIGEO (district-level geographic code)

## Monetary Values
There are three types of monetary variables in the survey data. Current field values are the raw amounts reported by respondents for income or expenses, recorded as given and identified with “P”. Deflated values adjust these amounts to a common point of comparison by annualizing and correcting with the Consumer Price Index (CPI), identified with “D”. Imputed values take the deflated data and fill in missing responses using median-based imputation, identified with “I”.

For analysis, two distinctions are key. Nominal values correspond to the imputed data for the reference year of the survey. Real values adjust these nominal figures for inflation and geographic differences, using CPI averages and a spatial deflator with Lima Metropolitana as the base. This allows meaningful comparisons across regions and over time by removing inflationary effects.

## Tables Not Included
The following tables from the ENAHO 2024 survey are not included in this database due to their specialized nature or limited sample sizes. These modules focus on specific topics such as detailed agricultural activities, social program participation, governance, and individual income sources that may not be relevant for general household analysis:
- Instituciones Beneficas
- Esparcimiento y Cultura
- Vestido y Calzado
- Muebles y Enseres
- Otros Bienes y Servicios
- Produccion Agricola
- Subproductos Agricolas
- Produccion Forestal
- Gastos en Actividades Agricolas y Forestales
- Produccion Pecuaria
- Subproductos Pecuarios
- Gastos en Actividades Pecuarias
- Programas Sociales
- Ingresos del Trabajador Independiente
- Bienes y Servicios de Cuidados Personales
- Participación Ciudadana
- Gobernabilidad, Democracia y Transparencia
- Beneficios de ONGs

# Mapping for Department Codes

Use UBIGEO codes to map department codes to department names according tot he table below. However, **DO NOT USE** the first two digits of UBIGEO as department codes, instead, drop the last 4 digits of UBIGEO to get the department codes, given that some department codes have leading zeros.

| Code | Department  |
|------|-------------|
| 01 | AMAZONAS      |
| 02 | ANCASH        |
| 03 | APURIMAC      |
| 04 | AREQUIPA      |
| 05 | AYACUCHO      |
| 06 | CAJAMARCA     |
| 07 | CALLAO        |
| 08 | CUSCO         |
| 09 | HUANCAVELICA  |
| 10 | HUANUCO       |
| 11 | ICA           |
| 12 | JUNIN         |
| 13 | LA LIBERTAD   |
| 14 | LAMBAYEQUE    |
| 15 | LIMA          |
| 16 | LORETO        |
| 17 | MADRE DE DIOS |
| 18 | MOQUEGUA      |
| 19 | PASCO         |
| 20 | PIURA         |
| 21 | PUNO          |
| 22 | SAN MARTIN    |
| 23 | TACNA         |
| 24 | TUMBES        |
| 25 | UCAYALI       |