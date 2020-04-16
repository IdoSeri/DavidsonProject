import sqlite3
import itertools

# conn = sqlite3.connect('equip_list.db')

# c = conn.cursor()

# c.execute("""
#     CREATE TABLE equipment(
#         name        TEXT        NOT NULL,
#         item        TEXT        NOT NULL,
#         count       INT         NOT NULL
#     )
# """)

# c.close()


def insert(name, item): #adds a new item
    conn = sqlite3.connect('equip_list.db')
    c = conn.cursor()
    
    count = c.execute("""SELECT COUNT(*) FROM equipment WHERE name = ? AND item = ?""", (name, item)).fetchone()[0] #the amount of an item
    if count == 0:
        c.execute("INSERT INTO equipment VALUES (?, ?, ?)", (name, item, count)) #creates new row for the new item
        conn.commit()
    else:
        c.execute("""UPDATE equipment SET count = count + 1 WHERE name = ? AND item = ?""", (name, item)) #increases the amount of an existing item by 1
        conn.commit()
    
    c.close()


def delete(name, item): #delets an item 
    conn = sqlite3.connect('equip_list.db')
    c = conn.cursor()
    
    table_exsist = c.execute("""SELECT COUNT(*) FROM equipment""").fetchone()[0]
    
    if table_exsist:
        row_exsist = c.execute("""SELECT COUNT(*) FROM equipment WHERE name = ? AND item = ?""", (name, item)).fetchone()[0]
        
        if row_exsist:
            item_amount = c.execute("""SELECT count FROM equipment WHERE name = ? AND item = ?""", (name, item)).fetchone()[0]
            if item_amount == 0:
                c.execute("""DELETE FROM equipment WHERE name = ? AND item = ?""", (name, item))#delete the row
                conn.commit()
            else:
                c.execute("""UPDATE equipment SET count = count - 1 WHERE name = ? AND item = ?""", (name, item)) #reduce by 1 the amount
                conn.commit() 
    else:
        pass
    
    c.close()
   

def check(name): #checks if the person retured all of his items
    conn = sqlite3.connect('equip_list.db')
    c = conn.cursor()
    row_exsist_name = c.execute("""SELECT COUNT(*) FROM equipment WHERE name = ?""", (name,)).fetchone()[0]
    if row_exsist_name: #search for a row with the given name - if exsists means that not all of the items were returned
        return False #not all of the items were returned
    return True #all items were returned
    c.close()


def items_left(name): #prints the person's items
    conn = sqlite3.connect('equip_list.db')
    c = conn.cursor()
    
    items = c.execute("""SELECT item FROM equipment WHERE name = ?""", (name,)).fetchall()
    items_list = list(itertools.chain(*items))
    if items_list:
        for item in items_list:
            item_amount = c.execute("""SELECT count FROM equipment WHERE name = ? AND item = ?""", (name, item)).fetchone()[0]
            print("   Item: " + item + " | Amount: " +  str(item_amount+1))
    else:
        print(name + ", you do not have any items")
    c.close()


def print_table():
    conn = sqlite3.connect('equip_list.db')
    c = conn.cursor()
    table_exsist = c.execute("""SELECT COUNT(*) FROM equipment""").fetchone()[0]
    if not table_exsist:
        print("Table is empty")
    else:

        names = c.execute("""SELECT DISTINCT name FROM equipment""").fetchall()
        names_list = list(itertools.chain(*names))
        print("-------------------------------------")
        for name in names_list:
            print("     The items of " + name + ":")
            
            items = c.execute("""SELECT item FROM equipment WHERE name = ?""", (name,)).fetchall()
            items_list = list(itertools.chain(*items))
            for item in items_list:
                item_amount = c.execute("""SELECT count FROM equipment WHERE name = ? AND item = ?""", (name, item)).fetchone()[0]
                print("     Item: " + item + "  Amount: " +  str(item_amount+1))
            
            print("-------------------------------------")
        
    c.close()


def delete_all():
    conn = sqlite3.connect('equip_list.db')
    c = conn.cursor()
    c.execute("""DELETE FROM equipment""")
    conn.commit()
    c.close()