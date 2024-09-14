require "cuba"
require "cuba/safe"
require "cuba/render"
require "./database"
require "open3"
require "rack/session"

Cuba.use Rack::Session::Cookie, :key => 'session', :secret => 'a!g<aH5GsN:+pv"-.fcx<;/1BCLT4lixxk]q/xB(_4pn]Ya_?JT#,_=}n|wf{`23'
Cuba.plugin Cuba::Safe
Cuba.plugin Cuba::Render
db = Database.new()
report_path = File.expand_path(".") + "/reports/"

def add_line_breaks(string)
  words = string.split
  result = ""
  words.each_slice(3) do |slice|
    result += slice.join(" ") + "<br/>"
  end
  result.chomp("<br/>")
end

def h(text)
  Rack::Utils.escape_html(text)
end

Cuba.define do

  on get do
    on "login" do
      begin
        session[:user] = nil
        res.write partial("login", error: "")
      rescue 
        res.status = 500
        res.headers["Content-Type"] = "text/html"
        res.write partial("500")
      end
    end

    on "register" do
      begin
        res.write partial("register", error: "")
      rescue
        res.status = 500
        res.headers["Content-Type"] = "text/html"
        res.write partial("500")
      end
    end

    on "flag" do
      begin
        if session[:user] == "admin"
          if req.ip == "127.0.0.1"
            stdout, status = Open3.capture2("/flag")
            res.write stdout
          else
            res.status = 403
            res.headers["Content-Type"] = "text/html"
            res.write partial("403")
          end
        else
            res.status = 403
            res.headers["Content-Type"] = "text/html"
            res.write partial("403")
        end        
      rescue
        res.status = 500
        res.headers["Content-Type"] = "text/html"
        res.write partial("500")
      end
    end

    on "admin" do
      begin
        if session[:user] == nil
          res.status = 403
          res.headers["Content-Type"] = "text/html"
          res.write partial("403")
        else
          if req.ip == "127.0.0.1"
            files = Dir.each_child(report_path)
            res.write partial("admin", error: "", user: session[:user], files: files, content: "")
          else
            res.status = 403
            res.headers["Content-Type"] = "text/html"
            res.write partial("403")
          end
        end
      rescue 
        res.status = 500
        res.headers["Content-Type"] = "text/html"
        res.write partial("500")
      end
    end

    on "report" do
      begin
        if session[:user] == nil
          res.redirect "/login"
        else
          res.write partial("report", user: session[:user], error: "", success: "")
        end
      rescue
        res.status = 500
        res.headers["Content-Type"] = "text/html"
        res.write partial("500")
      end
    end

    on root do
      begin
        if session[:user] == nil
          res.redirect "/login"
        else
          notes = db.grabAllNotes(session[:user])
          res.write partial("index", user: session[:user], notes: notes, error: "")
        end
      rescue
        res.status = 500
        res.headers["Content-Type"] = "text/html"
        res.write partial("500")
      end
    end
  end

  on post do 
    begin
      on "login" do 
        on param("username"), param("password") do |username, password|
          check = db.login(username, password)
          if check
            session[:user] = username
            res.redirect "/"
          else
            res.write partial("login", error: "Wrong credentials!")
          end
        end

        on true do
          res.write partial("login", error: "You need to provide a username and a password!")
        end      
    rescue
        res.status = 500
        res.headers["Content-Type"] = "text/html"
        res.write partial("500")
    end
  end

    on "register" do
      begin
        on param("username"), param("password"), param("confirmPassword") do |username, password, confirmPassword|
          if password == confirmPassword
            check = db.register(username, password)
            if check
              res.redirect "login"
            else
              res.write partial("register", error: "You can't register as admin or the username is already in use!")
            end
          else
            res.write partial("register", error: "Password is not the same!")
          end
        end
        on true do
          res.write partial("register", error: "You need to provide everything!")
        end        
      rescue
        res.status = 500
        res.headers["Content-Type"] = "text/html"
        res.write partial("500")
      end
    end

    on "report" do
      begin
        if session[:user] == nil
          res.redirect "/login" 
        else
          on param("title"), param("report") do |title, report|
            t = Time.new
            time = t.strftime("%k:%M:%S")    
            date = t.strftime("%d-%m-%Y") 
            fulldate = time + "_" + date

            file = File.new(report_path + "report_" + fulldate + ".txt", "w")
            File.open(file, "w") do |report_file|
              report_file.puts("Title:")
              report_file.puts(title)
              report_file.puts("<br/>")
              report_file.puts("Report:")
              report_file.puts(report)
              report_file.puts("<br/>")
              report_file.puts("User:")
              report_file.puts(session[:user])
            end
            res.write partial("report", user: session[:user], error: "", success: "Your report has been successfully sent!")
          end
          on param("title") do 
            res.write partial("report", user: session[:user], error: "Both fields are required!", success: "")
          end
          on param("report") do
            res.write partial("report", user: session[:user], error: "Both fields are required!", success: "")
          end
          res.write partial("report", user: session[:user], error: "You can't send an empty report!", success: "")   
        end    
      rescue
        res.status = 500
        res.headers["Content-Type"] = "text/html"
        res.write partial("500")
      end
    end

    on "download" do
      begin
        if session[:user] == nil
            res.status = 403
            res.headers["Content-Type"] = "text/html"
            res.write partial("403")
        else
          if req.ip == "127.0.0.1"
            on param("filename") do |filename|
              file = File.join(report_path, filename)
              if File.exist?(file)
                content = File.open(file).read()
                files = Dir.each_child(report_path)
                res.write partial("admin", error: "File doesn't exist!", user: session[:user], files: files, content: content)
              else
                files = Dir.each_child(report_path)
                res.write partial("admin", error: "File doesn't exist!", user: session[:user], files: files, content: "")
              end
            end
          else
            res.status = 403
            res.headers["Content-Type"] = "text/html"
            res.write partial("403")
          end
        end         
      rescue
        res.status = 500
        res.headers["Content-Type"] = "text/html"
        res.write partial("500")
      end
    end

    on root do
      begin
        if session == nil
          res.redirect "/login"
        else
          on param("title"), param("note") do |title, note|
            t = Time.new
            time = t.strftime("%k:%M:%S")    
            date = t.strftime("%d/%m/%Y") 
            fulldate = time + " " + date
            note = add_line_breaks(note)
            db.addNote(title, note, fulldate, session[:user])
            notes = db.grabAllNotes(session[:user])
            res.write partial("index", user: session[:user], notes: notes, error: "")
          end
          on param("title") do 
            notes = db.grabAllNotes(session[:user])
            res.write partial("index", user: session[:user], notes: notes, error: "Both fields are required!")
          end
          on param("note") do
            notes = db.grabAllNotes(session[:user])
            res.write partial("index", user: session[:user], notes: notes, error: "Both fields are required!")
          end
          notes = db.grabAllNotes(session[:user])
          res.write partial("index", user: session[:user], notes: notes, error: "Both fields are required!")        
        end
      rescue
        res.status = 500
        res.headers["Content-Type"] = "text/html"
        res.write partial("500")
      end
    end

    on "removeNote" do
      begin
        if session[:user] == nil
          res.redirect "/login"
        else
          on param("id") do |id|
            check = db.removeNote(id, session[:user])
            if check
              res.redirect "/"
            else
              res.status = 403
              res.headers["Content-Type"] = "text/html"
              res.write partial("403")
            end   
          end
        end     
      rescue
        res.status = 500
        res.headers["Content-Type"] = "text/html"
        res.write partial("500")
      end
    end

  end

end