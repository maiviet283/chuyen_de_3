Dưới đây là lời giải thích cho ba câu hỏi đầu tiên trong tài liệu:

### 1. **What are the hash values (MD5 & SHA-1) of all images? Does the acquisition and verification hash value match?**
   - **Hash values của PC Image:**
     - MD5: `A49D1254C873808C58E6F1BCD60B5BDE`
     - SHA-1: `AFE5C9AB487BD47A8A9856B1371C2384D44FD785`
   - **Hash values của RM#2 Image:**
     - MD5: `B4644902ACAB4583A1D0F9F1A08FAA77`
     - SHA-1: `048961A85CA3ECED8CC73F1517442D31D4DCA0A3`
   - **Hash values của RM#3 (Type1):**
     - MD5: `858C7250183A44DD83EB706F3F178990`
     - SHA-1: `471D3EEDCA9ADD872FC0708297284E1960FF44F8`
   - **Hash values của RM#3 (Type2):**
     - MD5: `858C7250183A44DD83EB706F3F178990`
     - SHA-1: `471D3EEDCA9ADD872FC0708297284E1960FF44F8`
   - **Hash values của RM#3 (Type3):**
     - MD5: `DF914108FB3D86744EB688EBA482FBDF`
     - SHA-1: `7F3C2EB1F1E2DB97BE6E963625402A0E362A532C`
   - **Kết quả xác minh:**
     - Giá trị hash thu được từ quá trình tạo ảnh pháp y (acquisition) trùng khớp với giá trị hash kiểm tra lại (verification), chứng minh rằng dữ liệu không bị thay đổi trong quá trình thu thập.

---

### 2. **Identify the partition information of PC image.**
   - **Bảng phân vùng của ổ đĩa PC:**
     | No. | Bootable | File System | Start Sector | Total Sectors | Size |
     |----|-----------|-------------|--------------|--------------|------|
     | 1  | No        | NTFS        | 2,048        | 204,800      | 100 MB |
     | 2  | Yes       | NTFS        | 206,848      | 41,734,144   | 19.9 GB |

   - **Phân tích:**
     - Ổ đĩa có hai phân vùng: 
       - Phân vùng đầu tiên có kích thước 100MB, có thể là phân vùng khởi động hệ thống.
       - Phân vùng chính chứa hệ điều hành có kích thước khoảng 19.9GB và được định dạng NTFS.

---

### 3. **Explain installed OS information in detail. (OS name, install date, registered owner…)**
   - **Hệ điều hành cài đặt:**
     - OS Name: `Windows 7 Ultimate`
     - Version: `6.1`
     - Build Number: `7601`
     - Registered Owner: `informant`
     - System Root: `C:\Windows`
     - Install Date: `2015-03-22 14:34:26 (GMT)`

   - **Nguồn thông tin:**
     - Các giá trị này có thể được tìm thấy trong registry tại đường dẫn:
       ```
       HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion
       ```

---
Dưới đây là lời giải từ câu 4 đến câu 10:

---

### **4. What is the timezone setting?**  
   - **Cài đặt múi giờ:**  
     - `Eastern Time (US & Canada) (UTC-05:00)`  
     - `Daylight Time Bias: +1` (cho thấy hệ thống có thể tự động điều chỉnh giờ mùa hè)  
   - **Nguồn thông tin:**  
     - Registry key:  
       ```
       HKLM\SYSTEM\ControlSet###\Control\TimeZoneInformation
       ```

---

### **5. What is the computer name?**  
   - **Tên máy tính:** `INFORMANT-PC`  
   - **Nguồn thông tin:**  
     - Có thể tìm thấy trong registry tại:  
       ```
       HKLM\SYSTEM\ControlSet###\Control\ComputerName\ComputerName  (value: ComputerName)
       HKLM\SYSTEM\ControlSet###\Services\Tcpip\Parameters  (value: Hostname)
       ```

---

