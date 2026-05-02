import socket
import threading
import time


ip_server = "127.0.0.1"
port_server = 8888

# COLORS = [
#     "\033[92m",  # سبز
# ]
# RESET = "\033[92m"  # ریست کردن رنگ


def clear_screen():
    """پاک کردن صفحه ترمینال"""
    print("\033[2J\033[H", end="")


print("\n" + "=" * 50)
print("if you want to leave the chat write [close]")
print("=" * 50)


def receive_messages(client_socket):
    """دریافت و نمایش پیام‌ها از سرور"""
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                break
            # پیام از قبل شامل کدهای رنگی است
            print(f"\r{message}")
            print(f"[You] Enter Message: ", end="", flush=True)
        except:
            break


def start_client():

    clear_screen()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip_server, port_server))

    try:
        username = input("Enter your name: ")
        client.sendall(username.encode("utf-8"))
        # اسم رو به بایت تبدیل کن و برای سرور بفرست

        # دریافت و نمایش بنر خوش‌آمدگویی از سرور
        time.sleep(0.5)  # کمی صبر برای دریافت بنر
        banner = client.recv(4096).decode("utf-8")
        clear_screen()
        print(banner)

        # شروع ترد دریافت پیام
        receive_thread = threading.Thread(target=receive_messages, args=(client,))
        receive_thread.daemon = True
        # 	اگه برنامه اصلی بسته شد، این پیشخدمت هم خودکار بسته بشه

        receive_thread.start()

        while True:
            message = input("Enter Message: ")
            if message.lower() == "close":
                client.sendall(message.encode("utf-8"))
                break

            client.sendall(message.encode("utf-8"))

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
        print("Connection Closed.")


start_client()
