import matplotlib.pyplot as plt
import numpy as np

def __round(value):
    return round(value, 3)

def plot_sint(*args):
    try:
        # Plotting simple interest over time for each set of inputs
        for i, input_set in enumerate(args, start=0):
            principal, rate, time = input_set
            rate /= 100
            time_periods = np.arange(1, time + 1)
            simple_interest_values = (principal * rate * time_periods + principal)

            # Plotting simple interest over time with custom label ('a', 'b', 'c', etc.)
            label = f'Interest {chr(ord("A") + i)}'  # Converts integer index to corresponding ASCII character
            plt.plot(time_periods, simple_interest_values, label=label, marker='o')
            print(f'Interest {chr(ord("A") + i)}: {simple_interest_values[-1]:.3f}')

        # Adding labels and title
        plt.xlabel('Time (Years)')
        plt.ylabel('Interest Amount')
        plt.title('Simple Interest Over Time')

        # Adding a legend
        plt.legend()

        # Display the graph
        plt.show()

    except SyntaxError as se:
        error_message = str("Invalid Syntax")
        print(f"SyntaxError: {error_message}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    
    

def plot_cint(*args):
    try:
        # Plotting compound interest over time for each set of inputs
        for i, input_set in enumerate(args, start=1):
            principal, rate, time, compounding_periods = input_set
            rate /= 100
            time_values = np.arange(1, time + 1)
            compound_interest_values = ((principal * (1 + rate / compounding_periods) ** (compounding_periods * time_values)) - principal) 
    

            # Using a character based on the index for the legend label
            label = f'Interest {chr(ord("A") + i - 1)}'
            plt.plot(time_values, compound_interest_values, label=label, marker='o')
            print(f'Interest {chr(ord("A") + i - 1)}: {compound_interest_values[-1]:.3f}')

        # Adding labels and title
        plt.xlabel('Time (Years)')
        plt.ylabel('Interest Amount')
        plt.title('Compound Interest Over Time')

        # Adding a legend
        plt.legend()

        # Display the graph
        plt.show()

    except SyntaxError as se:
        error_message = str("Invalid Syntax")
        print(f"SyntaxError: {error_message}")
    except Exception as e:
        print(f"An error occurred: {e}")
    


def plot_sc(simple_interest_list, compound_interest_list):
    # Ensure both lists have the same length
    if len(simple_interest_list) != len(compound_interest_list):
        raise ValueError("Both input lists must have the same length.")

    # Plotting simple interest and compound interest over time for each set of inputs
    for i, (simple_params, compound_params) in enumerate(zip(simple_interest_list, compound_interest_list), start=1):
        # Extracting parameters for simple interest
        simple_principal, simple_rate, simple_time = simple_params
        simple_rate/=100
        simple_time_periods = np.arange(1, simple_time + 1)
        simple_interest_values = (simple_principal * simple_rate * simple_time_periods + simple_principal)

        # Extracting parameters for compound interest
        compound_principal, compound_rate, compound_time, compound_periods = compound_params
        compound_rate/=100
        compound_time_values = np.arange(1, compound_time + 1)
        compound_interest_values = ((compound_principal * (1 + compound_rate / compound_periods) ** (compound_periods * compound_time_values)))

        # Using a character based on the index for the legend label
        # Plotting simple interest
        plt.plot(simple_time_periods, simple_interest_values, label=f'Simple Interest', marker='o')

        # Plotting compound interest
        plt.plot(compound_time_values, compound_interest_values, label=f'Compound Interest', marker='o')
        
        print(f'Simple Interest {chr(ord("A") + i - 1)}: {simple_interest_values[-1]:.3f}')
        print(f'Compound Interest {chr(ord("A") + i - 1)}: {compound_interest_values[-1]:.3f}')

    # Adding labels and title
    plt.xlabel('Time (Years)')
    plt.ylabel('Interest Amount')
    plt.title('Simple Interest vs Compound Interest')

    # Adding a legend
    plt.legend()

    # Display the graph
    plt.show()
    

def plot_loan(*args):
    """
    Visualizes the future value of multiple loans using a bar graph for direct comparison.

    Parameters:
    - *args: Variable number of arguments representing sets of parameters for each loan.
      Each set includes principal, rate, time, and an optional monthly payment.
    """
    bar_width = 0.50
    index = np.arange(len(args))
    
    # Plotting the future value for each loan as a bar
    for i, params in enumerate(args, start=1):
        principal, rate, time, monthly_payment = params
        rate /= 100

        # Calculate future value of the loan
        if monthly_payment is not None:
            interest_rate_per_period = rate / 12
            num_payments = time * 12
            future_value = principal * ((1 + interest_rate_per_period)**num_payments) + monthly_payment * (((1 + interest_rate_per_period)**num_payments) - 1) / interest_rate_per_period
        else:
            future_value = principal * (1 + rate)**time
            
        (future_value)

        # Plotting the future value for each loan as a bar
        label = f'Loan {chr(ord("A") + i -1)}'
        plt.bar(i, future_value, bar_width, label=label, color = 'tab:blue')
        
        print(f'Loan {chr(ord("A") + i -1)}: {future_value:.3f}')

    # Adding labels and title
    plt.xlabel('Loans')
    plt.ylabel('Future Value')
    plt.title('Future Value of Loan')
    
    plt.xticks(index + 1, [f'Loan {chr(ord("A") + i -1)}' for i in range(1, len(args) + 1)])


    # Display the graph
    plt.show()
    
    
def plot_yr(*args):
    """
    Visualizes the yield ratio of multiple investments using a bar graph for direct comparison.

    Parameters:
    - *args: Variable number of arguments representing sets of parameters for each investment.
      Each set includes initial investment, total return, and an optional label.
    """
    bar_width = 0.50
    index = np.arange(len(args))
    
    # Plotting the yield ratio for each investment as a bar
    for i, params in enumerate(args, start=1):
        initial_investment, total_return = params

        # Calculate yield ratio
        yield_ratio = (initial_investment / total_return * 100)
        
        (yield_ratio)

        # Plotting the yield ratio for each investment as a bar
        label = f'Investment {chr(ord("A") + i - 1)}'
        plt.bar(i, yield_ratio, bar_width, label = label, color = 'tab:blue')
        print(f'Investment {chr(ord("A") + i - 1)}: {yield_ratio:.3f}')

    # Adding labels and title
    plt.xlabel('Investments')
    plt.ylabel('Yield Ratio (in %)')
    plt.title('Yield Ratio of Investment')

    # Adding x-axis ticks
    plt.xticks(index + 1, [params[2] if len(params) > 2 else f'Investment {chr(ord("A") + i - 1)}' for i, params in enumerate(args, start=1)])



    # Display the graph
    plt.show()
    
    

def plot_coup(*args):
    """
    Visualizes the total coupon amounts for multiple bonds using a bar graph.

    Parameters:
    - *args: Variable number of arguments, each representing a set of parameters for a bond.
      Each set includes face value, coupon rate.
    """
    # Calculate the total coupon amount for each set of parameters
    total_coupon_amounts = [(arg[0] * arg[1]) for arg in args]

    # Plotting the total coupon amounts for each bond
    plt.bar(range(1, len(args) + 1), total_coupon_amounts, width=0.4, tick_label=[f'Bond {chr(ord("A") + i -1)}' for i in range(1, len(args) + 1)])
    
    for i, amount in enumerate(total_coupon_amounts, start=1):
        print(f'Bond {chr(ord("A") + i - 1)}: {amount:.3f}')

    # Adding labels and title
    plt.xlabel('Bonds')
    plt.ylabel('Total Coupon Amount')
    plt.title('Total Coupon Amount for Bond')

    # Display the graph
    plt.show()
    
    




