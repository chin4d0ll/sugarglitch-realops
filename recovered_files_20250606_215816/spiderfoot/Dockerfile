FROM python:3.11-slim

# ติดตั้ง dependencies พื้นฐาน
RUN apt-get update && apt-get install -y git build-essential libssl-dev libffi-dev python3-dev

# Clone source code SpiderFoot
RUN git clone https://github.com/smicallef/spiderfoot.git /opt/spiderfoot
WORKDIR /opt/spiderfoot

# ติดตั้ง Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001
CMD ["python3", "sf.py", "-l", "0.0.0.0:5001"]