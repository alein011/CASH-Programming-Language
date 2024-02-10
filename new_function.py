import matplotlib as m

def _round(expression):
    return round(expression, 2)

def simple_interest(principal, rate, time):
    try:
        rate /= 100
        return _round(principal * rate * time)
    except SyntaxError as se:
            error_message = str("Invalid Syntax")
    except (TypeError, ValueError) as e:
        print(f"Error calculating simple interest: {e}")
    except Exception as e:
        print(f"{e}")


def compound_interest(principal, rate, time, compounding_periods = 1):
    try:
        rate/=100
        return _round(principal * (1 + rate / compounding_periods) ** (compounding_periods * time) - principal)
    except SyntaxError as se:
        error_message = str("Invalid Syntax")
    except (TypeError, ValueError) as e:
        print(f"Error calculating compound interest: {e}")
    except Exception as e:
        print(f"{e}")
     
        
def simple_annuity(payment, rate, time, frequency):
    try:
        rate = rate/100
        n = round(_round(time) * frequency, 2)
        j = round(rate / frequency, 4)
        return _round(payment * ((1 - (1 + rate) ** -n)) / (j))
    except SyntaxError as se:
        error_message = str("Invalid Syntax")
    except (TypeError, ValueError) as e:
        print(f"Error calculating simple annuity: {e}")
     
        
def stock_dividend(total_div, total_share):
    try:
        return total_div / total_share
    except SyntaxError as se:
        error_message = str("Invalid Syntax")
    except ZeroDivisionError:
        print("Error: Total shares cannot be zero.")
        return None
    except (TypeError, ValueError):
        print("Error: Invalid input. Make sure total_div and total_share are numeric.")
        return None


def div_pershare(div_percentage, par_value, share_num):
    try:
        return _round(div_percentage * par_value * share_num)
    except SyntaxError as se:
        error_message = str("Invalid Syntax")
    except (TypeError, ValueError):
        print("Error: Invalid input. Make sure div_percentage, par_value, and share_num are numeric.")
        return None


def yield_ratio(div_per_share, market_val):
    try:
        return _round(div_per_share / market_val)
    except SyntaxError as se:
        error_message = str("Invalid Syntax")
    except ZeroDivisionError:
        print("Error: Market value cannot be zero.")
        return None
    except (TypeError, ValueError):
        print("Error: Invalid input. Make sure div_per_share and market_val are numeric.")
        return None


def coupon_payment(principal, rate, frequency):
    try:
        rate /= 100
        return _round(principal * rate / frequency)
    except SyntaxError as se:
        error_message = str("Invalid Syntax")
    except (TypeError, ValueError):
        print("Error: Invalid input. Make sure principal, rate, and frequency are numeric.")
        return None


def coupon_amount(face_value, rate, frequency):
    try:
        rate /= 100
        return _round(face_value * rate / frequency)
    except SyntaxError as se:
        error_message = str("Invalid Syntax")
    except (TypeError, ValueError):
        print("Error: Invalid input. Make sure face_value, rate, and frequency are numeric.")
        return None


def loan_principal(future_value, rate, time, frequency):
    try:
        rate /= 100
        return _round(future_value / ((1 + rate / frequency) ** (time * frequency)))
    except SyntaxError as se:
        error_message = str("Invalid Syntax")
    except (ZeroDivisionError, ValueError):
        print("Error: Invalid input. Make sure rate, time, and frequency are non-zero numeric values.")
        return None


def loanfv_pin(principal, rate, frequency):
    try:
        rate /= 100
        return _round(principal * (1 + rate / frequency))
    except SyntaxError as se:
        error_message = str("Invalid Syntax")
    except (TypeError, ValueError):
        print("Error: Invalid input. Make sure principal, rate, and frequency are numeric.")
        return None


def loanfv_rtm(regular_payment, time, frequency):
    try:
        return _round(regular_payment * time * frequency)
    except SyntaxError as se:
        error_message = str("Invalid Syntax")
    except (TypeError, ValueError):
        print("Error: Invalid input. Make sure regular_payment, time, and frequency are numeric.")
        return None
    
def get(prompt=""):
    try:
        if not isinstance(prompt, str):
            return input(prompt)
    except Exception as e:
            print(f"Error: {str(e)}")
