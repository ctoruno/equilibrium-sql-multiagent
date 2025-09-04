# GEIH 2024
The Gran Encuesta Integrada de Hogares (GEIH) 2024, conducted by Colombia’s National Administrative Department of Statistics (DANE), is the country’s largest household survey, with an annual sample of about 315,000 households. Building on decades of labor and living conditions surveys and redesigned in 2022 using the 2018 Census framework, the GEIH provides comprehensive information on the labor market, household incomes, monetary poverty, and extreme poverty. It captures employment, unemployment, underemployment, income sources, and population characteristics such as education, health coverage, ethnicity, and other demographic factors, producing reliable indicators essential for analyzing labor dynamics and informing public policy.

## Tables
The geih-2024 database is composed by 8 different tables:
- DBF_GECH_45_21
- DBF_GECH_6_10
- DBF_GECH_6_13
- DBF_GECH_6_234
- DBF_GECH_6_5
- DBF_GECH_6_67
- DBF_GECH_6_8
- DBF_GECH_6_9

### DBF_GECH_6_5
**Module Name**: Fuerza de Trabajo

**Description:**
Individual labor force participation module capturing employment status, job search activities, work availability, and labor market engagement for all persons of working age.

**Business Domain:** Labor Market & Employment Analytics

**Identifiers**: Each row represents an individual person of working age. Records are uniquely identified by the combination: PER, MES, DIRECTORIO, HOGAR, ORDEN.

**Expansion Factor**: FEX_C18 provides the statistical weight for population-level estimates and projections.

**Key Topics Covered:**
- Employment Classification: Primary activity during reference week, work engagement patterns
- Job Search Behavior: Active job search in last 4 weeks, search methods used, preparatory activities for starting a business
- Work Availability: Desire to work, reasons for not searching, availability for immediate work, work experience in last 12 months
- Inactive Population Analysis: Reasons for not seeking employment despite desire to work
- Recent Work History: Work episodes of at least 2 consecutive weeks in the last year, post-employment job search patterns

### DBF_GECH_6_67
**Module Name**: Ocupados

**Description:**
Comprehensive employment conditions and compensation module capturing detailed job characteristics, working arrangements, income sources, social protection coverage, and employment quality indicators for employed individuals.

**Business Domain:** Labor Market & Employment Analytics

**Identifiers**: Each row represents an employed individual. Records are uniquely identified by the combination: PER, MES, DIRECTORIO, HOGAR, ORDEN.

**Expansion Factor**: FEX_C18 provides the statistical weight for population-level estimates and projections.

**Key Topics Covered:**
- Employment Contracts: Contract existence and types, contract satisfaction, labor rights, job tenure and stability
- Labor Intermediation: Direct vs. subcontracted employment, types of intermediary entities (temporary services, work cooperatives), employment acquisition channels including internet platforms
- Compensation Structure: Monthly wages, overtime pay, bonuses and benefits, in-kind payments, subsidies, annual benefits
- Working Conditions: Weekly and actual hours worked, workplace location, job security perceptions, work-family balance compatibility, multiple job holding
- Social Protection: Pension system affiliation and contributions, occupational risk insurance, family compensation fund membership, health insurance coverage through employment
- Employment Quality: Desire for additional hours, active search for more hours, union/guild membership, job acquisition methods, commuting patterns and transportation modes

### DBF_GECH_6_8
**Module Name**: No Ocupados

**Description:**
Unemployed population characteristics module capturing job search duration, employment preferences, work availability, employment history, and social protection status for individuals actively seeking employment.

**Business Domain:** Labor Market & Unemployment Analytics

**Identifiers**: Each row represents an unemployed individual. Records are uniquely identified by the combination: PER, MES, DIRECTORIO, HOGAR, ORDEN.

**Expansion Factor**: FEX_C18 provides the statistical weight for population-level estimates and projections.

**Key Topics Covered:**
- Unemployment Duration: Weeks spent searching for work, availability patterns for starting work immediately or within specific timeframes
- Job Search Preferences: Desired occupational position, reservation wage, hours available for work
- Employment History: Previous work experience, time since last employment, reasons for leaving last job, last job characteristics
- Social Protection Access: Current unemployment benefit receipt, pension system contributions, health insurance coverage, type of pension regime affiliation
- Recent Labor Income: Income received from work in the previous month despite unemployment status
- Previous Job Details: Industry classification of last workplace, occupation codes, business formality indicators of previous employer

### DBF_GECH_6_9
**Module Name**: Otras Formas de Trabajo

**Description:**
Alternative work forms and unpaid activities module capturing time allocation for unpaid care work, volunteer activities, internships, subsistence production, and community service across different household types and locations.

**Business Domain:** Time Use & Unpaid Work Analytics

**Identifiers**: Each row represents an individual person. Records are uniquely identified by the combination: PER, MES, DIRECTORIO, HOGAR, ORDEN.

**Expansion Factor**: FEX_C18 provides the statistical weight for population-level estimates and projections.

**Key Topics Covered:**
- Unpaid Care Work: Time spent on household activities across different locations, intensity measured in days per period and hours per day
- Educational Work Experience: Internships and work placements, apprenticeship contracts, public vs. private educational institutions
- Subsistence Production: Food production for household consumption, clothing production for household members, time allocation and estimated market value of production
- Resource Collection: Water collection for household use (rural areas), firewood gathering, mineral extraction for household consumption, agricultural activities for subsistence (planting, watering, harvesting)
- Community Engagement: Voluntary community work, institutional volunteering through non-profit organizations, participation in social organization meetings
- Infrastructure Development: Home construction and improvement activities for own household, estimated value of self-produced goods and services

