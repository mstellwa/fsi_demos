"""
Date and quarter utility functions for dynamic data generation
"""

from datetime import datetime, timedelta
from typing import List, Tuple
from config import DemoConfig


def get_current_quarter() -> str:
    """Get the current quarter in YYYY-QN format"""
    now = datetime.now()
    quarter = (now.month - 1) // 3 + 1
    return f"{now.year}-Q{quarter}"


def get_previous_quarter(quarter_str: str) -> str:
    """Get the previous quarter from a given quarter string"""
    year, quarter = quarter_str.split('-Q')
    year = int(year)
    quarter = int(quarter)
    
    if quarter == 1:
        return f"{year - 1}-Q4"
    else:
        return f"{year}-Q{quarter - 1}"


def get_next_quarter(quarter_str: str) -> str:
    """Get the next quarter from a given quarter string"""
    year, quarter = quarter_str.split('-Q')
    year = int(year)
    quarter = int(quarter)
    
    if quarter == 4:
        return f"{year + 1}-Q1"
    else:
        return f"{year}-Q{quarter + 1}"


def get_historical_quarters(num_quarters: int = None) -> List[str]:
    """
    Generate a list of historical quarters based on current date
    
    Args:
        num_quarters: Number of quarters to generate (defaults to config)
    
    Returns:
        List of quarter strings in YYYY-QN format, most recent first
    """
    if num_quarters is None:
        num_quarters = DemoConfig.NUM_HISTORICAL_QUARTERS
    
    current_quarter = get_current_quarter()
    quarters = [current_quarter]
    
    quarter = current_quarter
    for _ in range(num_quarters - 1):
        quarter = get_previous_quarter(quarter)
        quarters.append(quarter)
    
    return quarters


def get_quarter_date_range(quarter_str: str) -> Tuple[datetime, datetime]:
    """
    Get the start and end dates for a given quarter
    
    Args:
        quarter_str: Quarter in YYYY-QN format
    
    Returns:
        Tuple of (start_date, end_date) as datetime objects
    """
    year, quarter = quarter_str.split('-Q')
    year = int(year)
    quarter = int(quarter)
    
    # Quarter start months: Q1=Jan, Q2=Apr, Q3=Jul, Q4=Oct
    start_month = (quarter - 1) * 3 + 1
    start_date = datetime(year, start_month, 1)
    
    # End date is start of next quarter minus 1 day
    if quarter == 4:
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(year, start_month + 3, 1) - timedelta(days=1)
    
    return start_date, end_date


def get_dynamic_date_range() -> Tuple[datetime, datetime]:
    """
    Get dynamic date range covering all historical quarters
    
    Returns:
        Tuple of (start_date, end_date) covering the historical period
    """
    quarters = get_historical_quarters()
    oldest_quarter = quarters[-1]  # Last in list is oldest
    newest_quarter = quarters[0]   # First in list is newest
    
    start_date, _ = get_quarter_date_range(oldest_quarter)
    _, end_date = get_quarter_date_range(newest_quarter)
    
    return start_date, end_date


def quarter_to_fiscal_quarter(quarter_str: str) -> str:
    """
    Convert quarter string to fiscal quarter format used in data
    This is currently the same format, but keeping for consistency
    """
    return quarter_str


# Example usage and testing
if __name__ == "__main__":
    print("Current quarter:", get_current_quarter())
    print("Historical quarters:", get_historical_quarters())
    print("Date range:", get_dynamic_date_range())
    
    # Test quarter operations
    current = get_current_quarter()
    print(f"Current: {current}")
    print(f"Previous: {get_previous_quarter(current)}")
    print(f"Next: {get_next_quarter(current)}")
    
    # Test quarter date ranges
    for quarter in get_historical_quarters(4):
        start, end = get_quarter_date_range(quarter)
        print(f"{quarter}: {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}")
