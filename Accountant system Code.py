# ACCOUNTANCY SYSTEM
# 1
# Record fees paid by students in a preliminary text file.

def record_fee():
    # opens ledger file to append details about payments
    fee_ledger = open('LedgerRecord.txt', 'a')

    # gets user's input about payment details
    first_name = input("Enter student's first name: ")
    last_name = input("Enter student's last name: ")
    tp = input('Enter student TP number: ')
    date = input('Enter date of payment: ')
    amount = int(input('Enter amount paid: '))
    description = input('Enter payment details: ')

    # form a new string with all the payment details taken from user
    NewString = (
                tp + ' | ' + first_name.upper() + ' | ' + last_name.upper() + ' | ' + date + ' | ' + description.upper() + ' | ' + str(
            amount) + '\n')

    # append new string to ledger file
    fee_ledger.write(NewString)

    print('Tuition fee has been recorded successfully.')

    # close the ledger file
    fee_ledger.close()


# 2
def outstanding_fee():
    # generates a list of students who having pending fee

    try:

        # open the master file for reading
        MasterFile = open("MasterFeeRecord.txt", "r")

        # read all contents from master file to a 2D array
        lines = MasterFile.readlines()  # read all lines in the file
        line_list = []
        main_list = []
        for line in lines:
            for i in range(6):
                line = line.strip()
                line_list = line.split(' | ')
            main_list.append(line_list)

        # close the master file
        MasterFile.close()

        # search the mainlist array for the required TP detail of pending
        print('Students with outstanding fee are as follows:')
        for row in range(len(main_list)):
            if main_list[row][5] == 'PENDING':
                print('1. Student TP: ', main_list[row][0])
                print('2. Student Name: ', main_list[row][1], main_list[row][2])
                print('3. Pending amount: ', main_list[row][4])
                print('\n')

    except FileNotFoundError:
        print('Invalid. File does not exist.')


# 3
def update_records(TPNum):
    # initialisations
    found = False
    completed = False
    change = False

    try:

        # open the master file for reading
        MasterFile = open("MasterFeeRecord.txt", "r")

        # read all contents from master file to a 2D array
        lines = MasterFile.readlines()  # read all lines in the file
        line_list = []
        main_list = []
        for line in lines:
            for i in range(6):
                line = line.strip()
                line_list = line.split(' | ')
            main_list.append(line_list)

        # close the master file
        MasterFile.close()

        # search the mainlist array for the required TP detail
        for row in range(len(main_list)):
            if main_list[row][0] == TPNum:
                found_index = row
                found = True

        # if found update the record
        if found == True:  # update record
            print('The details of the ID you entered is as follows:')
            print('1. Student TP: ', main_list[found_index][0])
            print('2. First name: ', main_list[found_index][1])
            print('3. Last name: ', main_list[found_index][2])
            print('4. Amount paid: ', main_list[found_index][3])
            print('5. Pending amount: ', main_list[found_index][4])
            print('6. Payment status ', main_list[found_index][5])

            while completed == False:
                detail_to_change = int(input('What detail would you like to update (1/2/3/4/5/6)? '))
                new_detail = input('Enter new detail to amend: ')
                main_list[found_index][detail_to_change - 1] = new_detail

                continue_choice = int(input('Would you like to update any other detail (1.yes/2.no)? '))

                if continue_choice == 1:
                    completed = False
                else:
                    completed = True

            change = True

            print('Successfully updated the record.')


        # if tp was not found ask to add new record or exit program
        else:
            print('Student details not found.')
            answer = int(input('Would you like to add a new record (1.yes/2.no)? '))

            if answer == 1:
                record_list = []

                tp = input('Enter TP number: ')
                first_name = input('Enter first name: ')
                last_name = input('Enter last name: ')
                amount = input('Enter amount paid: ')
                pending = input('Enter pending amount: ')
                status = input('Enter pending/paid: ')

                record_list = [tp, first_name, last_name, amount, pending, status]

                main_list.append(record_list)

                change = True

                print('New record has been successfully added.')

            else:
                print('Program will be exited.')
                
                change = False

        # if there was a change then rewrite the textfile with the amended array
        if change == True:
            MasterFile = open("MasterFeeRecord.txt", "w")

            for row in range(len(main_list)):
                New = ""
                for col in range(6):
                    New = New + main_list[row][col]
                    if col < 5:
                        New = New + ' | '
                New = New + '\n'

                MasterFile.write(New)

        MasterFile.close()

    except FileNotFoundError:
        print('Invalid. File does not exist.')


