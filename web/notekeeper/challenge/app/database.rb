require "sqlite3"

class Database

	def initialize
		@db = SQLite3::Database.new("./db/database.db")
		@db.execute("CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, username VARCHAR(50), password VARCHAR(50));")
		@db.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, title VARCHAR(50), note VARCHAR(50), date TEXT, user VARCHAR(50));")
	end

	def register(username, password)
		if username != "admin" && !checkSameUsername(username)
			@db.execute("INSERT INTO accounts (username, password) VALUES (?,?);", [username, password])
			return true
		else
			return false
		end
	end

	def login(username, password)
		if username != "admin"
			@db.execute("SELECT * FROM accounts WHERE username = ? AND password= ?;", [username, password]).each do | row |
				if row[1] == username && row[2] == password
					return true
				else
					return false
				end
			end
			return false
		else
			return false
		end
	end

	def checkSameUsername(username)
	  @db.execute("SELECT username FROM accounts WHERE username = ?", [username]).each do |row|
	    return true if row[0] == username
	  end
	  return false
	end

	def addNote(title, note, date, username)
		@db.execute("INSERT INTO notes (title, note, date, user) VALUES (?, ?, ?, ?);", [title, note, date, username])
		id = @db.last_insert_row_id
		return id
	end

	def removeNote(id, username)
		user = ""
		@db.execute("SELECT user FROM notes WHERE id = ?;", [id]).each do |row|
			if row[0] != "" || row[0] != Null
				user = row[0]
			else
				return false
			end
		end
		if user == username
	  		@db.execute("DELETE FROM notes WHERE id = ? AND user = ?;", [id, username])
	  		return true
	  	else
	  		return false
	  	end
	end

	def grabAllNotes(username)
		notes = @db.execute("SELECT * FROM notes WHERE user = ?;", [username])
		return notes
	end

end