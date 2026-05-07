import attr, re, json, random, string, time, requests
from mimetypes import guess_type 
from login import loginFacebook

# Lưu credentials để tự động đăng nhập lại khi cookie chết
_credentials = {"username": None, "password": None, "twofa": None}

DEAD_COOKIE_MARKER = "Unable to retrieve data for fb_dtsg. It's possible that they have been deleted or modified."


def _is_dead_cookie_data(dataFB):
     if not isinstance(dataFB, dict):
          return True
     return dataFB.get("fb_dtsg") == DEAD_COOKIE_MARKER or not dataFB.get("fb_dtsg")


def relogin_get_cookie():
     """Đăng nhập lại bằng credentials đã lưu, trả về cookie string hoặc None."""
     if not _credentials["username"] or not _credentials["password"]:
          print(">>> Không có thông tin đăng nhập để tự động login lại.")
          return None
     try:
          print(">>> Đang đăng nhập lại Facebook...")
          result = loginFacebook(
               _credentials["username"],
               _credentials["password"],
               _credentials["twofa"],
          ).main()
          if "success" in result:
               new_cookie = result["success"]["setCookies"]
               print(">>> Đăng nhập lại thành công!")
               return new_cookie
          err = result.get("error", {})
          print(f">>> Đăng nhập lại thất bại: {err.get('title')} - {err.get('description')}")
          return None
     except Exception as e:
          print(f">>> Lỗi khi đăng nhập lại: {e}")
          return None


def refresh_session(dataFB):
     """Thử lấy lại cookie mới và data home khi phát hiện cookie chết."""
     new_cookie = relogin_get_cookie()
     if not new_cookie:
          return None
     try:
          new_data = dataGetHome(new_cookie)
          if _is_dead_cookie_data(new_data):
               print(">>> Cookie mới vẫn không hợp lệ.")
               return None
          # Cập nhật dataFB tại chỗ
          dataFB.clear()
          dataFB.update(new_data)
          return dataFB
     except Exception as e:
          print(f">>> Lỗi khi làm mới phiên: {e}")
          return None

def Headers(setCookies, dataForm=None, Host=None):
     if (Host == None): Host = "www.facebook.com"
     headers = {}
     headers["Host"] = Host
     headers["Connection"] = "keep-alive"
     if (dataForm != None):
          headers["Content-Length"] = str(len(dataForm))
     headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
     headers["Accept"] = "*/*"
     headers["Origin"] = "https://" + Host
     headers["Sec-Fetch-Site"] = "same-origin"
     headers["Sec-Fetch-Mode"] = "cors"
     headers["Sec-Fetch-Dest"] = "empty"
     headers["Referer"] = "https://" + Host
     headers["Accept-Language"] = "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7"
     
     return headers
     
def digitToChar(digit):
          if digit < 10:
               return str(digit)
          return chr(ord("a") + digit - 10)

def str_base(number, base):
     if number < 0:
          return "-" + str_base(-number, base)
     (d, m) = divmod(number, base)
     if d > 0:
          return str_base(d, base) + digitToChar(m)
     return digitToChar(m)

def parse_cookie_string(cookie_string):
     cookie_dict = {}
     cookies = cookie_string.split(";")

     for cookie in cookies:
          if "=" in cookie:
               key, value = cookie.split("=")
          else:
               pass
          try: cookie_dict[key] = value
          except: pass

     return cookie_dict

def dataSplit(string1, string2, numberSplit1=None, numberSplit2=None, HTML=None, amount=None, string3=None, numberSplit3=None, defaultValue=None):
     if (defaultValue): numberSplit1, numberSplit2 = 1, 0
     if (amount == None):
          return HTML.split(string1)[numberSplit1].split(string2)[numberSplit2]
     elif (amount == 3):
          return HTML.split(string1)[numberSplit1].split(string2)[numberSplit2].split(string3)[numberSplit3]
     
