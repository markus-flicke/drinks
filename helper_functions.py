from splitwise import Splitwise
from splitwise.expense import Expense, ExpenseUser
from secrets import CONSUMER_KEY, CONSUMER_SECRET, API_KEY, MARKUS_USER_ID
import logging
logging.basicConfig(level=logging.DEBUG)


def add_expense(amount, user_id, description, group_id):
    """
    Adds an expense and credits the amount to me (Markus) in euros. 

    example: add_expense(15, 48123799, "coke", 32463151)
    """
    cost = str(float(amount))
    
    s = Splitwise(CONSUMER_KEY, CONSUMER_SECRET, api_key=API_KEY)
    expense = Expense()
    expense.setGroupId(group_id)
    expense.setCost(cost)
    expense.setDescription(description)
    user1 = ExpenseUser()
    user1.setId(user_id)
    user1.setPaidShare('0')
    user1.setOwedShare(cost)
    user2 = ExpenseUser()
    user2.setId(MARKUS_USER_ID)
    user2.setPaidShare(cost)
    user2.setOwedShare('0')
    expense.addUser(user1)
    expense.addUser(user2)
    expense.setCurrencyCode("EUR")
    nExpense, errors = s.createExpense(expense)
    if errors:
        print(errors.getErrors())
    print(nExpense.getId())

def getGroupMembers(group_id):
    """
    Returns group members in the format [(user_id, username), ... , (user_id, username)]
    """
    s = Splitwise(CONSUMER_KEY, CONSUMER_SECRET, api_key=API_KEY)
    group = s.getGroup(group_id)
    members = group.getMembers()
    return sorted([(member.getId(), f"{member.getFirstName()}{(' ' + member.getLastName()) if member.getLastName() else ''}") for member in members], key = lambda x: x[1])


if __name__=='__main__':
    print(getGroupMembers(32463151))