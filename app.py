# Import flask and flask session to save session data from users and to develop logic in python.
from flask import Flask, redirect,render_template, request, session, flash, jsonify, make_response, url_for
from flask_session import Session

# Make a flask session with the file.
app = Flask(__name__)

# Configure a session to save user data and update it.
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Code for the homepage of the website, called when the user first enters the website
@app.route('/', methods = ["GET","POST"])
def home():
  # If the user is entering the page, render the template for index.html, the homepage
    if request.method == "GET":
        return render_template('index.html')
    else:
      # When clicking the play on the homepage, save a bunch of session data for default game play
        # Get the users device width and height
        session['device_width'] = int(request.form.get("deviceWidth"))
        session['device_height'] = round(int(request.form.get("deviceHeight")) * 0.95)
        # Calculate the minimum number of rows and columns to fully cover the screen
        session['MinCellRows'] = round(session['device_height'] / 30)
        session['MinCellColumns'] = round(session['device_width'] / 30)
        # Set the default rows and columns value to be the minimum needed
        session['rows'] = session['MinCellRows']
        session['columns'] = session['MinCellColumns']
        # The timing between generations is defaulted to 300ms (0.3 seconds)
        session['timing'] = 300
        # Generate an array representation of the grid of squaree. They all start as false since
        # at the start every cell is dead.
        session['board'] = [[False for _ in range(session['columns'])] for _ in range(session['rows'])]
        # Reset the statistics of the cells, none are alive at the start, none are dead, and we are on the 0th generation (setup stage)
        session['alive'] = 0
        session['dead'] = 0
        session['generation'] = 0
        # The recent grid that the user has had (updated in the previous function) is None since the user is just starting off
        session['recent_grid'] = None
        # Set the basic behaviors, the minimum cells for survival is 2
        session['MinCells'] = 2
        # Maximum cells before dead is 3.
        session['MaxCells'] = 3
        # Cells needed for reproduction is 3.
        session['CellsRepop'] = 3
        # Redirect the user to the gameplay screen (game.html)
        return redirect("/game")

# The route that is called when the Restore Defaults button is clicked
# POST method since we are only updating session data.
@app.route('/RestoreDefaults', methods = ["POST"])
def RestoreDefaults():
        # Reset the rows and columns to their minumum values
        session['rows'] = session['MinCellRows']
        session['columns'] = session['MinCellColumns']
        # Reset the timing to the standard 300ms.
        session['timing'] = 300
        # Reset the board to have all cells be dead.
        session['board'] = [[False for _ in range(session['columns'])] for _ in range(session['rows'])]
        # Reset the cell statistics to make everything 0
        session['alive'] = 0
        session['dead'] = 0
        session['generation'] = 0
        # Remove any recent grids that existed
        session['recent_grid'] = None
        # Reset cell behaviors to be 2-3 adjacent for survival and 3 adjacent for repopulation
        session['MinCells'] = 2
        session['MaxCells'] = 3
        session['CellsRepop'] = 3
        # Return a 204 status code to inform that AJAX fetch call that there is no data being sent.
        return make_response('', 204)

# The route for when the user enters the rules page (called from the home page "rules & about" button)
@app.route("/rules")
def rules():
   # When they enter the page using the GET method, render the template that has already been made.
   return render_template("rules.html")

# The route for when the user enters the common patterns page (called from homepage Common Patterns button)
@app.route("/commonpatterns")
def commonpatterns():
   return render_template("commonpatterns.html")

# The route for when the user enteres the game page
# Called from Play button on home page, and back to game button in settings page.
@app.route('/game')
def game():
    # To prevent old data from interfering with the grid, whenever the user enters the game page
    # From any route, reset statistics and board data.
    # Set all cells to be dead
    session['board'] = [[False for _ in range(session['columns'])] for _ in range(session['rows'])]
    # Make recent grid be none
    session['recent_grid'] = None
    # Reset statistics on cell growth
    session['dead'] = 0
    session['alive'] = 0
    session['generation'] = 0
    # Render the template and send rows data, columns data, and timing data.
    return render_template('game.html', rows = session["rows"], columns = session["columns"], timing = int(session['timing']))

