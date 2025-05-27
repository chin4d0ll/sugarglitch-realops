import pikepdf
src = 'FINAL_REAL_DATA_REPORTS/ALX_TRADING_SENSITIVE_DATA_REPORT_20250527.pdf'
dst = 'FINAL_REAL_DATA_REPORTS/ALX_TRADING_SENSITIVE_DATA_REPORT_20250527_repaired.pdf'
try:
    pdf = pikepdf.open(src)
    pdf.save(dst)
    pdf.close()
    print(f'✅ ซ่อมแซม PDF สำเร็จ: {dst}')
except Exception as e:
    print(f'❌ ซ่อมแซม PDF ไม่สำเร็จ: {e}')
