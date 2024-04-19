import sqlite3
import os
import datetime
import turtle

conn = sqlite3.connect('workouts.db')
conn = sqlite3.connect('goals.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS prs (
             id INTEGER PRIMARY KEY,
             type TEXT,
             exercise TEXT NOT NULL,
             weight REAL,
             reps INTEGER,
             distance REAL,
             time REAL,
             date TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS goals (
             id INTEGER PRIMARY KEY,
             type TEXT,
             exercise TEXT NOT NULL,
             weight REAL,
             reps INTEGER,
             distance REAL,
             time REAL,
             date TEXT)''')

def addPR():
  while True:
    type = input("\n - Enter exercise type (Weight, Running): ")
    if type != "Weight" and type != "Running":
      print("Please choose one.")
    else:
      break
  exercise = input("\n - Enter exercise name: ")
  if type.lower() == "weight":
    weight = float(input("\n - Enter weight (lbs): "))
    reps = int(input("\n - Enter reps: "))
    date = enterDate()  # Input date
    c.execute('''INSERT INTO prs (type, exercise, weight, reps, date)
     VALUES (?, ?, ?, ?, ?)''', (type, exercise, weight, reps, date))
  elif type.lower() == "running":
    distance = int(input("\n - Enter distance (miles): "))
    time = float(input("\n - Enter time (minutes): "))
    date = enterDate()  # Input date
    c.execute('''INSERT INTO prs (type, exercise, distance, time, date)
     VALUES (?, ?, ?, ?, ?)''', (type, exercise, distance, time, date))
    print()
  conn.commit()
  print("PR added successfully.")

def exercisePR(exercise=None):
  if exercise:
    c.execute('''SELECT * FROM prs WHERE exercise = ?''', (exercise,))
  else:
    c.execute('''SELECT * FROM prs''')
  prs = c.fetchall()
  if not prs:
    print("\n\tNo workouts found.\n")
  else:
    print()
    for pr in prs:
      if pr[1].lower() == "weight":
        print(f"\tWorkout #{pr[0]} (WEIGHT, {pr[7]}): {pr[2]}, Weight: {pr[3]} Lbs, Reps: {pr[4]}")
      if pr[1].lower() == "running":
        print(f"\tWorkout #{pr[0]} (RUNNING, {pr[7]}): {pr[2]}, Distance: {pr[5]} miles, Time: {pr[6]} minutes")
    print()

def distinctExercises():
  c.execute('''SELECT DISTINCT exercise FROM prs''')
  exercises = c.fetchall()
  print("\n\tAvailable exercises:")
  for exercise in exercises:
     print(f"\n\t\t - {exercise[0]}\n")
  exercise = input("Enter exercise name: ")
  exercisePR(exercise)

def removeWorkout():
  exercisePR()
  workoutID = int(input("Enter the ID of the workout to remove: "))
  c.execute('''DELETE FROM prs WHERE id = ?''', (workoutID,))
  conn.commit()
  print("Workout removed successfully.")

def graphThings():
  while True:
    c.execute('''SELECT DISTINCT exercise FROM prs''')
    exercises = c.fetchall()
    print("Available exercises:")
    for exercise in exercises:
      print(exercise[0])
    choice = str(input("Please select an exercise: "))
    temp = False
    for exercise in exercises:
      if choice == exercise[0]:
        temp = True
        break
    if temp is True:
      break
    else:
      print("Error")
  c.execute('''SELECT DISTINCT type FROM prs WHERE exercise = ?''', (choice,))
  test = c.fetchall()
  if len(test) != 1:
    while True:
      type = input("\n - Enter the exercise type you'd like to graph. (Weight, Running): ")
      if type != "Weight" and type != "Running":
        print("Please choose one.")
      else:
        break
  else:
    type = test[0][0]
  c.execute('''SELECT exercise,type FROM prs WHERE exercise = ? AND type = ?''', (choice,type))
  test = c.fetchall()
  print("Which statistic would you like to graph?")
  if type.lower() == "weight":
    c.execute('''SELECT exercise,weight,reps,date FROM prs WHERE exercise = ? ORDER BY date''', (choice,))
    test = c.fetchall()
    while True:
      print("Choose one to graph: 1. Weight 2. Reps")
      choice = input()
      if choice in ["1","2"]:
        break
      print("Invalid choice")
  elif type.lower() == "running":
    c.execute('''SELECT exercise,distance,time,date FROM prs WHERE exercise = ? ORDER BY date''',(choice,))
    test = c.fetchall()
    while True:
      print("Choose one to graph: 1. Distance 2. Time")
      choice = input()
      if choice in ["1","2"]:
        break
      print("Invalid choice")
  choice = int(choice)
  thingstograph = []
  for i in test:
    thingstograph.append(i[choice])
  screen = turtle.Screen()
  screen.setup(450,350)
  turtle.clearscreen()
  turtle.home()
  turtle.up()
  turtle.left(180)
  turtle.forward(turtle.window_width()/2)
  turtle.left(90)
  turtle.forward(turtle.window_height()/2)
  date1 = datetime.datetime.strptime(test[len(test)-1][3], "%Y-%m-%d").date()
  date2 = datetime.datetime.strptime(test[0][3], "%Y-%m-%d").date()
  multiply = 450 / ((date1-date2).total_seconds()//86400)
  multiply2 = 300 / (max(thingstograph)-min(thingstograph))
  subtract = min(thingstograph)
  turtle.goto(turtle.window_width()/-2,(test[0][choice]-subtract) * multiply2 - 150)
  turtle.down()
  for i in test:
    date1 = datetime.datetime.strptime(i[3], "%Y-%m-%d").date()
    turtle.goto((((date1 - date2).total_seconds()//86400)) * multiply - 225, (i[choice] - subtract) * multiply2 - 150)

def clearData():
  choice = int(input("\n\tWhich database would you like to remove? (1 - workouts.db, 2 - goals.db): "))
  if choice == 1:
    confirm = input("\n\tAre you sure?: ")
    if confirm.lower() == 'y':
      os.remove('workouts.db')
      print("\n\tRemoving database...")
      exit()
    else:
      exit()
  if choice == 2:
    confirm = input("\n\tAre you sure?: ")
    if confirm.lower() == 'y':
      os.remove('goals.db')
      print("\n\tRemoving database...")
      exit()
    else:
      exit()

def enterDate():
  while True:
    tempdate = input("\n - Enter date (YYYY-MM-DD): ")
    try:
      datetime.datetime.strptime(tempdate, "%Y-%m-%d").date()
    except ValueError:
      print("That isn't a valid date...")
    else:
      break
  return tempdate

def setGoals():
  type = input("\n - Goal Type (Weight, Running): ")
  exercise = input("\n - Enter Exercise: ")
  if type.lower() == 'weight':
    weight = int(input("\n - Enter Weight: "))
    reps = int(input("\n - Enter Reps: "))
    c.execute('''INSERT INTO goals (type, exercise, weight, reps)
     VALUES (?, ?, ?, ?)''', (type, exercise, weight, reps))
  elif type.lower() == 'running':
    distance = int(input("\n - Enter distance (miles): "))
    time = float(input("\n - Enter time (minutes): "))
    c.execute('''INSERT INTO goals (type, exercise, distance, time)
     VALUES (?, ?, ?, ?)''', (type, exercise, distance, time))
  else:
    print("Please select a type of goal.")
  conn.commit()
  print("Goal added successfully.")

def distinctGoals():
  c.execute('''SELECT DISTINCT exercise FROM goals''')
  goals = c.fetchall()
  print("Available goals:")
  for goal in goals:
     print(goal[0])

def start():
  print("Gym Stat Tracker: \n\n\t1. Track new workout \n\t2. View all workouts \n\t3. View workouts by exercise \n\t4. Set a goal for next week \n\t5. View next week's goals \n\t6. Remove a workout \n\t7. Graph statistics \n\t8. Reset database \n\t9. Exit")
  while True:
    choice = input("\nEnter your choice: ")
    if int(choice) in [1,2,3,4,5,6,7,8,9]:
      type = int(choice) - 1
      return type
    else:
      print("Please select an option.")

def mainMenu(choice):
  list = [addPR, exercisePR, distinctExercises, setGoals, distinctGoals, removeWorkout, graphThings, clearData]
  if choice <= 7:
    list[choice]()
  elif choice == 8:
    print("Exiting...")
    exit()
  else:
    print("whar?")

while True:
  type = start()
  mainMenu(type)

conn.close()