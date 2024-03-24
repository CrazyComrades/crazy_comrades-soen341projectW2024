from website import create_app
from datetime import datetime
app = create_app()


if __name__ == '__main__':
    app.run(debug=True)