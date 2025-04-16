import pymysql as db
from datetime import datetime, timedelta


cnx = db.connect(user='root', password='bhargavi',
                 host='127.0.0.1',
                 database='lib',
                 charset='utf8')

print("Connected successfully")
cmd = cnx.cursor()

while True:
    print('\n1. Manage Books')
    print('2. Manage Borrowers')
    print('3. Issue Books')
    print('4. Return Books')
    print('5. View Logs')
    print('6. Exit')
    c = int(input('Enter your choice: '))

    if c == 1: 
        while True:
            print('\n1. Add Book')
            print('2. View All Books')
            print('3. Search Book')
            print('4. Update Book Status')
            print('5. Delete Book')
            print('6. Exit')
            ch = int(input('Enter choice: '))

            if ch == 1: 
                Title = input('Enter Book Title: ')
                Author = input('Enter Author: ')
                ISBN = int(input('Enter ISBN: '))
                Genre = input('Enter Genre: ')
                Copies = int(input('Enter Copies: '))

                q = "INSERT INTO books (Title, Author, ISBN, Genre, Copies, Status) VALUES (%s, %s, %s, %s, %s, 'N')"
                cmd.execute(q, (Title, Author, ISBN, Genre, Copies))
                cnx.commit()
                print("---------------------------------------")
                print("Book added successfully!")
                print("---------------------------------------")

            elif ch == 2: 
                cmd.execute("SELECT * FROM books")
                print("----------------------------------------------------------")
                for row in cmd.fetchall():
                    print(row)
                print("----------------------------------------------------------")

            elif ch == 3:
                print('1.Search by title')
                print('2.Search by ISBN')
                print('3.Search by author')
                print('4.Search by genre')
                sch=int(input('Enter choice '))
                if sch == 1:
                    title = input("Enter Book Title to search: ")
                    q = "SELECT * FROM books WHERE Title LIKE %s AND Status = 'N'"
                    cmd.execute(q, ('%' + title + '%',))
                    result = cmd.fetchall()
                    if result:
                        print("---------------------------------------------------------")
                        for row in result:
                            print(row)
                            print("---------------------------------------------------------")
                    else:
                        print("---------------------------------------------------------")
                        print("Book not found or unavailable.")
                        print("---------------------------------------------------------")
                elif sch == 2:
                    isbno = int(input('Enter the ISBN number'))
                    q = f"select * from books where status = 'N' and ISBN = {isbno}"
                    cmd.execute(q)
                    result = cmd.fetchall()
                    if result:
                        print("---------------------------------------------------------")
                        for row in result:
                            
                            print(row)
                        print("---------------------------------------------------------")
                    else:
                        print("---------------------------------------------------------")
                        print("Book not found or unavailable.")
                        print("---------------------------------------------------------")
                        
                elif sch == 3:
                    authorname = input('Enter the author name ')
                    q =f"select * from books where status = 'N' and Author = '{authorname}'"
                    cmd.execute(q)
                    result = cmd.fetchall()
                    if result:
                        print("---------------------------------------------------------")
                        for row in result:
                            print(row)
                        print("---------------------------------------------------------")
                    else:
                        print("---------------------------------------------------------")
                        print("Book not found or unavailable.")
                        print("---------------------------------------------------------")
                        
                elif sch == 4:
                    genretype = input('Enter the type of the genre ')
                    q = f"select * from books where status = 'N' and Genre = '{genretype}'"
                    cmd.execute(q)
                    result = cmd.fetchall()
                    if result:
                        print("---------------------------------------------------------")
                        for row in result:
                            print(row)
                        print("---------------------------------------------------------")
                    else:
                        print("---------------------------------------------------------")
                        print("Book not found or unavailable.")
                        print("---------------------------------------------------------")
                    
                

            elif ch == 4:  # Update Book Status
                ISBN = int(input("Enter ISBN of the book to update: "))
                q = "UPDATE books SET Status = 'Y' WHERE ISBN = %s"
                cmd.execute(q, (ISBN,))
                cnx.commit()
                print("---------------------------------------------------------")
                print("Book status updated!")
                print("---------------------------------------------------------")

            elif ch == 5:  # Delete Book
                ISBN = int(input("Enter ISBN of the book to delete: "))
                q = "DELETE FROM books WHERE ISBN = %s"
                cmd.execute(q, (ISBN,))
                cnx.commit()
                print("---------------------------------------------------------")
                print("Book deleted successfully!")
                print("---------------------------------------------------------")

            elif ch == 6:
                break

    elif c == 2:  # Borrower Management
        while True:
            print('\n1. Register Borrower')
            print('2. View Borrowers')
            print('3. Delete Borrower')
            print('4. Exit')
            ch = int(input('Enter choice: '))

            if ch == 1:  # Register Borrower
                BID = int(input('Enter Borrower ID: '))
                BName = input('Enter Name: ')
                BNo = input('Enter Contact Number: ')
               
                q = "INSERT INTO borrower (BID, BName, BNo) VALUES (%s, %s, %s)"
                cmd.execute(q, (BID, BName, BNo))
                cnx.commit()
                print("---------------------------------------------------------")
                print("Borrower registered successfully!")
                print("---------------------------------------------------------")

            elif ch == 2:  # View Borrowers
                cmd.execute("SELECT * FROM borrower")
                print("---------------------------------------------------------")
                for row in cmd.fetchall():
                    print(row)
                print("---------------------------------------------------------")

            elif ch == 3:  # Delete Borrower
                BID = int(input("Enter Borrower ID to delete: "))
                q = "DELETE FROM borrower WHERE BID = %s"
                cmd.execute(q, (BID,))
                cnx.commit()
                print("---------------------------------------------------------")
                print("Borrower deleted successfully!")
                print("---------------------------------------------------------")

            elif ch == 4:
                break

    elif c == 3:  # Issue Books
        BID = int(input('Enter Borrower ID: '))
        ISBN = int(input('Enter ISBN of book to issue: '))
        DueDate = datetime.today() + timedelta(days=14)

        # Check if book is available
        cmd.execute("SELECT Copies FROM books WHERE ISBN = %s AND Status = 'N'", (ISBN,))
        result = cmd.fetchone()

        if result and result[0] > 0:
            # Issue the book
            q = "INSERT INTO transacts (BID, ISBN, IssueDate, DueDate, Fine) VALUES (%s, %s, %s, %s, 0)"
            cmd.execute(q, (BID, ISBN, datetime.today().date(), DueDate.date()))
            cnx.commit()

            # Update book stock
            cmd.execute("UPDATE books SET Copies = Copies - 1 WHERE ISBN = %s", (ISBN,))
            cnx.commit()
            print("---------------------------------------------------------")
            print(f"Book issued successfully! Due Date: {DueDate.date()}")
            print("---------------------------------------------------------")

        else:
            print("Book not available.")

    elif c == 4:  # Return Books
        ISBN = int(input('Enter ISBN of book to return: '))
        BID = int(input('Enter Borrower ID: '))

        # Update Transactions table
        cmd.execute("UPDATE transacts SET ReturnDate = %s WHERE ISBN = %s AND BID = %s",
                    (datetime.today().date(), ISBN, BID))
        cnx.commit()

        # Update stock
        cmd.execute("UPDATE books SET Copies = Copies + 1 WHERE ISBN = %s", (ISBN,))
        cnx.commit()
        print("---------------------------------------------------------")
        print("Book returned successfully!")
        print("---------------------------------------------------------")

    elif c == 5:  # View Logs
        cmd.execute("SELECT * FROM transacts")
        print("---------------------------------------------------------")
        for row in cmd.fetchall():
            print(row)
        print("---------------------------------------------------------")

    elif c == 6:  # Exit
        break

cnx.close()