def formAll(dataFB, FBApiReqFriendlyName=None, docID=None, requireGraphql=None):
     __reg = attr.ib(0).counter
     _revision = attr.ib()
     __reg += 1 
     dataForm = {}
     
     if (requireGraphql == None):
          dataForm["fb_dtsg"] = dataFB["fb_dtsg"]
          dataForm["jazoest"] = dataFB["jazoest"]
          dataForm["__a"] = 1
          dataForm["__user"] =str(dataFB["FacebookID"])
          dataForm["__req"] = str_base(__reg, 36) 
          dataForm["__rev"] = dataFB["clientRevision"]
          dataForm["av"] = dataFB["FacebookID"]
          dataForm["fb_api_caller_class"] = "RelayModern"
          dataForm["fb_api_req_friendly_name"] = FBApiReqFriendlyName
          dataForm["server_timestamps"] = "true"
          dataForm["doc_id"] = str(docID)
     else:
          dataForm["fb_dtsg"] = dataFB["fb_dtsg"]
          dataForm["jazoest"] = dataFB["jazoest"]
          dataForm["__a"] = 1
          dataForm["__user"] =str(dataFB["FacebookID"])
          dataForm["__req"] = str_base(__reg, 36) 
          dataForm["__rev"] = dataFB["clientRevision"]
          dataForm["av"] = dataFB["FacebookID"]

     return dataForm
     
def mainRequests(urlRequests, dataForm, setCookies):
     return {
          "headers": Headers(setCookies, dataForm),
          "timeout": 5,
          "url": urlRequests, # "https://www.facebook.com/api/graphql/",
          "data": dataForm,
          "cookies": parse_cookie_string(setCookies),
          "verify": True
     }
     
def dataGetHome(setCookies):
     
     mainRequests = {
          "headers": {
               "authority": "www.facebook.com",
               "method": "GET",
               "path": "/",
               "scheme": "https",
               "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
               "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
               "cache-control": "max-age=0",
               "cookie": setCookies,
               "dpr": "1.25",
               "priority": "u=0, i",
               "sec-ch-prefers-color-scheme": "dark",
               "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
               "sec-ch-ua-full-version-list": '"Chromium";v="140.0.7339.128", "Not=A?Brand";v="24.0.0.0", "Google Chrome";v="140.0.7339.128"',
               "sec-ch-ua-mobile": "?0",
               "sec-ch-ua-model": '""',
               "sec-ch-ua-platform": '"Windows"',
               "sec-ch-ua-platform-version": '"19.0.0"',
               "sec-fetch-dest": "document",
               "sec-fetch-mode": "navigate",
               "sec-fetch-site": "same-origin",
               "sec-fetch-user": "?1",
               "upgrade-insecure-requests": "1",
               "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
               "viewport-width": "493"
          },
          "timeout": 60000,
          "url": "https://www.facebook.com/",
          "cookies": parse_cookie_string(setCookies),
          "verify": True
     }
     
     dictValueSaved = {}
     splitDataList = [
          # FORMAT: nameValue, stringData_1, stringData_2
          ["fb_dtsg", "DTSGInitialData\",[],{\"token\":\"", "\""],
          ["fb_dtsg_ag", "async_get_token\":\"", "\""],
          ["jazoest", "jazoest=", "\""],
          ["hash", "hash\":\"", "\""],
          ["sessionID", "sessionId\":\"", "\""],
          ["FacebookID", "\"actorID\":\"", "\""],
          ["clientRevision", "client_revision\":", ","]
     ]
     
     sendRequests = requests.get(**mainRequests).text
     for i in splitDataList:
          nameValue = i[0]
          try:
               exportValue = dataSplit(i[1], i[2], HTML=sendRequests, defaultValue=True)
          except:
               exportValue = "Unable to retrieve data for %s. It's possible that they have been deleted or modified." % nameValue
          dictValueSaved[nameValue] = exportValue
     dictValueSaved["cookieFacebook"] = setCookies
     
     return dictValueSaved

def _looks_like_auth_error(parsed):
    """Phát hiện response báo phiên đăng nhập đã hết hạn."""
    if not isinstance(parsed, dict):
         return False
    err_code = parsed.get("errorCode") or parsed.get("error")
    err_summary = (parsed.get("errorSummary") or "").lower()
    err_desc = (parsed.get("errorDescription") or "").lower()
    if err_code in (1357001, 1357004, "1357001", "1357004"):
         return True
    keywords = ("login", "log in", "session", "đăng nhập", "phiên")
    return any(k in err_summary or k in err_desc for k in keywords)