### **6. List all accounts in OS except the system accounts: Administrator, Guest, systemprofile, LocalService, NetworkService. (Account name, login count, last logon date…)**  
   - **Danh sách tài khoản người dùng (không tính tài khoản hệ thống):**  

     | Account Name | Login Count | Last Logon Date |
     |-------------|------------|-----------------|
     | `informant`  | 10         | `2015-03-25 09:45:59` |
     | `admin11`    | 2          | `2015-03-22 10:57:02` |
     | `ITechTeam`  | 0          | `-` |
     | `temporary`  | 1          | `2015-03-22 10:55:57` |

   - **Nguồn thông tin:**  
     - Registry key:  
       ```
       HKLM\SAM\~
       ```
     - **Hash mật khẩu:**  
       - `informant`: `9E3D31B073E60BFD7B07978D6F914D0A` (Password: `informant#suspect1`)  
       - `admin11`: `21759544B2D7EFCCC978449463CF7E63` (Password: `djemals11`)  
       - `ITechTeam`: `75ED0CB7676889AB43764A3B7D3E6943` (Password: `dkdlxpzmxla`)  
       - `temporary`: `1B3801B608A6BE89D21FD3C5729D30BF` (Password: `xpavhfkfl`)  

---

### **7. Who was the last user to logon into PC?**  
   - **Tài khoản cuối cùng đăng nhập:** `informant`  
   - **Nguồn thông tin:**  
     - Registry key:  
       ```
       HKLM\SAM\~
       ```

---

### **8. When was the last recorded shutdown date/time?**  
   - **Thời gian tắt máy cuối cùng:** `2015-03-25 11:31:05 (Eastern Time + DST)`  
   - **Nguồn thông tin:**  
     - Registry key:  
       ```
       HKLM\SYSTEM\ControlSet###\Control\Windows  (value: ShutdownTime)
       ```

---

### **9. Explain the information of network interface(s) with an IP address assigned by DHCP.**  
   - **Thông tin mạng:**  

     | Parameter         | Value |
     |------------------|----------------|
     | Device Name      | Intel(R) PRO/1000 MT Network Connection |
     | IP Address       | `10.11.11.129` |
     | Subnet Mask      | `255.255.255.0` |
     | Name Server      | `10.11.11.2` |
     | Domain          | `localdomain` |
     | Default Gateway | `10.11.11.2` |
     | DHCP Usage      | `Yes` |
     | DHCP Server     | `10.11.11.254` |

   - **Nguồn thông tin:**  
     - Registry key:  
       ```
       HKLM\SYSTEM\ControlSet###\Services\Tcpip\Parameters\Interfaces\{GUID}
       ```

---

### **10. What applications were installed by the suspect after installing OS?**  
   - **Danh sách ứng dụng đã cài đặt:**  

     | Installation Time (UTC-5) | Name | Version | Manufacturer |
     |------------------|------------------------------------|------------------|--------------------|
     | 2015-03-22 10:04:14 | Microsoft Office Professional Plus 2013 | 15.0.4420.1017 | Microsoft Corporation |
     | 2015-03-22 10:11:51 | Google Chrome | 41.0.2272.101 | Google Inc. |
     | 2015-03-22 10:16:03 | Google Update Helper | 1.3.26.9 | Google Inc. |
     | 2015-03-23 15:00:45 | Apple Application Support | 3.0.6 | Apple Inc. |
     | 2015-03-23 15:00:58 | Bonjour | 3.0.0.10 | Apple Inc. |
     | 2015-03-23 15:01:01 | Apple Software Update | 2.1.3.127 | Apple Inc. |
     | 2015-03-23 15:02:46 | Google Drive | 1.20.8672.3137 | Google Inc. |
     | 2015-03-25 09:51:39 | Microsoft .NET Framework 4 | 4.0.30319 | Microsoft Corporation |
     | 2015-03-25 09:57:31 | Eraser | 6.2.2962 | The Eraser Project |

   - **Nguồn thông tin:**  
     - Registry key:  
       ```
       HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\~
       HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\~
       ```

---

Nếu bạn cần giải thích thêm hoặc tiếp tục với các câu tiếp theo, cứ hỏi mình nhé! 😊
