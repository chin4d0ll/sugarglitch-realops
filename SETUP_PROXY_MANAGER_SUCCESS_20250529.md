# สรุปการตั้งค่าและทดสอบ Bright Data Proxy Manager (SG Zone)

**วันที่:** 2025-05-29

## ขั้นตอนที่ดำเนินการ

1. สร้าง/ตั้งค่า proxy port 24000 ใน Proxy Manager ผ่าน UI
2. ใส่ Bright Data credentials ที่ถูกต้อง (zone: mobile_proxy, password: q9yihckpz3qk)
3. อนุญาต allowlisted IPs เป็น 0.0.0.0 (ทุก IP)
4. ทดสอบ proxy ด้วยคำสั่ง curl:

```bash
curl -k -x http://127.0.0.1:24000 https://geo.brdtest.com/mygeo.json
```

**ผลลัพธ์:**

- สามารถดึง geo IP ออกมาได้สำเร็จ (ตัวอย่าง: RU, Tyumen, MegaFon)
- Proxy Manager พร้อมใช้งานสำหรับงาน automation หรือ integration อื่น ๆ

---

## หมายเหตุ

- หากต้องการเปลี่ยน zone หรือ credentials ให้แก้ไขใน proxy_config.json หรือผ่าน UI
- หากต้องการทดสอบกับ endpoint อื่น หรือเขียนสคริปต์ Python แจ้งได้เลย

---

บันทึกโดย GitHub Copilot (อัตโนมัติ)