### DBF_GECH_6_10
**Module Name**: Otros Ingresos e Impuestos

**Description:**
Non-labor income and tax obligations module capturing rental income, pensions, transfers, financial returns, government program benefits, and tax payments for comprehensive household income analysis.

**Business Domain:** Income & Transfer Analytics

**Identifiers**: Each row represents an individual person. Records are uniquely identified by the combination: PER, MES, DIRECTORIO, HOGAR, ORDEN.

**Expansion Factor**: FEX_C18 provides the statistical weight for population-level estimates and projections.

**Key Topics Covered:**
- Property Income: Rental income from real estate and equipment, pension and retirement payments, alimony and child support receipts, monthly amounts and payment patterns
- Transfer Income: Domestic monetary transfers from other households, international remittances from abroad, institutional aid, specific program transfers (Más Familias en Acción, Jóvenes en Acción, Colombia Mayor)
- Financial Income: Interest from loans and time deposits, dividends and investment returns, severance payments and severance interest, capital gains from asset sales
- Tax Obligations: Property tax payments, improvement tax contributions, vehicle tax payments, income tax and complementary taxes, taxes on extraordinary gain
- Asset Ownership: Real estate property ownership status, estimated tax burden distribution across different tax categories

### DBF_GECH_6_13
**Module Name**: Migración

**Description:**
Migration patterns and mobility history module capturing place of birth, nationality, international migration experience, internal mobility, and migration motivations for understanding population movements and demographic changes.

**Business Domain:** Migration & Demographics Analytics

**Identifiers**: Each row represents an individual household member. Records are uniquely identified by the combination: PER, MES, DIRECTORIO, HOGAR, ORDEN.

**Expansion Factor**: FEX_C18 provides the statistical weight for population-level estimates and projections.

**Key Topics Covered:**
- Place of Birth & Nationality: Birth location, nationality status, arrival timing to Colombia for foreign-born individuals
- International Migration History: Experience living abroad for more than 6 months, work experience during international residence, destination countries for labor migration, duration and timing of international work episodes
- Recent Mobility Patterns: Residence location 5 years ago and 12 months ago, urban/rural classification of previous residence locations, identification of recent migrants and return migrants
- Migration Motivations: Primary reasons for residential changes
- Return Migration: Timing of departure and return to specific countries, multiple international migration episodes, integration of circular migration patterns

### DBF_GECH_6_234
**Module Name**: Características Generales, Seguridad Social en Salud y Educación

**Description:**
Comprehensive individual demographics, health insurance, functional limitations, educational attainment, COVID-19 impacts, and identity characteristics module for all household members providing foundational sociodemographic information.

**Business Domain:** Demographics, Health & Education Analytics

**Identifiers**: Each row represents an individual household member. Records are uniquely identified by the combination: PER, MES, DIRECTORIO, HOGAR, ORDEN.

**Expansion Factor**: FEX_C18 provides the statistical weight for population-level estimates and projections.

**Key Topics Covered:**
- Basic Demographics: Age, sex assigned at birth, household relationship to head, parental co-residence status, marital status and spouse co-residence, informant identification for survey responses
- Ethnic & Cultural Identity: Ethnic self-recognition, indigenous group affiliation, rural identity
- Health Insurance & Disability: Health system affiliation, payment responsibility and costs, functional limitations assessment across eight domains
- Educational Background: Literacy status, current school enrollment, educational institution type (public/private), highest educational level achieved, specific degree/diploma obtained, field of study for professional programs
- COVID-19 Impact Assessment: Multiple dimensions of pandemic effects
- Sexual Orientation & Gender Identity: Attraction patterns, gender identity self-recognition, derived indicators for LGBTI population analysis and social inclusion monitoring

### DBF_GECH_45_21
**Module Name**: Datos del Hogar y la Vivienda

**Description:**
Housing conditions, household characteristics, public services access, and financial inclusion module capturing dwelling quality, infrastructure, tenure arrangements, and economic assets at the household level.

**Business Domain:** Housing & Household Analytics

**Identifiers**: Each row represents a household within a dwelling. Records are uniquely identified by the combination: PER, MES, DIRECTORIO, HOGAR.

**Expansion Factor**: FEX_C18 provides the statistical weight for population-level estimates and projections.

**Key Topics Covered:**
- Housing Quality: Dwelling type classification, construction materials for walls and floors, overall housing quality indicators for habitability assessment
- Public Services Access: Availability and quality of basic services (electricity with stratification, natural gas, sewerage, waste collection frequency, aqueduct), service coverage patterns
- Household Space: Number of rooms available to household, sleeping room allocation, overcrowding indicators, number of households sharing the dwelling
- Sanitation Infrastructure: Type of sanitary service, exclusive vs. shared access, waste disposal methods
- Water & Energy Sources: Primary water source for human consumption, cooking fuel types, food preparation areas
- Housing Tenure: Property ownership status, mortgage payments, estimated property values, rental costs
- Financial Inclusion: Household access to financial products, banking relationships and credit access patterns