# 4
def receipt_generator():
    Filename = input('Enter student TP number: ')
    Name = input('Enter student name: ')

    receipt = open(Filename, 'w')

    # header
    receipt.write("Asia Pacific University SDN BHD\n\n")

    # file->array
    fee_ledger = open('LedgerRecord.txt', 'r')

    # read all contents from master file to a 2D array
    lines = fee_ledger.readlines()  # read all lines in the file
    line_list = []
    main_list = []
    for line in lines:
        for i in range(6):
            line = line.strip()
            line_list = line.split(' | ')
        main_list.append(line_list)

    # close the master file
    fee_ledger.close()

    # body
    receipt.write("Student TP No: ")
    receipt.write(Filename)
    receipt.write("\nStudent Name: ")
    receipt.write(Name)
    receipt.write("\n\nDate	|	Description	|	Amount\n")

    # search array
    Total = 0
    for row in range(len(main_list)):
        if main_list[row][0] == Filename:
            NewString = ""
            NewString = (NewString + main_list[row][3] + ' | ' + main_list[row][4] + ' | ' + main_list[row][5] + '\n')

            Total = Total + int(main_list[row][5])

            receipt.write(NewString)

    TotalString = ('\nTotal:' + str(Total))
    print(TotalString)
    receipt.write(TotalString)

    # footer
    receipt.write("\n\n*terms and conditions will be applied.")
    
    receipt.close()

    print('Receipt has been generated. Please find it as a text file in the folder titled under the student TP number.')


# 5
def financial_summary():
    # Summarize total fees collected versus outstanding fees

    # initializations
    TotalPaid = 0
    TotalPending = 0

    try:

        # open the master file for reading
        MasterFile = open("MasterFeeRecord.txt", "r")

        # read all contents from master file to a 2D array
        lines = MasterFile.readlines()  # read all lines in the file
        line_list = []
        main_list = []
        for line in lines:
            for i in range(6):
                line = line.strip()
                line_list = line.split(' | ')
            main_list.append(line_list)

        #     print(main_list)

        # close the master file
        MasterFile.close()

        # calculate total fee and total pending fee
        for row in range(len(main_list)):
            TotalPaid += int(main_list[row][3])
            TotalPending += int(main_list[row][4])


        print('Total fees collected:', TotalPaid)
        print('Total outstanding fees:', TotalPending)

        # if there is no pending fees then let the user know so.
        if TotalPending == 0:
            print('All fees have been collected. No outstanding payments.')

    except FileNotFoundError:
        print('Invalid. File does not exist.')


# Main menu for the accountant
def accountant_menu():
    while True:
        print("----------------------------")
        print("School Accountancy System")
        print("----------------------------")
        print("1. Record Tuition Fees")
        print("2. View Outstanding Fees")
        print("3. Update Payment Records")
        print("4. Issue Fee Receipts")
        print("5. View Financial Summary")
        print("6. Exit")
        print("----------------------------")
        choice = input("Choose: ")
        print("----------------------------")

        if choice == "1":
            record_fee()
        elif choice == "2":
            outstanding_fee()
        elif choice == "3":
            TPNum = input("Enter the student TP Number you would like to update: ")
            update_records(TPNum)
        elif choice == "4":
            receipt_generator()
        elif choice == "5":
            financial_summary()
        elif choice == "6":
            print("Program has successfully been exited.")
            break
        else:
            print("Invalid choice. Try again.")
            print("----------------------------")

#calling the function
accountant_menu()