# The route for when the user enters the settings page, via the settings icon in the top right of the screen
@app.route('/settings', methods = ["GET", "POST"])
def settings():
    # For when the user enters the page, render the template.
    if request.method == "GET":
      # Render the settings template with data for rows, columns, timing, minimum cells, maximum cells, and the amount needed for repopulation
      # Send timing data /1000.0 to ensure that the value is in seconds, not in milliseconds
        return render_template('setting.html', rows = session['rows'], columns = session['columns'], timing = session['timing'] / 1000.0, MinCells = session['MinCells'], MaxCells = session['MaxCells'], CellsRepop = session['CellsRepop'])
    # If the user is pressing the save button to update their settings
    else:
        # Get all of the fields in settings
        rows = request.form.get("rows")
        columns = request.form.get("columns")
        timing = request.form.get("timing")
        mincells = request.form.get("MinCells")
        maxcells = request.form.get("MaxCells")
        cellsrepop = request.form.get("CellsRepop")
        # Make sure that rows and columns are valid integers, if not flash an erorr for the user tosee
        try:
            rows = int(rows)
            columns = int(columns)
        except ValueError:
            flash("Column or row values are not integers.")
            # Go back to the settings page with a "GET" method and display the error for the user
            return redirect(url_for("settings"))
        # Make sure the timing value is a float
        try:
            timing = float(timing)
        except ValueError:
            # If it isnt, go back to the settings page with "GET" method and display error
            flash("Timing is not a valid decimal or integer")
            return redirect(url_for("settings"))
        # Make sure that mincells, maxcells, and cellsrepop are all integers
        try:
           mincells = int(mincells)
           maxcells = int(maxcells)
           cellsrepop = int(cellsrepop)
        except ValueError:
          # If they aren't, go back to the settings page with "GET" method and display error
           flash("Non-Integer input for minimum, maximum, or repopulation settings")
        # Check if the inputs for rows or columns is less then the minimum needed to cover the screen
        if rows < session['MinCellRows'] or columns < session['MinCellColumns']:
            # If the vales are less, go back to settings page with "GET" and tell users the minimum columns and rows.
            flash(f"Please input at least {session['MinCellRows']} rows and {session["MinCellColumns"]} columns")
            return redirect(url_for("settings"))
        # Check if the timing is less than 100ms
        elif timing < 0.1:
            # If it is, go back to settings page with "GET" method and inform user that the time must be more than 0.1 seconds
            flash("Please ensure that the time between generation is greater than or 0.1 seconds.")
            return redirect(url_for("settings"))
        # Check if mincells is more then max cells, or if they are values other then numbers 1-8
        elif mincells < 1 or mincells > maxcells or maxcells > 8 or cellsrepop < 1 or cellsrepop > 8:
            # If so, go back to settings page with "GET" method and inform user of their invalid input
            flash("Invalid input for rules settings. Please ensure all values are integers between 1 and 8, and the minimum is less than or equal to the maximum")
            return redirect(url_for("settings"))
        # If all the inputs are valid
        else:
            # Update all session data that is configurable to match the user's inputs.
            session['rows'] = rows
            session['columns'] = columns
            # Timing is multiplied by 1000 to ensure value is in ms, not in seconds
            session['timing'] = timing * 1000
            session['MinCells'] = mincells
            session['MaxCells'] = maxcells
            session['CellsRepop'] = cellsrepop
            # Go back to settings page and update values.
            return redirect(url_for("settings"))

# A function called by the Javascript update function in order to make sure that cells
# Turned on via the user's click are updated inside of the array
# POST method only since we are only updating data.
@app.route("/update", methods = ["POST"])
def update():
    if request.method == "POST":
      # Get the button_id sent by the Javascript function
        data = request.get_json()
        button_id = data['button_id']
        # Split the button_id by the comma and assign the left half to be the row value and the right to be the column
        # This is possible because the button id's are formatted in the same way.
        row,column = map(int,button_id.split(','))
        # Update the board to be the opposite of what it was. If the cell was alive, make it dead, if it was dead, make it alive
        session['board'][row][column] = not session['board'][row][column]
        # If the color was originally white, the click will make the cell dead and remove one from alive counter
        if data['color'] == 'white':
           session['alive'] -= 1
        # If the color was originally black, the click will make it alive, and add one to alive counter
        else:
           session['alive'] += 1
        # Return the alive data to update the statistics on the bottom of the screen
        return jsonify(alive = session['alive'])