def _post_graphql(dataFB, friendly_name, doc_id, variables):
    """Gửi request GraphQL với try/except và tự động re-login khi cookie chết."""
    for attempt in range(2):
         try:
              dataForm = formAll(dataFB, friendly_name, doc_id)
              dataForm["variables"] = json.dumps(variables)
              response = requests.post(**mainRequests(
                   "https://www.facebook.com/api/graphql/",
                   dataForm,
                   dataFB["cookieFacebook"],
              ))
              try:
                   parsed = json.loads(response.text)
              except (ValueError, json.JSONDecodeError):
                   parsed = None

              if parsed is None or _looks_like_auth_error(parsed):
                   if attempt == 0 and refresh_session(dataFB):
                        continue
                   return parsed if parsed is not None else {"error": "invalid_response", "raw": response.text[:300]}
              return parsed
         except requests.RequestException as e:
              print(f">>> Lỗi mạng: {e}")
              if attempt == 0 and refresh_session(dataFB):
                   continue
              return {"error": "network_error", "message": str(e)}
         except Exception as e:
              print(f">>> Lỗi không xác định: {e}")
              return {"error": "unknown", "message": str(e)}
    return {"error": "failed_after_retry"}


def getSuggestFriends(dataFB):
    parsed = _post_graphql(dataFB, "FriendingCometSuggestionsRootQuery", 24180156278339004, {"scale": 1})
    try:
         return parsed['data']['viewer']['people_you_may_know']['edges']
    except (KeyError, TypeError):
         print(f">>> Không lấy được danh sách gợi ý: {parsed}")
         return []

def sendAddFriend(dataFB, uid):
    return _post_graphql(
         dataFB,
         "FriendingCometFriendRequestSendMutation",
         25491427290506954,
         {
              "input": {
                   "click_correlation_id": str(int(time.time())),
                   "click_proof_validation_result": "{\"validated\":true}",
                   "friend_requestee_ids": [f"{uid}"],
                   "friending_channel": "FRIENDS_HOME_MAIN",
                   "warn_ack_for_ids": [],
                   "actor_id": dataFB["FacebookID"],
                   "client_mutation_id": "2",
              },
              "scale": 1,
         },
    )
# =============================================================
#                              UI
# =============================================================
import threading
import queue
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

# Sử dụng builtin print gốc cho UI (sẽ override print trong module này khi chạy UI
# để các hàm bên trên log thẳng vào cửa sổ).
import builtins as _builtins
_builtin_print = _builtins.print


