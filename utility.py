import datetime

class Utility:
    @staticmethod
    def get_months_between(start_date: datetime, end_date: datetime):
        # Ensure the start_date is less than or equal to the end_date
        if start_date > end_date:
            raise ValueError("The start date must be before or the same as the end date")

        months = []
        # Current date to keep track of the month currently being processed
        current_date = start_date.replace(day=1)  # We set the day to 1 to ensure we always start from the first day of the month

        while current_date <= end_date:
            months.append(current_date)
            # Move to the next month. The "%Y-%m-%d" format ensures we are working with the first day of each month.
            next_month = current_date.month + 1 if current_date.month < 12 else 1
            next_year = current_date.year if current_date.month < 12 else current_date.year + 1
            current_date = current_date.replace(month=next_month, year=next_year)

        return months
