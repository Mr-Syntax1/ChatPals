import socket
import threading

# به جای 0.0.0.0 بگذارید تا از همه شبکه‌ها اتصال قبول کند
ip_server = "0.0.0.0"
port_server = 8888

clients = {}


RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"


COLORS = [
    "\033[91m",  # قرمز روشن
    "\033[94m",  # آبی روشن
    "\033[95m",  # ارغوانی / بنفش روشن
    "\033[92m",  # سبز روشن
    "\033[93m",  # زرد روشن
    "\033[96m",  # فیروزه‌ای روشن
    "\033[31m",  # قرمز معمولی
    "\033[34m",  # آبی معمولی
]
RESET = "\033[0m"  # برگردوندن رنگ به حالت عادی

next_color_index = 0  # شمارنده چندمین کاربر چندمین رنگ رو گرفته
color_lock = threading.Lock()
# قفلی که جلوی تداخل تردها رو می‌گیره (چون چندتا کاربر همزمان ممکنه میان)


# ========== تابع نمایش بنر بزرگ ==========
def get_welcome_banner():
    """ساخت بنر خوش‌آمدگویی ChatPals"""
    banner = f"""
{BOLD}{CYAN}{'='*60}{RESET}
{BOLD}{YELLOW}██╗    ██╗███████╗██╗     ██████╗ ██████╗ ███╗   ███╗███████╗
{BOLD}{YELLOW}██║    ██║██╔════╝██║    ██╔════╝██╔═══██╗████╗ ████║██╔════╝
{BOLD}{YELLOW}██║ █╗ ██║█████╗  ██║    ██║     ██║   ██║██╔████╔██║█████╗  
{BOLD}{YELLOW}██║███╗██║██╔══╝  ██║    ██║     ██║   ██║██║╚██╔╝██║██╔══╝  
{BOLD}{YELLOW}╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗
{BOLD}{YELLOW} ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝{RESET}
{BOLD}{GREEN}{' '*20}WELCOME TO CHATPALS!{RESET}
{BOLD}{CYAN}{'='*60}{RESET}

{BOLD}{CYAN}{'='*60}{RESET}{"\n"}
{BOLD}{RED}{' '*10}If You Want To Leave The Chat Write [close]{RED}{"\n"}
{BOLD}{CYAN}{'='*60}{RESET}
"""
    return banner


def get_next_color():
    global next_color_index
    with color_lock:  # مطمئن می‌شه که فقط یک ترد به این تابع دسترسی داره
        color = COLORS[next_color_index % len(COLORS)]
        next_color_index += 1
        return color


def broadcast_message(sender_name, message, sender_color, sender_sock):
    for name, (addr, sock, color) in clients.items():
        if sock != sender_sock:
            try:
                colored_message = (
                    f"[{sender_name}] says: {sender_color}{message}{RESET}"
                )
                sock.send(colored_message.encode("utf-8"))
            except:
                pass


def handle_client(client_socket, client_addr):
    name = None
    try:
        name_data = client_socket.recv(1024).decode("utf-8")
        name = name_data.strip()  # فاصله‌های اضافه اول و آخر رو حذف کن
        client_color = get_next_color()

        clients[name] = (client_addr, client_socket, client_color)

        # ===== ارسال بنر خوش‌آمدگویی به کاربر جدید =====
        welcome_banner = get_welcome_banner()
        client_socket.send(welcome_banner.encode("utf-8"))

        # پیام خوش‌آمدگویی شخصی
        personal_welcome = f"{GREEN}✨ Welcome {client_color}{name}{GREEN}! You joined ChatPals ✨{RESET}\n"
        client_socket.send(personal_welcome.encode("utf-8"))

        # اعلام ورود به سرور
        print(
            f"{client_color}[*] [{name}] connected from {client_addr[0]}:{client_addr[1]}{RESET}"
        )

        # اعلام ورود به دیگران
        join_msg = f"✨ {name} joined the chat! ✨"
        for other_name, (addr, sock, color) in clients.items():
            if sock != client_socket:
                try:
                    sock.send(join_msg.encode("utf-8"))
                except:
                    pass

        while True:
            request = client_socket.recv(1024).decode("utf-8")
            if not request or request.lower() == "close":
                break

            print(f"{client_color}[{name}] says: {request}{RESET}")
            broadcast_message(name, request, client_color, client_socket)

    except Exception as e:
        print(f"[*] Error ({name}): {e}")
    finally:
        if name and name in clients:
            del clients[name]
            leave_msg = f"💔 {name} left the chat. 💔"
            for other_name, (addr, sock, color) in clients.items():
                try:
                    sock.send(leave_msg.encode("utf-8"))
                    # متن رو به بایت تبدیل کن بفرست
                except:
                    pass
            print(f"{name} disconnected.")
        client_socket.close()


def start_server():
    # نمایش اطلاعات مهم برای اتصال دیگران

    print(get_welcome_banner())

    print("\n" + "=" * 50)
    print("\033[92m✅ ChatPals Server is running!\033[0m")
    print("=" * 50)

    # دریافت IP خصوصی
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"\033[93m🏠 Your Local IP (for port forwarding): \033[96m{local_ip}\033[0m")
    print(f"\033[93m🔌 Port: \033[96m{port_server}\033[0m")
    # print(f"\033[93m Host name : {hostname}\033[0m")
    print("=" * 50)
    print("\033[92m✅ Server is running and waiting for connections...\033[0m\n")

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # ipv4 , tcp
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # بذار بعد از بستن سرور، دوباره بتونم سریع روشنش کنم
        server.bind((ip_server, port_server))
        # فقط به این ایپی و پورت گوش کن
        server.listen(50)  # حداکثر 50 کلاینت
        print(
            f"\033[92m[*] Listening on all interfaces (0.0.0.0:{port_server})\033[0m\n"
        )

        while True:
            client_socket, client_addr = server.accept()
            # پشت در بایست و منتظر بمون تا کسی بیاد در بزنه
            threading.Thread(
                target=handle_client,
                args=(client_socket, client_addr),
                #  یه پیشخدمت جدید استخدام کن و این کار هارو بکن و اطلاعات کاربر رو هم بده
            ).start()
    except Exception as e:
        print(f"\033[91m[*] Server Error: {e}\033[0m")
    finally:
        server.close()


if __name__ == "__main__":
    start_server()