class AddFriendApp:
     def __init__(self, root):
          self.root = root
          self.root.title("Auto Add Friend - Facebook")
          self.root.geometry("780x620")
          self.root.minsize(680, 540)

          self.log_queue = queue.Queue()
          self.worker_thread = None
          self.stop_event = threading.Event()
          self.getData = None

          self._build_ui()
          self._patch_print()
          self.root.after(120, self._drain_log_queue)
          self.root.protocol("WM_DELETE_WINDOW", self._on_close)

     def _build_ui(self):
          pad = {"padx": 8, "pady": 4}

          frm_top = ttk.LabelFrame(self.root, text="Thông tin đăng nhập")
          frm_top.pack(fill="x", **pad)

          ttk.Label(frm_top, text="Cookie:").grid(row=0, column=0, sticky="ne", padx=6, pady=4)
          self.txt_cookie = tk.Text(frm_top, height=4, wrap="word")
          self.txt_cookie.grid(row=0, column=1, columnspan=3, sticky="ew", padx=6, pady=4)

          ttk.Label(frm_top, text="Email/SĐT/UID:").grid(row=1, column=0, sticky="e", padx=6, pady=4)
          self.ent_user = ttk.Entry(frm_top)
          self.ent_user.grid(row=1, column=1, sticky="ew", padx=6, pady=4)

          ttk.Label(frm_top, text="Mật khẩu:").grid(row=1, column=2, sticky="e", padx=6, pady=4)
          self.ent_pass = ttk.Entry(frm_top, show="*")
          self.ent_pass.grid(row=1, column=3, sticky="ew", padx=6, pady=4)

          ttk.Label(frm_top, text="2FA Key:").grid(row=2, column=0, sticky="e", padx=6, pady=4)
          self.ent_2fa = ttk.Entry(frm_top)
          self.ent_2fa.grid(row=2, column=1, sticky="ew", padx=6, pady=4)

          ttk.Label(frm_top, text="Delay (giây):").grid(row=2, column=2, sticky="e", padx=6, pady=4)
          self.ent_delay = ttk.Entry(frm_top, width=8)
          self.ent_delay.insert(0, "5")
          self.ent_delay.grid(row=2, column=3, sticky="w", padx=6, pady=4)

          frm_top.columnconfigure(1, weight=1)
          frm_top.columnconfigure(3, weight=1)

          frm_action = ttk.Frame(self.root)
          frm_action.pack(fill="x", **pad)

          self.btn_login = ttk.Button(frm_action, text="Đăng nhập / Kiểm tra cookie", command=self.on_login)
          self.btn_login.pack(side="left", padx=4)

          self.btn_start = ttk.Button(frm_action, text="Bắt đầu add friend", command=self.on_start, state="disabled")
          self.btn_start.pack(side="left", padx=4)

          self.btn_stop = ttk.Button(frm_action, text="Dừng", command=self.on_stop, state="disabled")
          self.btn_stop.pack(side="left", padx=4)

          self.btn_clear = ttk.Button(frm_action, text="Xoá log", command=lambda: self._set_log_text(""))
          self.btn_clear.pack(side="left", padx=4)

          self.var_status = tk.StringVar(value="Sẵn sàng.")
          ttk.Label(self.root, textvariable=self.var_status, anchor="w", relief="sunken").pack(fill="x", padx=8)

          frm_log = ttk.LabelFrame(self.root, text="Log")
          frm_log.pack(fill="both", expand=True, **pad)
          self.txt_log = scrolledtext.ScrolledText(
               frm_log, wrap="word", state="disabled",
               bg="#111", fg="#ddd", insertbackground="#ddd", font=("Consolas", 10)
          )
          self.txt_log.pack(fill="both", expand=True, padx=4, pady=4)

     def _patch_print(self):
          """Redirect print() trong module main sang UI log queue."""
          q = self.log_queue

          def ui_print(*args, **kwargs):
               end = kwargs.get("end", "\n")
               sep = kwargs.get("sep", " ")
               msg = sep.join(str(a) for a in args) + ("" if end == "\r" else end)
               q.put(msg)

          # Override binding 'print' trong module hiện tại
          globals()["print"] = ui_print

     def _drain_log_queue(self):
          try:
               while True:
                    msg = self.log_queue.get_nowait()
                    self._append_log(msg)
          except queue.Empty:
               pass
          self.root.after(120, self._drain_log_queue)

     def _append_log(self, msg):
          self.txt_log.configure(state="normal")
          self.txt_log.insert("end", msg)
          self.txt_log.see("end")
          self.txt_log.configure(state="disabled")

     def _set_log_text(self, text):
          self.txt_log.configure(state="normal")
          self.txt_log.delete("1.0", "end")
          self.txt_log.insert("end", text)
          self.txt_log.configure(state="disabled")

     def _log(self, msg):
          self.log_queue.put(msg + "\n")

     def _set_status(self, text):
          self.var_status.set(text)

     def _collect_credentials(self):
          _credentials["username"] = self.ent_user.get().strip() or None
          _credentials["password"] = self.ent_pass.get().strip() or None
          _credentials["twofa"] = self.ent_2fa.get().strip() or None

     def on_login(self):
          cookie = self.txt_cookie.get("1.0", "end").strip()
          self._collect_credentials()

          if not cookie and not (_credentials["username"] and _credentials["password"]):
               messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập cookie hoặc email/mật khẩu.")
               return

          self._set_status("Đang kiểm tra cookie...")
          self.btn_login.configure(state="disabled")

          def work():
               try:
                    data = {}
                    if cookie:
                         try:
                              data = dataGetHome(cookie)
                         except Exception as e:
                              self._log(f"Lỗi lấy data từ cookie: {e}")
                              data = {}

                    if _is_dead_cookie_data(data):
                         self._log("Cookie không hợp lệ hoặc trống, thử đăng nhập lại...")
                         refreshed = refresh_session(data if isinstance(data, dict) else {})
                         if not refreshed:
                              self.root.after(0, lambda: self._set_status("Đăng nhập thất bại."))
                              return
                         data = refreshed

                    self.getData = data
                    fbid = data.get("FacebookID", "?")
                    self._log(f"Đăng nhập thành công | Facebook ID: {fbid}")
                    self.root.after(0, lambda: self._set_status(f"Đã đăng nhập: {fbid}"))
                    self.root.after(0, lambda: self.btn_start.configure(state="normal"))
               finally:
                    self.root.after(0, lambda: self.btn_login.configure(state="normal"))

          threading.Thread(target=work, daemon=True).start()

     def on_start(self):
          if not self.getData:
               messagebox.showwarning("Chưa đăng nhập", "Vui lòng đăng nhập trước.")
               return
          if self.worker_thread and self.worker_thread.is_alive():
               return

          try:
               delay = int(self.ent_delay.get().strip() or "5")
          except ValueError:
               delay = 5

          self._collect_credentials()
          self.stop_event.clear()
          self.btn_start.configure(state="disabled")
          self.btn_stop.configure(state="normal")
          self._set_status("Đang chạy...")

          self.worker_thread = threading.Thread(target=self._run_loop, args=(delay,), daemon=True)
          self.worker_thread.start()

     def on_stop(self):
          self.stop_event.set()
          self._set_status("Đang dừng...")
          self.btn_stop.configure(state="disabled")

     def _run_loop(self, delay):
          try:
               while not self.stop_event.is_set():
                    try:
                         suggestFriends = getSuggestFriends(self.getData)
                    except Exception as e:
                         self._log(f">>> Lỗi khi lấy danh sách gợi ý: {e}")
                         suggestFriends = []

                    if not suggestFriends:
                         self._log(">>> Không có gợi ý nào, chờ rồi thử lại...")
                         if self._interruptible_sleep(max(delay, 10)):
                              break
                         continue

                    self._log("= " * 15)
                    for i in suggestFriends:
                         if self.stop_event.is_set():
                              break
                         try:
                              uid = i["node"]["id"]
                              name = i["node"]["name"]
                              social = i["node"].get("social_context", {}).get("text", "")
                              self._log(f"UID: {uid} | Name: {name} | Social: {social}")
                         except (KeyError, TypeError) as e:
                              self._log(f">>> Bỏ qua mục lỗi: {e}")
                              continue

                         try:
                              resp = sendAddFriend(self.getData, uid)
                              data_block = (resp or {}).get("data") or {}
                              send_block = data_block.get("friend_request_send") or {}
                              if send_block.get("friend_requestees") is None:
                                   err_msg = (resp or {}).get("error", {})
                                   if isinstance(err_msg, dict):
                                        err_msg = err_msg.get("message", resp)
                                   self._log(f">>> Thêm bạn bè thất bại: {err_msg}")
                              else:
                                   self._log(">>> Đã gửi lời mời kết bạn thành công!")
                         except Exception as e:
                              self._log(f">>> Lỗi khi gửi kết bạn: {e}")

                         if self._interruptible_sleep(delay):
                              break
                         self._log("= " * 15)
          finally:
               self.root.after(0, lambda: self.btn_start.configure(state="normal"))
               self.root.after(0, lambda: self.btn_stop.configure(state="disabled"))
               self.root.after(0, lambda: self._set_status("Đã dừng."))

     def _interruptible_sleep(self, seconds):
          end = time.time() + seconds
          while time.time() < end:
               if self.stop_event.is_set():
                    return True
               time.sleep(0.2)
          return False

     def _on_close(self):
          if self.worker_thread and self.worker_thread.is_alive():
               if not messagebox.askyesno("Thoát", "Tool đang chạy. Thoát thật?"):
                    return
               self.stop_event.set()
          self.root.destroy()


def run_ui():
     root = tk.Tk()
     try:
          style = ttk.Style()
          if "vista" in style.theme_names():
               style.theme_use("vista")
          elif "clam" in style.theme_names():
               style.theme_use("clam")
     except Exception:
          pass
     AddFriendApp(root)
     root.mainloop()


if __name__ == "__main__":
     run_ui()