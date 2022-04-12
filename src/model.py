from typing import Optional
from pydantic import BaseModel

# DEV URL 1: https://www.cdp.net/en/formatted_responses/responses?campaign_id=74241094&discloser_id=892976&locale=en&organization_name=Air+Liquide&organization_number=432&program=Investor&project_year=2021&redirect=https%3A%2F%2Fcdp.credit360.com%2Fsurveys%2F2021%2Fdbbr64mv%2F145645&survey_id=73557641
# DEV URL 2: https://www.cdp.net/en/formatted_responses/responses?campaign_id=74241094&discloser_id=897126&locale=en&organization_name=BNP+Paribas&organization_number=1907&program=Investor&project_year=2021&redirect=https%3A%2F%2Fcdp.credit360.com%2Fsurveys%2F2021%2Fdbbr64mv%2F142019&survey_id=73557641


class Customer(BaseModel):
    url: str
    query_year: int
    query_country: str
    company_name: str
    is_completed: bool = False
    scraped_at: str
    # C0.2
    reporting_start_date: Optional[str] = None
    reporting_end_date: Optional[str] = None
    # C1.1a
    owner_board: Optional[str] = None
    # C1.1b
    is_owner_board_detail: Optional[bool] = None
    # C1.2
    owner_names: Optional[str] = None
    # C6.1 (unit: metrics ton CO2e)
    scope_1_y0: Optional[float] = None
    scope_1_y1: Optional[float] = None
    scope_1_y2: Optional[float] = None
    scope_1_y3: Optional[float] = None
    # C6.3
    scope_2_location_y0: Optional[float] = None
    scope_2_location_y1: Optional[float] = None
    scope_2_location_y2: Optional[float] = None
    scope_2_location_y3: Optional[float] = None
    scope_2_market_y0: Optional[float] = None
    scope_2_market_y1: Optional[float] = None
    scope_2_market_y2: Optional[float] = None
    scope_2_market_y3: Optional[float] = None
    # C6.5 (scope 3)
    purchase_goods: Optional[float] = None
    capital_goods: Optional[float] = None
    fuel_energy: Optional[float] = None
    upstream_transportation: Optional[float] = None
    waste_ops: Optional[float] = None
    business_travel: Optional[float] = None
    commute: Optional[float] = None
    upstream_leasing: Optional[float] = None
    downstream_transportation: Optional[float] = None
    processing_of_sold_products: Optional[float] = None
    use_of_sold_products: Optional[float] = None
    end_of_life_sold_products: Optional[float] = None
    downstream_leasing: Optional[float] = None
    franchises: Optional[float] = None
    others_upstream: Optional[float] = None
    # C11.1a
    regulation: Optional[str] = None
    # C11.1b
    ets_name_1: Optional[str] = None
    scope_1_emissions_coverage_1: Optional[float] = None
    scope_2_emissions_coverage_1: Optional[float] = None
    allowances_allocated_1: Optional[float] = None
    allowances_purchased_1: Optional[float] = None
    verified_scope_1_emissions_1: Optional[float] = None
    verified_scope_2_emissions_1: Optional[float] = None
    ets_name_2: Optional[str] = None
    scope_1_emissions_coverage_2: Optional[float] = None
    scope_2_emissions_coverage_2: Optional[float] = None
    allowances_allocated_2: Optional[float] = None
    allowances_purchased_2: Optional[float] = None
    verified_scope_1_emissions_2: Optional[float] = None
    verified_scope_2_emissions_2: Optional[float] = None
    ets_name_3: Optional[str] = None
    scope_1_emissions_coverage_3: Optional[float] = None
    scope_2_emissions_coverage_3: Optional[float] = None
    allowances_allocated_3: Optional[float] = None
    allowances_purchased_3: Optional[float] = None
    verified_scope_1_emissions_3: Optional[float] = None
    verified_scope_2_emissions_3: Optional[float] = None
    # C11.2
    has_crc_y0: Optional[bool] = None
    # C11.2a
    crc_origin_1: Optional[str] = None
    project_type_1: Optional[str] = None
    project_id_1: Optional[str] = None
    verify_standards_1: Optional[str] = None
    credits_1: Optional[float] = None
    purpose_1: Optional[str] = None
    crc_origin_2: Optional[str] = None
    project_type_2: Optional[str] = None
    is_project_id_2: Optional[str] = None
    verify_standards_2: Optional[str] = None
    credits_2: Optional[float] = None
    purpose_2: Optional[str] = None
    crc_origin_3: Optional[str] = None
    project_type_3: Optional[str] = None
    is_project_id_3: Optional[str] = None
    verify_standards_3: Optional[str] = None
    credits_3: Optional[float] = None
    purpose_3: Optional[str] = None
    crc_origin_4: Optional[str] = None
    project_type_4: Optional[str] = None
    is_project_id_4: Optional[str] = None
    verify_standards_4: Optional[str] = None
    credits_4: Optional[float] = None
    purpose_4: Optional[str] = None
    # C11.3a
    ghg_scope: Optional[str] = None
    actual_price: Optional[float] = None
