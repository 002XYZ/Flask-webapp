from website import create_app
# import website.create_app as create_app
app=create_app()

if __name__ == '__main__':  # This line makes sure that only when this file is run, without
                            # this, even when main.py is imported, server will run
    app.run(debug=True)     # debug=True means whenever we change the code, it's going to 
                            # automatically rerun the web server