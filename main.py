from tkinter import Tk
from views.login_view import LoginView
from controllers.auth_controller import AuthController

def main():
    root = Tk()
    auth_controller = AuthController()

    def handle_login(username, password):
        auth_controller.login(username, password)

    login_view = LoginView(root)  # Chỉ truyền root thôi

    root.mainloop()

if __name__ == "__main__":
    main()