# The main function that applies the rules of Conway's Game of Life.
# This function takes the current grid, and moves on to the next generation.
# The rules of how cells repopulate and die can all be configured by the user.
@app.route("/step", methods = ["GET", "POST"])
def step():
    # Get the current board and increment generation by 1.
    grid = session['board']
    session['generation'] += 1
    # Create a new grid to fill with updated values for the new generation
    new_grid = [[False for _ in range(0,session['columns'])] for _ in range(0,session['rows'])]
    # Go through every cell in the 2 dimensional grid
    for row in range(0,len(grid)):
      for column in range(0,len(grid[0])):
        # Initalize the number of adjacent alive cells to be 0.
        adjacency = 0
        # Go through all of the cells surrounding the current selected cell.
        for i in range(row-1, row + 2):
          for j in range(column - 1, column + 2):
            # If the surrounding cells do not exist, or the surrounding cell found is
            # the current cell focused on, skip to the next adjacent cell.
            if i < 0 or i > len(grid) - 1 or j < 0 or j > len(grid[0]) - 1 or (i == row and j == column):
              continue
            # If it isnt the current cell and it exists
            else:
              # If the adjacent cell is alive, increment adjaceny, if not, move on to the next adjacent cell
              if grid[i][j] == True:
                adjacency+=1
              else:
                continue
        # After analyzing adjacent cells
        # If the current cell is alive, and the adjacent cells falls between the Min and Max Cell values,
        # That cell is alive for the next generation
        if (adjacency >= session['MinCells'] and adjacency <= session['MaxCells']) and grid[row][column] == True:
          new_grid[row][column] = True
        # If the current cell is dead, but the amount of live cells around it matches the repopulation value,
        # That cell becomes alive in the next generation
        elif adjacency == session['CellsRepop'] and grid[row][column] == False:
          new_grid[row][column] = True
          # Increment alive by 1 because repopulation has occured.
          session['alive'] += 1
        else:
          # If the cell does not fall into any of the rules, it is dead in then next generation
          new_grid[row][column] = False
          # If the cell was originally alive, decrement alive and increase dead since a once alive cell died.
          if grid[row][column] == True:
            session['alive'] -= 1
            session['dead'] += 1
    # Update the session board to be the new board created after going through all cells
    session['board'] = new_grid
    # Return the current board, along with alive, dead, and generation values to update statistics.
    return jsonify(board = new_grid, alive = session['alive'], generation = session['generation'], dead = session['dead'])

# A method called by the reset button, clears the grid and resets statistics
# Designed as "GET" method because it allows we recieve a boolean in return.
@app.route("/clear", methods = ["GET"])
def clear():
   # Reset board to have all cells be dead
   session['board'] = [[False for _ in range(0,session['columns'])] for _ in range(0,session['rows'])]
   # Reset alive and dead statistics
   session['alive'] = 0
   session['dead'] = 0
   # Set generation value to be -1, since after the clear function is clear, step is called right after
   # Since step with a dead grid will return a dead grid and it increments the generation, starting generation at -1
   # Allows the generation counter in the actual webpage to reset to 0.
   session['generation'] = -1
   # Return a boolean that we should call the step function and nothing has gone wrong.
   return jsonify(call_function = True)

# A method called when the run function is ran to save the grid before the function is ran.
# A "POST" method because we are only updating data
@app.route("/recent_grid", methods = ["POST"])
def recent_grid():
   # Update the session_recent grid to be the current board
   session['recent_grid'] = session['board']
   # Return 204 status code to tell AJAX that no content is being sent back.
   return make_response('', 204)

# A method called by the previous button that returns the recent grid and resets statistics.
# "GET" method because we are getting the recent grid.
@app.route("/load_recent_grid", methods = ["GET"])
def load_recent_grid():
   # Make the current board the recent_grid value that is called when the function is first ran.
   session['board'] = session['recent_grid']
   # Reset all statistics to be 0
   session['generation'] = 0
   session['alive'] = 0
   session['dead'] = 0
   # Return the recent grid value that is in session.
   return jsonify(board = session['recent_grid'])
