def convert_to_ml(amount):

    amounts = []
    amounts = amount.split(" ")
    amountTotal = 0

    if amounts[1].lower() == "ml":
        amountTotal += float(amounts[0])
    elif amounts[1].lower() == "oz":
        amountTotal += float(amounts[0]) * 29.5735
    elif amounts[1].lower() == "gallon":
        amountTotal += float(amounts[0]) * 3785.41
    elif amounts[1].lower() == "liter":
        amountTotal += float(amounts[0]) * 1000
    return amountTotal
    