# ENAHO 2024
The 2024 National Household Survey (ENAHO), conducted by the National Institute of Statistics and Informatics (INEI), is an ongoing survey that has measured the living conditions, poverty, and well-being of Peruvian households since 1995. Its coverage is national, encompassing urban and rural areas of the 24 departments and the Constitutional Province of Callao, through mixed interviews (in-person and by telephone). The 2024 sample comprises 36,594 households and allows for the generation of indicators on poverty, employment, health, education, spending, social programs, governance, and other social and economic aspects, with inference levels from the national to the departmental level.

## Tables
The enaho-2024 database is composed by 11 different tables:
- Enaho01-2024-100
- Enaho01-2024-200
- Enaho01-2024-601
- Enaho01-2024-603
- Enaho01-2024-604
- Enaho01-2024-605
- Enaho01-2024-609
- Enaho01-2024-612
- Enaho01A-2024-300
- Enaho01A-2024-400
- Enaho01A-2024-500

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

### Enaho01-2024-200
**Module Name**: Características de la Vivienda y del Hogar (Módulo 200)

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

### Enaho01-2024-601
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

### Enaho01-2024-603
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

### Enaho01-2024-604
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

### Enaho01-2024-605
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

### Enaho01-2024-609
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

### Enaho01-2024-612
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

### Enaho01A-2024-300
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

### Enaho01A-2024-400
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

### Enaho01A-2024-500
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
