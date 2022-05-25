import mysql.connector
import datetime

all_users = []
count = 0
user_valid = 0
bool_exists = 0
fanid = ''
review_match_id = ''
username = ''
club = ''
club_secondary = ''
favourite_club = ''
player_input = ''
player_query = ''
stadium_input = ''
stadium_query = ''
position_input = ''
position_query = ''
nation_input = ''
nation_query = ''
player_id = ''
nation_check=''
nation_list = []
home_team = ''
away_team = ''
match_id = 0

print("Please enter one of these operations:")
print ("'u' to register a new user")
print("'r' to create a new review")
print("'q' to query")
invalue = input()
while invalue != 'u' and invalue != 'r' and invalue != 'q':
    print("Please enter one of these operations:")
    print ("'u' to register a new user",'\n', "'r' to create a new review,",'\n',"'q' to query")
    invalue = input()
def user_exists():
    global bool_exists
    global username
    global all_users
    bool_exists = 0
    for i in all_users:
        if username == i:
            bool_exists = 1
            
    if bool_exists == 1:
            print("This username is already in use. Please enter another.")
            username = input()

def username_validation():
    global user_valid
    for i in all_users:
        if fan_reviewing == i:
            user_valid = 1
    if user_valid == 0:
            print("Please enter a valid username")

def fav_team():
    global club 
    global favourite_club
    favourite_club = input()
    cursor.execute(f'SELECT id FROM clubs WHERE name = "{favourite_club}"')
    result = cursor.fetchall()
    for x in result:
           for y in x:
              club = y
              

def away():
    global club_secondary 
    global favourite_club
    favourite_club = input()
    cursor.execute(f'SELECT id FROM clubs WHERE name = "{favourite_club}"')
    result = cursor.fetchall()
    for x in result:
           for y in x:
              club_secondary = y
              
def find_player():
    global player_query
    global player_input
    player_input = input()
    cursor.execute(f'SELECT name FROM players WHERE name = "{player_input}"')
    result = cursor.fetchall()
    for x in result:
           for y in x:
              player_query = y

def find_stadium():
    global stadium_query
    global stadium_input
    stadium_input = input()
    cursor.execute(f'SELECT id FROM stadiums WHERE name = "{stadium_input}"')
    result = cursor.fetchall()
    for x in result:
           for y in x:
              stadium_query = y
def find_position():
    global position_query
    global position_input
    position_input = input()
    cursor.execute(f'SELECT name FROM players WHERE position = "{position_input}"')
    result = cursor.fetchall()
    for x in result:
           for y in x:
              position_query = y
              print(position_query)
def find_nation():
    global nation_query
    global nation_input
    global nation_check
    cursor.execute(f'SELECT id FROM players WHERE nationality = "{nation_input}"')
    result = cursor.fetchall()
    for x in result:
           for y in x:
              player_id = y
              cursor.execute(f'SELECT player FROM player_club_history WHERE player_id = "{player_id}"')
              res = cursor.fetchall()
              for i in res:
                  for j in i:
                      nation_check = j
                      nation_list.append(j) 
    for i in nation_list:
        print(i,': ')         
        cursor.execute(f'SELECT * FROM player_club_history WHERE player = "{i}"')
        r = cursor.fetchall()
        for x in r:
            if x[4]!='' and x[5]!='':
                print(x[3],',',x[4],',',x[5])
            if x[4] == '':
                print(x[3])
            if x[4] != '' and x[5] == '':
                print(x[3],',',x[4])    

                  
                      
try:
#establishing the connection
    conn = mysql.connector.connect(
    user='gemiey', password='12345Karim@', host='db4free.net', database='gemieydb'
    )
#Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    if invalue == 'u':
        print("Username:")
        username = input()

        cursor.execute('SELECT username FROM fans')
        result = cursor.fetchall()
        for x in result:
            for y in x:
                all_users.append(y)
        user_exists()
        while bool_exists == 1:
            user_exists()
        
        print("Enter your email:")
        email = input()
        print("Enter your age:")
        age = int(input())
        
        #age validation
        while age < 7:
            print("Please enter a valid age:")
            age=int(input())

        print("Enter your gender (Type in m or f):")
        gender = input()

        # gender validation
        while gender!='m' and gender!='f':
            print("Please enter a valid gender (Type in m or f):")
            gender = input()

        print("BIRTHDATE")
        print("Year")
        year = int(input())
        print("Month (pick from 1 to 12)")
        month = int(input())
        while month < 1 or month > 12:
            print("Month (pick from 1 to 12)")
            month = int(input())
        print("Day")
        day = int(input())

        cursor.execute('SELECT name FROM clubs')
        result = cursor.fetchall()
        for i in result:
            for j in i:
                print(j)
        print("Enter the name of your favorite club from the list above.")
        fav_team()               
        while club == '':
            print('Invalid club name. Enter again.')
            fav_team()
    
            
        print("You have successfully been registered")
        all_users.append(username)

        
        cursor.execute('SELECT * FROM fans')
        result = cursor.fetchall()
        query = 'INSERT INTO `fans` (id,email,username,age,gender,birth_date,favourite_club_id) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        val = (len(result)+5,email, username, age, gender,datetime.date(year,month,day),club)
        cursor.execute(query,val)
    
    if invalue == 'r':
            cursor.execute('SELECT username FROM fans')
            result = cursor.fetchall()
            for x in result:
                for y in x:
                    all_users.append(y)
        
            print("Enter your username:")
            while user_valid == 0:
                fan_reviewing = input()
                username_validation()
            print("Enter the home team of the match you wish to review:")
            fav_team()               
            while club == '':
                print('Invalid club name. Enter again.')
                fav_team()
            home_team = favourite_club    
            print("Enter the away team of the match you wish to review:")
            away()               
            while club_secondary == '':
                print('Invalid club name. Enter again.')
                away()
            away_team = favourite_club 
            if home_team == away_team:
                club_secondary=''
                while club_secondary == '':
                    print('You entered the same team twice. Reenter away team name.')
                    away()
            cursor.execute(f'SELECT id FROM matches WHERE home_team = "{home_team}" and away_team = "{away_team}"')
            result = cursor.fetchall()
            for x in result:
                for y in x:
                    match_id = y      
            print("Enter your match rating:")
            match_rating = int(input())
            print("Enter your match review:")
            match_review = input()
            # finding id of fan based on entered username, adding it as foreing key into reviews table
            cursor.execute('SELECT * FROM `fans`')
            result = cursor.fetchall()
            for x in result:
                print(x)
                print(fan_reviewing)
                if x[1] == fan_reviewing:
                    fanid = x[6] 
                    break
            cursor.execute('SELECT * FROM `reviews`')
            result = cursor.fetchall()
            query = 'INSERT INTO reviews (id,fan_id,match_id,rating,review) VALUES (%s, %s, %s, %s, %s)'
            val = (len(result)+1,fanid, match_id, match_rating, match_review)
            cursor.execute(query,val)
    if invalue == 'q':
        print("Choose a query to perform")
        print("'m' to view the information of a given club")
        print("'p' to view the information of a given player")
        print("'s' to identify the home team of a given stadium")
        print("'pos' to identify all players of a given position")
        print("'n' to identify all players of a given nationality")
        print("'v' to view reviews of a match")
        input_query = input()

        while input_query != 'm' and input_query!='p' and input_query!='s' and input_query!='pos' and input_query!='n'and input_query!='v':
            print("Invalid input. Choose a query to perform")
            print("'m' to view the information of a given club")
            print("'p' to view the information of a given player")
            print("'s' to identify the home team of a given stadium")
            print("'pos' to identify all players of a given position")
            print("'n' to identify all players of a given nationality")
            input_query = input()
        
        if input_query == 'm':
            cursor.execute('SELECT name FROM clubs')
            result = cursor.fetchall()
            for i in result:
                for j in i:
                    print(j)
            print("Enter the name of a club from the list above.")
            fav_team()               
            while club == '':
                print('Invalid club name. Enter again.')
                fav_team()
            cursor.execute(f'SELECT * FROM clubs WHERE name = "{favourite_club}"')
            result = cursor.fetchall()
            for x in result:
                for y in x:
                    if count == 1:
                        print("Name:")
                        print(y)
                    if count == 2:
                        print("Website:")
                        print(y) 
                    if count == 4:
                        print("Stadium:")
                        print(y)              
                    count +=1
            
        if input_query == 'p':
                print("Enter the first name and last name of a player.")
                find_player()               
                while player_query == '':
                    print('Invalid name. Enter again.')
                    find_player()
                cursor.execute(f'SELECT * FROM players WHERE name = "{player_query}"')
                result = cursor.fetchall()
                for x in result:
                    for y in x:
                        if count == 1:
                            print("Name:")
                            print(y)
                        if count == 2:
                            print("Height:")
                            print(y,'cm')
                        if count == 3:
                            print("Weight:")
                            print(y, 'kg')
                        if count == 4:
                            print("Position:")
                            print(y)
                        if count == 5:
                            print("Birthdate:") 
                            print(y)
                        if count == 6:
                            print("Nationality:")
                            print(y)
                        if count == 8:
                            print("Club:")
                            print(y)                       
                        count +=1    
        if input_query == 's':
                print("Enter the name of a stadium.")
                find_stadium()               
                while stadium_query == '':
                    print('Invalid name. Enter again.')
                    find_stadium()
                cursor.execute(f'SELECT name FROM clubs WHERE home_stadium_id = "{stadium_query}"')
                result = cursor.fetchall()
                for x in result:
                    for y in x:
                        print(y)
        if input_query=='pos':
                print("Enter a position (goalkeeper, defender, midfielder or forward).")
                find_position()               
                while position_query == '':
                    print('Invalid position. Enter again.')
                    find_position()
        
        if input_query=='n':
                print("Enter a country (ex: Germany, England, etc).")
                nation_input = input()
                find_nation()               
                while nation_check == '':
                    print('Invalid nationality. Enter again.')
                    nation_input = input()
                    find_nation()
        if input_query == 'v':
            print("Enter the home team of the match:")
            fav_team()               
            while club == '':
                print('Invalid club name. Enter again.')
                fav_team()
            home_team = favourite_club    
            print("Enter the away team of the match:")
            away()               
            while club_secondary == '':
                print('Invalid club name. Enter again.')
                away()
            away_team = favourite_club 
            cursor.execute(f'SELECT id FROM matches WHERE home_team = "{home_team}" and away_team = "{away_team}"')
            result = cursor.fetchall()
            for x in result:
                for y in x:
                    review_match_id = y
            if (review_match_id != ''):                
                cursor.execute(f'SELECT fan_id FROM reviews WHERE match_id = "{review_match_id}"')
                result = cursor.fetchall()
                for x in result:
                    for y in x:
                        z = y
                cursor.execute(f'SELECT username FROM fans WHERE id = "{z}"')
                result = cursor.fetchall()
                for x in result:
                    for y in x:
                        user = y
                cursor.execute(f'SELECT review, rating FROM reviews WHERE match_id = "{review_match_id}"')
                result = cursor.fetchall()
                print('Review by',user)
                for x in result:
                    for y in x:
                        print(y)
            else:
                print('There are no reviews for this match')

                          
                                
                                  
    #cursor.execute('SELECT * FROM reviews')

    # result = cursor.fetchall()
    # for x in result:
    #     print(x)
    
    conn.commit()

except Exception as e:
    print(e)

